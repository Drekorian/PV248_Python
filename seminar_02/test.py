#!/usr/bin/python

import unittest
import ircbot
import state
import copy

class TestParseKarma(unittest.TestCase):
	def setUp(self):
		ifc = ircbot.BotInterface()
		self.bot = ircbot.IrcBot(ifc)
		ircbot.KARMA = {}

	def test_plus(self):
		self.bot.parse("foo++")
		self.bot.parse("foo++")
		self.assertEqual(ircbot.KARMA.get("foo"), 2)

	def test_minus(self):
		ircbot.KARMA["foo"] = 2
		self.bot.parse("foo--")
		self.assertEqual(ircbot.KARMA.get("foo"), 1)

	def test_minus_zero(self):
		ircbot.KARMA["foo"] = 1
		self.bot.parse("foo--")
		self.assertEqual(ircbot.KARMA.get("foo"), None)

	def test_cpp(self):
		self.bot.parse("c++++")
		self.assertEqual(ircbot.KARMA.get("c++"), 1)
		self.bot.parse("c++--")
		self.assertEqual(ircbot.KARMA.get("c++"), None)

	def test_middle_line_plus(self):
		self.bot.parse("a b c d++ e")
		self.assertEqual(ircbot.KARMA.get("a b c d"), None)
		self.assertEqual(ircbot.KARMA.get("d"), 1)

	def test_middle_line_minus(self):
		ircbot.KARMA["d"] = 1
		self.bot.parse("a b c d--")
		self.assertEqual(ircbot.KARMA.get("a b c d"), None)
		self.assertEqual(ircbot.KARMA.get("d"), None)

	def test_get(self):
		self.bot.parse("foo++")
		msg = self.bot.parse("karma foo")
		self.assertEqual(msg, "'foo' has 1 points of karma.")

	def test_get_zero(self):
		msg = self.bot.parse("karma foo")
		self.assertEqual(msg, "'foo' has no karma.")


class TestShutdown(unittest.TestCase):
	def setUp(self):
		ifc = ircbot.BotInterface()
		self.bot = ircbot.IrcBot(ifc)

	def test_shutdown(self):
		self.assertRaises(SystemExit, self.bot.parse, "SHUTDOWN")


class TestParseCommand(unittest.TestCase):
	def c_shutdown(self, t):
		raise SystemExit

	def c_echo(self, t):
		return state.done("echo " + t)

	def c_unknown(self, t):
		return state.next()

	def c_nothing(self, t):
		return state.done()

	def setUp(self):
		ifc = ircbot.BotInterface()
		self.bot = ircbot.IrcBot(ifc)
		self._cmd = copy.copy(self.bot.COMMANDS)
		self._hook = copy.copy(self.bot.FILTERS)

		self.bot.COMMANDS = {
			"echo": self.c_echo,
			"SHUTDOWN": self.c_shutdown,
			"nothing": self.c_nothing,
			"unknown": self.c_unknown
		}

		self.bot.FILTERS = []

	def test_shutdown(self):
		self.assertRaises(SystemExit, self.bot.parse, "SHUTDOWN")

	def test_spaces(self):
		self.assertRaises(SystemExit, self.bot.parse, "SHUTDOWN   ")

	def test_CR(self):
		self.assertRaises(SystemExit, self.bot.parse, "SHUTDOWN\r")

	def test_echo(self):
		self.assertEquals("echo bot", self.bot.parse("echo bot"))

	def test_unknown(self):
		self.assertEquals("unknown test", self.bot.parse("unknown test"))

	def test_nothing(self):
		self.assertEquals(None, self.bot.parse("nothing test"))

	def tearDown(self):
		self.bot.COMMANDS = self._cmd
		self.bot.FILTERS = self._hook


class TestParseHooks(unittest.TestCase):
	def c_shutdown(self, t):
		raise SystemExit

	def c_echo(self, t):
		return state.done("echo " + t)

	def h_count(self, t):
		return state.done("%d" % len(t))

	def h_next(self, t):
		return state.next()

	def h_replace(self, t):
		return state.replace("pokusny")

	def setUp(self):
		ifc = ircbot.BotInterface()
		self.bot = ircbot.IrcBot(ifc)
		self._cmd = copy.copy(self.bot.COMMANDS)
		self._hook = copy.copy(self.bot.FILTERS)

		self.bot.COMMANDS = {
			"echo": self.c_echo,
			"SHUTDOWN": self.c_shutdown
		}

		self.bot.FILTERS = []

	def test_shutdown(self):
		self.bot.FILTERS = []
		self.assertRaises(SystemExit, self.bot.parse, "SHUTDOWN")

	def test_command(self):
		self.bot.FILTERS = []
		self.assertEquals("echo bot", self.bot.parse("echo bot"))

	def test_filter(self):
		self.bot.FILTERS = [self.h_count]
		self.assertEquals("5", self.bot.parse("pocet"))

	def test_next_filter(self):
		self.bot.FILTERS = [self.h_next, self.h_count]
		self.assertEquals("5", self.bot.parse("pocet"))

	def test_replace_filter(self):
		self.bot.FILTERS = [self.h_replace, self.h_count]
		self.assertEquals("7", self.bot.parse("pocet"))

	def tearDown(self):
		self.bot.COMMANDS = self._cmd
		self.bot.FILTERS = self._hook


if __name__ == '__main__':
	unittest.main()
