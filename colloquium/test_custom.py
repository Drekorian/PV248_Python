#!/usr/bin/python
import unittest
import re
import ircbot
import interface
import plugins
from plugins import state


class TestCmdShutdown(unittest.TestCase):
	def test_cmd_shutdown_empty(self):
		with self.assertRaises(SystemExit):
			plugins.shutdown.cmd_shutdown()

	def test_cmd_shutdown_with_argument(self):
		with self.assertRaises(SystemExit):
			plugins.shutdown.cmd_shutdown("message")


class TestCmdCalc(unittest.TestCase):
	def test_not_math(self):
		self.assertTrue(state.is_next(calculator.cmd_calc("foo +1")))

	def test_single_positive_number(self):
		self.assertTrue(state.is_done(calculator.cmd_calc("1")))
		self.assertEquals(calculator.cmd_calc("1").value, "1")

	def test_single_positive_number_float(self):
		self.assertTrue(state.is_done(calculator.cmd_calc("1.0")))
		self.assertEquals(calculator.cmd_calc("1.0").value, "1.0")

	def test_single_negative_number(self):
		self.assertTrue(state.is_done(calculator.cmd_calc("-1")))
		self.assertEqual(calculator.cmd_calc("-1").value, "-1")

	def test_single_negative_number_float(self):
		self.assertTrue(state.is_done(calculator.cmd_calc("-1.0")))
		self.assertEqual(calculator.cmd_calc("-1.0").value, "-1.0")

	def test_addition(self):
		self.assertTrue(state.is_done(calculator.cmd_calc("1 + 1")))
		self.assertEqual(calculator.cmd_calc("1 + 1").value, "2")
		self.assertTrue(state.is_done(calculator.cmd_calc("-1 + 1")))
		self.assertEqual(calculator.cmd_calc("-1 + 1").value, "0")
		self.assertTrue(state.is_done(calculator.cmd_calc("0.5 + 0.5")))
		self.assertEqual(calculator.cmd_calc("0.5 + 0.5").value, "1.0")

	def test_subtraction(self):
		self.assertTrue(state.is_done(calculator.cmd_calc("1 - 1")))
		self.assertEqual(calculator.cmd_calc("1 - 1").value, "0")
		self.assertTrue(state.is_done(calculator.cmd_calc("-1 - 1")))
		self.assertEqual(calculator.cmd_calc("-1 - 1").value, "-2")
		self.assertTrue(state.is_done(calculator.cmd_calc("0.6 - 0.5")))
		self.assertEqual(calculator.cmd_calc("0.6 - 0.5").value, "0.1")

	def test_multiplication(self):
		self.assertTrue(state.is_done(calculator.cmd_calc("1 * 1")))
		self.assertEqual(calculator.cmd_calc("1 * 1").value, "1")
		self.assertTrue(state.is_done(calculator.cmd_calc("-1 * 1")))
		self.assertEqual(calculator.cmd_calc("-1 * 1").value, "-1")
		self.assertTrue(state.is_done(calculator.cmd_calc("0.1 * 0.1")))
		self.assertEqual(calculator.cmd_calc("0.1 * 0.1").value, "0.01")

	def test_division(self):
		self.assertTrue(state.is_done(calculator.cmd_calc("1 / 1")))
		self.assertEqual(calculator.cmd_calc("1 / 1").value, "1")
		self.assertTrue(state.is_done(calculator.cmd_calc("1 / 2")))
		self.assertEqual(calculator.cmd_calc("1 / 2").value, "0")
		self.assertTrue(state.is_done(calculator.cmd_calc("1.0 / 2")))
		self.assertEqual(calculator.cmd_calc("1.0 / 2").value, "0.5")

	def test_division_by_zero(self):
		self.assertTrue(state.is_next(calculator.cmd_calc("1 / 0")))
		self.assertEqual(calculator.cmd_calc("1 / 0").value, "1 / 0")
		self.assertTrue(state.is_next(calculator.cmd_calc("1.0 / 0")))
		self.assertEqual(calculator.cmd_calc("1.0 / 0").value, "1.0 / 0")

	def test_correct_parenthesis(self):
		self.assertTrue(state.is_done(calculator.cmd_calc("2 * (1 + 2)")))
		self.assertEqual(calculator.cmd_calc("2 * (1 + 2)").value, "6")

	def test_incorrect_parenthesis(self):
		self.assertTrue(state.is_next(calculator.cmd_calc("2 * ((1 + 2)")))
		self.assertEqual(calculator.cmd_calc("2 * ((1 + 2)").value, "2 * ((1 + 2)")

	def test_none(self):
		self.assertTrue(state.is_next(calculator.cmd_calc(None)))


class TestCmdWordCount(unittest.TestCase):
	def setUp(self):
		plugins.wordcount.WORDCOUNT = 0

	def tearDown(self):
		plugins.wordcount.WORDCOUNT = 0

	def test_default(self):
		self.assertTrue(state.is_done(plugins.wordcount.cmd_word_count()))
		self.assertEqual(plugins.wordcount.cmd_word_count(None).value, 'Actual word count is ' + str(plugins.wordcount.WORDCOUNT) + ' words.')

	def test_custom(self):
		plugins.wordcount.WORDCOUNT = 5
		self.assertEqual(plugins.wordcount.WORDCOUNT, 5)
		self.assertTrue(state.is_done(plugins.wordcount.cmd_word_count()))
		self.assertEqual(plugins.wordcount.cmd_word_count(None).value, 'Actual word count is ' + str(plugins.wordcount.WORDCOUNT) + ' words.')


class TestCmdKarma(unittest.TestCase):
	def setUp(self):
		plugins.karma.KARMA = {}

	def tearDown(self):
		plugins.karma.KARMA = {}

	def test_default(self):
		self.assertTrue(state.is_done(plugins.karma.cmd_karma('foo')))
		self.assertEqual(plugins.karma.cmd_karma('foo').value, "'foo' has no karma.")
		plugins.karma.KARMA = { 'foo': 5 }
		self.assertTrue(state.is_done(plugins.karma.cmd_karma('foo')))
		self.assertEqual(plugins.karma.cmd_karma('foo').value, "'foo' has 5 points of karma.")


class TestFWordCount(unittest.TestCase):
	def setUp(self):
		plugins.wordcount.WORDCOUNT = 0

	def tearDown(self):
		plugins.wordcount.WORDCOUNT = 0

	def test_single(self):
		old_count = plugins.wordcount.WORDCOUNT
		self.assertTrue(state.is_next(plugins.wordcount.f_word_count('foo')))
		self.assertEqual(plugins.wordcount.WORDCOUNT, old_count + 1)

	def test_double(self):
		old_count = plugins.wordcount.WORDCOUNT
		self.assertTrue(state.is_next(plugins.wordcount.f_word_count('foo bar')))
		self.assertEqual(plugins.wordcount.WORDCOUNT, old_count + 2)

	def test_triple(self):
		old_count = plugins.wordcount.WORDCOUNT
		self.assertTrue(state.is_next(plugins.wordcount.f_word_count('foo bar baz')))
		self.assertEqual(plugins.wordcount.WORDCOUNT, old_count + 3)


class TestFKarma(unittest.TestCase):
	def setUp(self):
		plugins.karma.KARMA = {}

	def tearDown(self):
		plugins.karma.KARMA = {}

	def test_plus_plus(self):
		self.assertTrue(state.is_next(plugins.karma.f_karma('foo++')))
		self.assertEqual(plugins.karma.KARMA['foo'], 1)

	def test_minus_minus(self):
		self.assertTrue(state.is_next(plugins.karma.f_karma('bar--')))
		self.assertEqual(plugins.karma.KARMA['bar'], -1)

	def test_delete_zero(self):
		self.assertFalse(plugins.karma.KARMA.has_key("baz"))
		plugins.karma.f_karma("baz++")
		self.assertTrue(plugins.karma.KARMA.has_key("baz"))
		plugins.karma.f_karma("baz--")
		self.assertFalse(plugins.karma.KARMA.has_key("baz"))


class TestFLogging(unittest.TestCase):
	def test_default(self):
		log_name = "test.log"
		log_file = open(log_name, "w")
		log_file.close()

		plugins.local_logging.f_logging("foo", log_name)

		log_file = open(log_name, "r")
		log_data = log_file.read()
		log_file.close()

		pattern = "\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}  foo"

		if not(re.match(pattern, log_data)):
			self.fail()


class TestBotInterface(unittest.TestCase):
	def setUp(self):
		self._ifc = interface.IRCBotShellInterface()
		self._bot = ircbot.IrcBot(self._ifc)

	def test_read(self):
		self.assertEqual(self._bot._if.read(lambda(prompt): "foo"), "foo")

	def test_write_default(self):
		self.assertEqual(self._bot._if.write("foo"), None)

	def test_write_dummy(self):
		self.assertEqual(self._bot._if.write("foo", lambda(arg): arg), "foo")


class TestIrcBot(unittest.TestCase):
	def setUp(self):
		self._bot = ircbot.IrcBot(interface.IRCBotShellInterface())

		self._bot.COMMANDS = {
			'hello': self.cmd_say_hello
		}

		self._bot.FILTERS = [self.f_replace_secret_with_hashes]
		self._bot.KARMA = {}

	def tearDown(self):
		self.bot = ircbot.IrcBot(interface.IRCBotShellInterface())

	def cmd_say_hello(self, msg = None):
		return state.done("hello to you too")

	def f_replace_secret_with_hashes(self, msg):
		replaced = msg.replace("secret", "######")

		if msg != replaced:
			return state.replace(replaced)

		return state.next(msg)

	def test_parse_hello(self):
		self.assertEqual(self._bot.parse("hello"), "hello to you too")

	def test_parse_secret(self):
		self.assertEqual(self._bot.parse("the secret is secret"), "the ###### is ######")
		self.assertEqual(self._bot.parse("foo bar"), "foo bar")

	def test_parse_no_command_no_filter(self):
		self.assertEqual(self._bot.parse("foo"), "foo")


class TestIsDone(unittest.TestCase):
	def test_done(self):
		self.assertTrue(state.is_done(state.done(None)))

	def test_not_done(self):
		self.assertFalse(state.is_done(state.replace(None)))
		self.assertFalse(state.is_done(state.next(None)))

	def test_not_state(self):
		self.assertFalse(state.is_done(object()))


class TestIsReplace(unittest.TestCase):
	def test_replace(self):
		self.assertTrue(state.is_replace(state.replace(None)))

	def test_not_replace(self):
		self.assertFalse(state.is_replace(state.done(None)))
		self.assertFalse(state.is_replace(state.next(None)))

	def test_not_state(self):
		self.assertFalse(state.is_replace(object()))


class TestIsNext(unittest.TestCase):
	def test_next(self):
		self.assertTrue(state.is_next(state.next(None)))

	def test_not_next(self):
		self.assertFalse(state.is_next(state.done(None)))
		self.assertFalse(state.is_next(state.replace(None)))

	def test_not_state(self):
		self.assertFalse(state.is_next(object()))


if __name__ == "__main__":
	unittest.main()
