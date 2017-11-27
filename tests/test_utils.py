from pytest import raises
from app import utils


class TestOffsetRange():
    """
    Tests for utils.offset_range
    """
    def test_neg_total_pos_count_max(self):
        with raises(ValueError):
            next(utils.offset_range(-1, 42))

    def test_zero_total_pos_count_max(self):
        with raises(ValueError):
            next(utils.offset_range(0, 42))

    def test_pos_total_neg_count_max(self):
        with raises(ValueError):
            next(utils.offset_range(42, -1))

    def test_pos_total_zero_count_max(self):
        with raises(ValueError):
            next(utils.offset_range(42, 0))

    def test_pos_total_pos_count_max(self):
        g = utils.offset_range(42, 20)
        assert next(g) == (0, 20)
        assert next(g) == (20, 20)
        assert next(g) == (40, 2)
        with raises(StopIteration):
            next(g)
