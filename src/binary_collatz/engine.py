from copy import copy
from dataclasses import dataclass
from enum import Enum


class Op(Enum):
    EVEN = 'n → n // 2'
    ODD = 'n → 3 * n + 1'


@dataclass(frozen=True)
class Step:
    index: int
    value: int
    op: Op | None
    bits: str


def iterate(n: int):
    step = Step(0, copy(n), None, '')
    while step.value != 1:
        num = 0
        op = None
        if step.value % 2 == 1:
            num = 3 * step.value + 1
            op = Op.ODD
        elif step.value % 2 == 0:
            num = step.value // 2
            op = Op.EVEN
        step = Step(step.index + 1, num, op, f'{num:b}')
        yield step


@dataclass(frozen=True)
class Summary:
    total_steps: int
    peak: int
    peak_step: int


def summarize(n: int):
    pass
