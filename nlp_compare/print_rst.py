def print_rst_table(offset_data: list[CmpItem], nlp_name: str):

    size_offset_data = len(offset_data)
    cmp_info = get_filehandels(nlp_name)
    wow_, other_ = cmp_info["wowool"], cmp_info[nlp_name]

    idx = 0
    literal = "literal"

    for k, item in cmp_info.items():
        item.write(f"{'='*30} {'='*30}\n")
        item.write(f"{k:^30} {literal:^30}\n")
        item.write(f"{'='*30} {'='*30}\n")

    while idx < size_offset_data:

        # ic(offset_data[idx])
        lhs = offset_data[idx]

        if lhs.uri == "Sentence":
            wow_.write(f"\n{lhs.text}\n")
            other_.write("\n\n")
            idx += 1
            continue

        if lhs.begin_offset == None:
            idx += 1
            continue

        nidx = get_next_valid_idx(offset_data, size_offset_data, idx)
        if nidx >= size_offset_data or nidx == -1:
            cmp_info[lhs.source].write(
                f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
            )
            # check to write to the other side
            if "wowool" == lhs.source:
                other_.write(
                    f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
                )
            else:
                wow_.write(
                    f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
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
                        f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
                    )
                    cmp_info[rhs.source].write(
                        f"{rhs.uri:<30} ({rhs.begin_offset:<3},{rhs.end_offset:<3}) :{rhs.text}\n"
                    )
                    idx = idx + 2
                else:
                    if lhs.source == "wowool":
                        wow_.write(
                            f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
                        )
                        other_.write(
                            f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
                        )
                    else:
                        wow_.write(
                            f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
                        )
                        other_.write(
                            f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
                        )
                    idx += 1
            else:
                # print("=b , != e")
                if lhs.source == "wowool":
                    wow_.write(
                        f"{lhs.uri:<30}:{lhs.text} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) \n"
                    )
                    other_.write(
                        f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
                    )
                else:
                    wow_.write(
                        f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) \n"
                    )
                    other_.write(
                        f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
                    )
                idx += 1
        elif lhs.begin_offset < rhs.begin_offset:
            if lhs.source == "wowool":
                wow_.write(
                    f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
                )
                other_.write(
                    f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
                )
            else:
                wow_.write(
                    f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
                )
                other_.write(
                    f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
                )
            idx += 1
        else:
            assert False, "Can we realy get here ?????"

    for k, item in cmp_info.items():
        item.write(f"{'='*30} {'='*30}\n")

    for k, item in cmp_info.items():
        item.close()

    with open(f"wowool-vs-{nlp_name}-tbl.txt", "a") as wfh:
        for ll, rl in zip(wow_.lines, other_.lines):
            ll = ll[:-1]
            wfh.write(ll)
            line_length = len(ll)
            while line_length < 62:
                wfh.write(" ")
                line_length += 1
            wfh.write(rl)

    # for k, item in cmp_info.items():
    #     item.write(f"{'='*30} {'='*30}\n")


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
