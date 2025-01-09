from pathlib import Path
from wowool.native.core import PipeLine
from wowool.error import Error
from wowool.io.provider import Factory
import subprocess
from collections import Counter
import time
from functools import cmp_to_key
from dataclasses import dataclass, field
from nlp_compare.nlp_engine import get_nlp_engine
from nlp_compare.cmp_objects import CmpItem
from logging import getLogger
from tabulate import tabulate
from nlp_compare.concept_filter import ConceptFilter
import csv
import re


MISSING = "**Missing**"


logger = getLogger("nlp_engine")


@dataclass
class RowData:
    source: str
    uri: str
    begin_offset: int
    end_offset: int
    text: str | None = None
    literal: str | None = None


@dataclass
class NlpData:
    name: str
    cmp_idx: int
    time: float = 0
    counter: Counter = field(default_factory=Counter)
    data: list[CmpItem] = field(default_factory=list)
    tt_time: float = 0
    tt_counter: Counter = field(default_factory=Counter)
    missing: list[CmpItem] = field(default_factory=list)
    rows: list[RowData] = field(default_factory=list)

    def add_row(
        self,
        uri,
        begin_offset,
        end_offset,
        text: str | None = None,
        literal: str | None = None,
    ):
        self.rows.append(
            RowData(self.name, uri, begin_offset, end_offset, text, literal)
        )


def find_source(compare_data, cmp_idx):
    for source, data in compare_data.items():
        if data.cmp_idx == cmp_idx:
            return source
    return None


def get_next_valid_idx(offset_data, offset_data_len, idx):
    nidx = idx + 1
    while nidx < offset_data_len:
        if offset_data[nidx]:
            return nidx
        nidx = idx + 1

    return -1


def insert_missing_comparison_items(offset_data: list[CmpItem], nlp_engines: list):
    # print("Insert missing comparison items")
    # print(*offset_data, sep="\n")
    sz_cmp = len(nlp_engines)
    size_offset_data = len(offset_data)
    offset_data_ = []
    idx = 0
    while idx < size_offset_data:
        lhs = offset_data[idx]
        cmp_items = [None] * sz_cmp
        if lhs.uri == "Sentence":
            cmp_items[lhs.cmp_idx] = lhs
            offset_data_.append(cmp_items)
            idx += 1
            continue

        nidx = get_next_valid_idx(offset_data, size_offset_data, idx)
        if nidx == -1:
            cmp_items[lhs.cmp_idx] = lhs
            offset_data_.append(cmp_items)
            break

        cmp_items[lhs.cmp_idx] = lhs
        while nidx != -1:
            rhs = offset_data[nidx]
            if lhs.begin_offset == rhs.begin_offset:
                if lhs.end_offset == rhs.end_offset:
                    if cmp_items[rhs.cmp_idx] and cmp_items[rhs.cmp_idx].uri != rhs.uri:
                        cmp_items[rhs.cmp_idx].uri += f", {rhs.uri}"
                    else:
                        cmp_items[rhs.cmp_idx] = rhs
                elif lhs.uri == rhs.uri:
                    cmp_items[rhs.cmp_idx] = rhs
                else:
                    break
            else:
                break
            if len(cmp_items) != sz_cmp:
                raise Error("Should not get here")

            nidx = get_next_valid_idx(offset_data, size_offset_data, nidx)

        offset_data_.append(cmp_items)
        if nidx != -1:
            idx = nidx
        else:
            idx += 1

    return offset_data_


class FileHandler:
    def __init__(self, name):
        self.fn = Path(name)
        self.name = self.fn.stem
        self.fh = open(self.fn, "w")
        self.lines_ = None

    def write(self, data):
        self.fh.write(data)

    def close(self):
        self.fh.close()

    @property
    def lines(self):
        if self.lines_ is None:
            with open(self.fn) as fh:
                self.lines_ = fh.readlines()
        return self.lines_


def get_filehandels(name: str):
    return {
        "wowool": FileHandler("wowool.diff"),
        name: FileHandler(f"{name}.diff"),
    }


def print_diff(offset_data: list[CmpItem], nlp_name: str):

    size_offset_data = len(offset_data)
    cmp_info = get_filehandels(nlp_name)
    wow_, other_ = cmp_info["wowool"], cmp_info[nlp_name]

    idx = 0
    for k, item in cmp_info.items():
        item.write(f"{'-' *30} {k} {'-' *30}\n")

    while idx < size_offset_data:

        # ic(offset_data[idx])
        # print("idx", idx, offset_data[idx])
        if offset_data[idx].uri == "Sentence":
            wow_.write(f"\n{offset_data[idx].text}\n")
            other_.write(f"\n{offset_data[idx].text}\n")
            idx += 1
            continue

        lhs = offset_data[idx]
        if lhs.begin_offset == None:
            idx += 1
            continue

        nidx = get_next_valid_idx(offset_data, size_offset_data, idx)
        if nidx >= size_offset_data or nidx == -1:
            cmp_info[lhs.source].write(
                f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
            )
            # check to write to the other side
            if "wowool" == lhs.source:
                other_.write(
                    f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                )
            else:
                wow_.write(
                    f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                )
            break

        rhs = offset_data[nidx]

        # check begin offsets.
        # if args.verbose:
        #     ic(lhs, rhs)
        if lhs.begin_offset == rhs.begin_offset:
            if lhs.end_offset == rhs.end_offset:
                if lhs.source != rhs.source:
                    cmp_info[lhs.source].write(
                        f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                    )
                    cmp_info[rhs.source].write(
                        f"({rhs.begin_offset:<3},{rhs.end_offset:<3}) {rhs.uri:<30}:{rhs.text}\n"
                    )
                    idx = idx + 2
                else:
                    if lhs.source == "wowool":
                        wow_.write(
                            f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                        )
                        other_.write(
                            f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                        )
                    else:
                        wow_.write(
                            f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                        )
                        other_.write(
                            f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                        )
                    idx += 1
            else:
                # print("=b , != e")
                if lhs.source == "wowool":
                    wow_.write(
                        f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                    )
                    other_.write(
                        f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                    )
                else:
                    wow_.write(
                        f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                    )
                    other_.write(
                        f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                    )
                idx += 1
        elif lhs.begin_offset < rhs.begin_offset:
            if lhs.source == "wowool":
                wow_.write(
                    f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                )
                other_.write(
                    f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                )
            else:
                wow_.write(
                    f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                )
                other_.write(
                    f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                )
            idx += 1
        else:
            assert False, "Can we realy get here ?????"

    for k, item in cmp_info.items():
        item.close()


def sort_by_offset(lhs: CmpItem, rhs: CmpItem):
    if lhs.begin_offset == rhs.begin_offset:
        if lhs.end_offset == rhs.end_offset:
            if lhs.uri != rhs.uri:
                return lhs.source < rhs.source
            return 0
        return rhs.end_offset - lhs.end_offset
    return lhs.begin_offset - rhs.begin_offset


KEY_IS_DIFFERENT = "?"


class CompareContext:
    def __init__(self):
        self.exclude_missing = None

    def print_tabulate(self, compare_data: dict[str:NlpData]):

        tabel_data = []
        rows = [nlpdata.rows for nlpdata in compare_data.values()]
        for row in zip(*rows):
            ll = row[0]
            item = {
                KEY_IS_DIFFERENT: "",
                "beg": ll.begin_offset,
                "end": ll.end_offset,
                "literal": ll.literal,
                f"uri_{ll.source}": ll.uri,
                f"text_{ll.source}": ll.text,
            }
            missing_in_source = []
            for other_ in row[1:]:
                rl = other_
                if ll.uri != rl.uri:
                    if rl.uri == MISSING:
                        item[KEY_IS_DIFFERENT] += "-"
                        missing_in_source.append(rl.source)
                    elif ll.uri == MISSING:
                        item[KEY_IS_DIFFERENT] += "x"
                        missing_in_source.append(ll.source)
                    else:
                        item[KEY_IS_DIFFERENT] += "!"
                item[f"uri_{rl.source}"] = rl.uri
                item[f"text_{rl.source}"] = rl.text if rl.text else f"({rl.literal})"

            if missing_in_source and item[KEY_IS_DIFFERENT]:
                if self.exclude_missing and self.exclude_missing.match(item["literal"]):
                    ...
                else:
                    for source in missing_in_source:
                        compare_data[source].missing.append(item)

            item.pop("literal")
            tabel_data.append(item)

        if tabel_data:
            # print(*tabel_data, sep="\n")
            print(tabulate(tabel_data, headers="keys", tablefmt="github"))

    def get_text(self, document_text, begin_offset, end_offset):
        return document_text[begin_offset:end_offset]

    def clear_rows(self, compare_data: dict[str, NlpData]):
        for nlpdata in compare_data.values():
            nlpdata.rows.clear()

    def print_md_table(
        self,
        document_text,
        compare_data: dict[str, NlpData],
        cmp_lines: list[list[CmpItem]],
        nlp_name: str,
    ):
        for cmp_line in cmp_lines:
            first = None
            for cmp_item in cmp_line:
                if cmp_item is not None:
                    first = cmp_item
                    break
            if first and first.uri == "Sentence":
                self.print_tabulate(compare_data)
                self.clear_rows(compare_data)
                print(f"\n\n`{first.text}`\n")
                continue

            for cmp_idx, cmp_item in enumerate(cmp_line):
                if cmp_item is not None:
                    uri = cmp_item.uri
                    text = cmp_item.text
                    literal = cmp_item.literal
                    source = cmp_item.source
                else:
                    uri = MISSING
                    text_ = self.get_text(
                        document_text, first.begin_offset, first.end_offset
                    )
                    text = f"*{text_}*"
                    literal = text
                    source = find_source(compare_data, cmp_idx)

                compare_data[source].add_row(
                    uri,
                    first.begin_offset,
                    first.end_offset,
                    text,
                    literal=literal,
                )

        self.print_tabulate(compare_data)
        self.clear_rows(compare_data)

    def compare_entities(
        self,
        compare_data,
        input_provider,
        nlp_engines: list,
        concept_filter: ConceptFilter,
    ):

        wowool_pipeline, other_engines = nlp_engines[0], nlp_engines[1:]
        text = input_provider.text
        for nlp in nlp_engines:
            if nlp.name not in compare_data:
                compare_data[nlp.name] = NlpData(nlp.name, nlp.cmp_idx)

        wowool_: NlpData = compare_data["wowool"]

        offset_data = []
        for nlp in nlp_engines:
            other_: NlpData = compare_data[nlp.name]
            start = time.time()
            doc = nlp(text)
            end = time.time()
            other_.time += end - start
            processing_time = end - start
            logger.info(f"{nlp.name} processing time: {processing_time:.3f}")

            nlp.get_compare_data(other_, doc, concept_filter)
            # print(*other_.data, sep="\n")
            offset_data.extend(other_.data)

        offset_data = sorted(offset_data, key=cmp_to_key(sort_by_offset))

        cmp_lines = insert_missing_comparison_items(offset_data, nlp_engines)

        nlp = other_engines[0]
        # print_rst_table(offset_data, nlp.name)
        self.print_md_table(text, compare_data, cmp_lines, nlp.name)
        # print_diff(offset_data, nlp.name)

        # with open(f"wowool-vs-{nlp.name}-diff.txt", "a") as wfh:
        #     subprocess.run(
        #         ["diff", "-y", "wowool.diff", f"{nlp.name}.diff"], stdout=wfh
        #     )


def get_nlp_engines(nlp_engines: str, language, **kwargs):
    """warming up the engines"""

    # engine_strings = split(",")
    if not nlp_engines.startswith("wowool"):
        nlp_engines = f"wowool,{nlp_engines}"
    engines = []

    for cmp_idx, nlp_name in enumerate(nlp_engines.split(",")):
        start = time.time()
        nlp_engine = get_nlp_engine(cmp_idx, nlp_name, language, **kwargs)
        nlp_engine.warmup()
        engines.append(nlp_engine)
        end = time.time()
        startup_time = end - start
        logger.info(f"{nlp_name} startup time: {startup_time:.3f}")

    return engines


DEFAULT_ANNOTATIONS = [
    "Sentence",
    "ORG",
    "PERSON",
    "GPE",
    "TIME",
    "DATE",
    "MONEY",
    "EVENT",
    "LOC",
]


def get_wowool_annotation_filter(annotations):
    filter_table = set()
    if annotations:
        annotations_ = annotations.split(",")
    else:
        annotations_ = DEFAULT_ANNOTATIONS

    for annotation in annotations_:
        filter_table.add(annotation)

    return ConceptFilter(filter_table)


def cleanup_result_files(nlp_engines: str):
    for name in nlp_engines:
        Path(f"{name}.diff").unlink(missing_ok=True)
        Path(f"missing_in_{name}.csv").unlink(missing_ok=True)


def clear_intermediate_results(compare_data):
    for engine, data in compare_data.items():
        data.data.clear()
        data.counter.clear()
        data.time = 0


def print_timing_results(
    prefix, wowool_time, other_name, other_time, wowool_counter, other_counter
):
    print(f"""\n{prefix} Time: {other_name: <8}: {other_time:.3f} {other_counter}""")
    print(f"""{prefix} Time: {'Wowool':<8}: {wowool_time:.3f} {wowool_counter}""")
    word = "faster than" if wowool_time < other_time else "slower than"
    faster = round(abs((other_time / wowool_time) - 1), 1)

    if faster == 0:
        print(f""" Wowool is is as fast as {other_name}""")
    else:
        print(f""" Wowool is {faster:.3f} {word} {other_name}""")


def write_missing_entities(compare_data):
    for engine, data in compare_data.items():
        with open(f"missing_in_{engine}.csv", "w") as csvfile:
            if data.missing:
                writer = csv.DictWriter(csvfile, fieldnames=data.missing[0].keys())
                writer.writeheader()
                writer.writerows(data.missing)


def compare(nlp_engine: str, language: str, annotations: str, file: str, **kwargs):

    cc = CompareContext()
    exculde_fn = Path(f"config/{language}_exculde.txt")
    if exculde_fn.exists():
        with exculde_fn.open() as fh:
            exclude_missing = set()
            for line in fh:
                line = line.strip()
                if line:
                    exclude_missing.add(line)
            patterns = "|".join(exclude_missing)
            cc.exclude_missing = re.compile(patterns)

    nlp_engines = get_nlp_engines(nlp_engine, language, **kwargs)
    cleanup_result_files(nlp_engines)
    wowool_pipeline, nlp = nlp_engines[0], nlp_engines[1]
    # map_table = nlp.get_mapping_table()
    concept_filter = get_wowool_annotation_filter(annotations)
    files = []
    for fn in file:
        files.extend([fn for fn in Factory.glob(Path(fn))])
    if files:
        compare_data = {"wowool": NlpData("wowool", 0)}
        for ip in files:
            logger.info(f"Process: {ip.id}")
            clear_intermediate_results(compare_data)
            cc.compare_entities(compare_data, ip, nlp_engines, concept_filter)
            for engine, data in compare_data.items():
                data.tt_time += data.time
                data.tt_counter.update(data.counter)

        other_ = compare_data[nlp.name]
        wowool_ = compare_data["wowool"]
        print_timing_results(
            "Total: ",
            wowool_.tt_time,
            other_.name,
            other_.tt_time,
            wowool_.tt_counter,
            other_.tt_counter,
        )

        write_missing_entities(compare_data)

    else:
        raise ValueError(f"File {file} not found")
