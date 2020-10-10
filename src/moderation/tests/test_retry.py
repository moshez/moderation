import unittest
from hamcrest import assert_that, equal_to, empty, calling, raises
from unittest import mock

from moderation import retry, strategies


class TestRetries(unittest.TestCase):

    def setUp(self):
        self.func = mock.MagicMock(name="function")
        self.sleeper = mock.MagicMock(name="time.sleep")
        self.backoff = strategies.linear()

    def test_succeed_on_first_try(self):
        self.func.side_effect = [42]
        retrier = retry.retry(
            sleeper=self.sleeper,
            backoff=self.backoff,
            retries=3,
            exceptions=[Exception],
        )(self.func)
        result = retrier("life")
        assert_that(result, equal_to(42))
        assert_that(self.func.call_count, equal_to(1))
        [[what], kwargs] = self.func.call_args
        assert_that(kwargs, empty())
        assert_that(what, equal_to("life"))

    def test_succeed_on_fourth_try(self):
        self.func.side_effect = [ValueError(), KeyError(), KeyError(), 42]
        retrier = retry.retry(
            sleeper=self.sleeper,
            backoff=self.backoff,
            retries=4,
            exceptions=[Exception],
        )(self.func)
        result = retrier("life")
        assert_that(result, equal_to(42))
        assert_that(self.func.call_count, equal_to(4))
        [[what], kwargs] = self.func.call_args
        assert_that(kwargs, empty())
        assert_that(what, equal_to("life"))
        for thing in self.sleeper.call_args_list:
            [[duration], kwargs] = thing
            assert_that(duration, equal_to(next(self.backoff)))

    def test_fail(self):
        self.func.side_effect = KeyError()
        retrier = retry.retry(
            sleeper=self.sleeper,
            backoff=self.backoff,
            retries=4,
            exceptions=[Exception],
        )(self.func)
        assert_that(calling(retrier).with_args("life"), raises(KeyError))
        assert_that(self.func.call_count, equal_to(4))
        [[what], kwargs] = self.func.call_args
        assert_that(kwargs, empty())
        assert_that(what, equal_to("life"))
        strategies.reset(self.backoff)
        for thing in self.sleeper.call_args_list:
            [[duration], kwargs] = thing
            assert_that(duration, equal_to(next(self.backoff)))
