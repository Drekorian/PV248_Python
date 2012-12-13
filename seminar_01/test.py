#!/usr/bin/python
import unittest
import ircbot
import state
import copy

class TestShutdown(unittest.TestCase):
    def test_shutdown(self):
        self.assertRaises(SystemExit, ircbot.parse, "SHUTDOWN")


class TestParseCommand(unittest.TestCase):
    def c_shutdown(self, t):
        raise SystemExit

    def c_echo(self, t):
        return state.done("echo "+t)

    def c_unknown(self, t):
        return state.next()

    def c_nothing(self, t):
        return state.done()
    
    def setUp(self):
        self._cmd = copy.copy(ircbot.COMMANDS)
        self._hook = copy.copy(ircbot.FILTERS)
        
        ircbot.COMMANDS = {
            "echo": self.c_echo,
            "SHUTDOWN": self.c_shutdown,
            "nothing": self.c_nothing,
            "unknown": self.c_unknown
		}

        ircbot.FILTERS = []

    def test_shutdown(self):
        self.assertRaises(SystemExit, ircbot.parse, "SHUTDOWN")

    def test_echo(self):
        self.assertEquals("echo bot", ircbot.parse("echo bot"))

    def test_unknown(self):
        self.assertEquals("unknown test", ircbot.parse("unknown test"))

    def test_nothing(self):
        self.assertEquals(None, ircbot.parse("nothing test"))

    def tearDown(self):
        ircbot.COMMANDS = self._cmd
        ircbot.FILTERS = self._hook


class TestParseHooks(unittest.TestCase):
    def c_shutdown(self, t):
        raise SystemExit

    def c_echo(self, t):
        return state.done("echo "+t)

    def h_count(self, t):
        return state.done("%d" % len(t))

    def h_next(self, t):
        return state.next()

    def h_replace(self, t):
        return state.replace("pokusny")
    
    def setUp(self):
        self._cmd = copy.copy(ircbot.COMMANDS)
        self._hook = copy.copy(ircbot.FILTERS)
        
        ircbot.COMMANDS = {
            "echo": self.c_echo,
            "SHUTDOWN": self.c_shutdown
            }

        ircbot.FILTERS = []

    def test_shutdown(self):
        ircbot.FILTERS = []
        self.assertRaises(SystemExit, ircbot.parse, "SHUTDOWN")

    def test_command(self):
        ircbot.FILTERS = []
        self.assertEquals("echo bot", ircbot.parse("echo bot"))

    def test_filter(self):
        ircbot.FILTERS = [self.h_count]
        self.assertEquals("5", ircbot.parse("pocet"))

    def test_next_filter(self):
        ircbot.FILTERS = [self.h_next, self.h_count]
        self.assertEquals("5", ircbot.parse("pocet"))

    def test_replace_filter(self):
        ircbot.FILTERS = [self.h_replace, self.h_count]
        self.assertEquals("7", ircbot.parse("pocet"))

    def tearDown(self):
        ircbot.COMMANDS = self._cmd
        ircbot.FILTERS = self._hook


if __name__ == '__main__':
    unittest.main()
