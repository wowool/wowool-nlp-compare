from dataclasses import dataclass


@dataclass
class CmpItem:
    cmp_idx: int
    begin_offset: int
    end_offset: int
    source: str
    uri: str | None = None
    text: str | None = None
    literal: str | None = None
    original_uri: str | None = None


class NLPEngine:
    def __init__(self, cmp_idx: int):
        self.cmp_idx = cmp_idx


@dataclass
class GoldenIem:
    begin_offset: int
    end_offset: int
    literal: str | None = None
    uri: str | None = None


@dataclass
class PrecisionRecallData:
    true_positive: int = 0
    false_positive: int = 0
    false_negative: int = 0
