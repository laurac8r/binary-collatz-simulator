import pytest  # ty:ignore[unresolved-import]

from src.binary_collatz.render import cells


class TestCells:
    @pytest.mark.parametrize(
        "value, width, expected", [(26, 5, "██·█·"), (41, 6, "█·█··█")]
    )
    def test_renders_cells_correctly(self, value, width, expected):
        actual = cells(value, width)
        assert actual == expected
