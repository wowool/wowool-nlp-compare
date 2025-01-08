from dataclasses import dataclass


@dataclass
class CmpItem:
    cmp_idx: int
    begin_offset: int
    end_offset: int
    source: str
    uri: str
    text: str
    literal: str | None = None


class NLPEngine:
    def __init__(self, cmp_idx: int):
        self.cmp_idx = cmp_idx
