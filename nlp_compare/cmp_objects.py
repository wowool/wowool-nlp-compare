from dataclasses import dataclass, field


@dataclass
class CmpItem:
    begin_offset: int
    end_offset: int
    source: str
    uri: str
    text: str
    literal: str | None = None
