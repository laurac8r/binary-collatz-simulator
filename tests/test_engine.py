import pytest

from src.binary_collatz.engine import iterate


class TestIterate:
    @pytest.mark.parametrize("n, lgt, peak", [(27, 111, 9232), (6, 8, 16), (1, 0, 0)])
    def test_accurate_num_and_peak(self, n, lgt, peak):
        steps = []

        step = n

        for step in iterate(step):
            steps.append(step)

        assert len(steps) == lgt
        if lgt > 0:
            assert max([x.value for x in steps]) == peak
