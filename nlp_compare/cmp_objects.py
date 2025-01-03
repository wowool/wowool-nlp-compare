from dataclasses import dataclass


@dataclass
class CmpItem:
    begin_offset: int
    end_offset: int
    source: str
    uri: str
    text: str
