from binary_collatz.render import sparkline
import pytest

from src.binary_collatz.render import cells


class TestCells:
    @pytest.mark.parametrize(
        "value, width, expected", [(26, 5, "██·█·"), (41, 6, "█·█··█"), (1, 5, "    █")]
    )
    def test_renders_cells_correctly(self, value, width, expected):
        actual = cells(value, width)
        assert actual == expected


class TestSparkline:
    @pytest.mark.parametrize(
        "values, log, expected", [([*range(1, 9)], False, "▁▂▃▄▅▆▇█")]
    )
    def test_renders_sparkline_correctly(self, values, log, expected):
        actual = sparkline(values=values, log=log)
        assert actual == expected
