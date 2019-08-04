from enum import Enum
from typing import Tuple


class ExtendedEnum(Enum):
    @classmethod
    def to_choices(cls) -> Tuple[Tuple[str, str], ...]:
        return tuple((tag.name, str(tag.value)) for tag in cls)

    @classmethod
    def from_str(cls, s: str, upper_case=True, raise_on_fail=False):
        try:
            return cls[s.upper() if upper_case else s]
        except KeyError:
            if raise_on_fail:
                raise ValueError(f'{cls} have no tag with name {s}')
            return None
