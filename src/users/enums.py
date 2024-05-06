from enum import StrEnum, auto
from functools import lru_cache


class Role(StrEnum):
    ADMIN = auto()
    SENIOR = auto()
    JUNIOR = auto()

    @classmethod
    @lru_cache(maxsize=1)
    def users(cls) -> list[str]:
        return [cls.SENIOR, cls.JUNIOR]

    @classmethod
    @lru_cache(maxsize=1)
    def users_values(cls) -> list[str]:
        return [cls.SENIOR.value, cls.JUNIOR.value]

    @classmethod
    @lru_cache(maxsize=1)
    def choices(cls) -> list[tuple[str, str]]:
        results = []

        for element in cls:
            _element = (element.value, element.name.lower().capitalize())
            results.append(_element)

        return results
