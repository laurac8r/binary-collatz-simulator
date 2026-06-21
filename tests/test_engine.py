from src.binary_collatz.engine import iterate


class TestIterate:
    def test_27_returns_111_steps_9232_peak(self):
        steps = []

        step = 27

        for step in iterate(step):
            steps.append(step)

        assert len(steps) == 111
        assert max([x.value for x in steps]) == 9232