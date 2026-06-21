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

    @classmethod
    def iterate(cls, prior: "Step") -> "Step":
        num = 0
        op = None
        if prior.value % 2 == 1:
            num = 3 * prior.value + 1
            op = Op.ODD
        elif prior.value % 2 == 0:
            num = prior.value // 2
            op = Op.EVEN
        return cls(prior.index + 1, num, op, f'{num:b}')



def iterate(n: int):
    step = Step(0, copy(n), None, '')
    yield step
    while step.value != 1:
        step = Step.iterate(step)
        yield step


@dataclass(frozen=True)
class Summary:
    total_steps: int
    peak: int
    peak_step: int


def summarize(n: int):
    pass
