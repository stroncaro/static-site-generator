import functools
from typing import Iterable


def all_true(bools: Iterable[bool]) -> bool:
    return functools.reduce(lambda a, b: a and b, bools, True)
