import unittest
from hamcrest import assert_that, equal_to, greater_than, less_than, all_of

from moderation import strategies


def between(lower_bound, upper_bound):
    return all_of(
        greater_than(lower_bound),
        less_than(upper_bound),
    )


class TestFibonacci(unittest.TestCase):
    def setUp(self):
        self.sequence = strategies.fibonacci()

    def test_run(self):
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), equal_to(1))
        assert_that(next(self.sequence), equal_to(1))
        assert_that(next(self.sequence), equal_to(2))
        assert_that(next(self.sequence), equal_to(3))
        assert_that(next(self.sequence), equal_to(5))

    def test_reset(self):
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), equal_to(1))
        assert_that(next(self.sequence), equal_to(1))
        strategies.reset(self.sequence)
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), equal_to(1))
        assert_that(next(self.sequence), equal_to(1))

    def test_double_reset(self):
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), equal_to(1))
        assert_that(next(self.sequence), equal_to(1))
        strategies.reset(self.sequence)
        strategies.reset(self.sequence)
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), equal_to(1))
        assert_that(next(self.sequence), equal_to(1))


class TestLinear(unittest.TestCase):
    def setUp(self):
        self.sequence = strategies.linear()

    def test_run(self):
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), equal_to(1))
        assert_that(next(self.sequence), equal_to(2))
        assert_that(next(self.sequence), equal_to(3))
        assert_that(next(self.sequence), equal_to(4))
        assert_that(next(self.sequence), equal_to(5))

    def test_reset(self):
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), equal_to(1))
        strategies.reset(self.sequence)
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), equal_to(1))

    def test_double_reset(self):
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), equal_to(1))
        strategies.reset(self.sequence)
        strategies.reset(self.sequence)
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), equal_to(1))


class TestExponential(unittest.TestCase):
    def setUp(self):
        self.sequence = strategies.exponential(2)

    def test_run(self):
        assert_that(next(self.sequence), equal_to(1))
        assert_that(next(self.sequence), equal_to(2))
        assert_that(next(self.sequence), equal_to(4))
        assert_that(next(self.sequence), equal_to(8))
        assert_that(next(self.sequence), equal_to(16))
        assert_that(next(self.sequence), equal_to(32))

    def test_reset(self):
        assert_that(next(self.sequence), equal_to(1))
        assert_that(next(self.sequence), equal_to(2))
        strategies.reset(self.sequence)
        assert_that(next(self.sequence), equal_to(1))
        assert_that(next(self.sequence), equal_to(2))

    def test_double_reset(self):
        assert_that(next(self.sequence), equal_to(1))
        assert_that(next(self.sequence), equal_to(2))
        strategies.reset(self.sequence)
        strategies.reset(self.sequence)
        assert_that(next(self.sequence), equal_to(1))
        assert_that(next(self.sequence), equal_to(2))


class TestTransform(unittest.TestCase):
    def setUp(self):
        self.sequence = strategies.transform(strategies.linear(), str)

    def test_run(self):
        assert_that(next(self.sequence), equal_to("0"))
        assert_that(next(self.sequence), equal_to("1"))
        assert_that(next(self.sequence), equal_to("2"))
        assert_that(next(self.sequence), equal_to("3"))

    def test_reset(self):
        assert_that(next(self.sequence), equal_to("0"))
        assert_that(next(self.sequence), equal_to("1"))
        strategies.reset(self.sequence)
        assert_that(next(self.sequence), equal_to("0"))
        assert_that(next(self.sequence), equal_to("1"))

    def test_double_reset(self):
        assert_that(next(self.sequence), equal_to("0"))
        assert_that(next(self.sequence), equal_to("1"))
        strategies.reset(self.sequence)
        strategies.reset(self.sequence)
        assert_that(next(self.sequence), equal_to("0"))
        assert_that(next(self.sequence), equal_to("1"))


class TestQuickTransform(unittest.TestCase):
    def setUp(self):
        self.sequence = strategies.qt(strategies.linear())

    def test_run(self):
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), between(1 * 0.9, 1 * 1.1))
        assert_that(next(self.sequence), between(2 * 0.9, 2 * 1.1))

    def test_reset(self):
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), between(1 * 0.9, 1 * 1.1))
        strategies.reset(self.sequence)
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), between(1 * 0.9, 1 * 1.1))

    def test_double_reset(self):
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), between(1 * 0.9, 1 * 1.1))
        strategies.reset(self.sequence)
        strategies.reset(self.sequence)
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), between(1 * 0.9, 1 * 1.1))


class TestPower(unittest.TestCase):
    def setUp(self):
        self.sequence = strategies.transform(strategies.linear(), strategies.power(3))

    def test_run(self):
        assert_that(next(self.sequence), equal_to(0))
        assert_that(next(self.sequence), equal_to(1))
        assert_that(next(self.sequence), equal_to(8))
