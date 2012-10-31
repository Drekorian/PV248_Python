import unittest
import ircbot
import state

class TestParseKarma(unittest.TestCase):
	def setUp(self):
		# prepare test environment to start from scratch in each test
		ircbot.KARMA = {}

	def tearDown(self):
		# clean things up
		del ircbot.KARMA

	def test_FOO(self):
		ircbot.parse("foo++")
		self.assertEqual(ircbot.KARMA["foo"], 1)
		self.assertTrue("foo" in ircbot.KARMA)
		self.assertRaises(KeyError, ircbot.KARMA.__getitem__, "bar")

class TestCalc(unittest.TestCase):
	def test_not_math(self):
		self.assertTrue(state.is_next(ircbot.cmd_calc("foo +1")))

	def test_single_positive_number(self):
		self.assertTrue(state.is_done(ircbot.cmd_calc("1")))
		self.assertEquals(ircbot.cmd_calc("1").value, "1")

	def test_single_negative_number(self):
		self.assertTrue(state.is_done(ircbot.cmd_calc("-1")))
		self.assertEqual(ircbot.cmd_calc("-1").value, "-1")

	def test_addition(self):
		self.assertTrue(state.is_done(ircbot.cmd_calc("1 + 1")))
		self.assertEqual(ircbot.cmd_calc("1 + 1").value, "2")
		self.assertTrue(state.is_done(ircbot.cmd_calc("-1 + 1")))
		self.assertEqual(ircbot.cmd_calc("-1 + 1").value, "0")

	def test_subtraction(self):
		self.assertTrue(state.is_done(ircbot.cmd_calc("1 - 1")))
		self.assertEqual(ircbot.cmd_calc("1 - 1").value, "0")

	def test_multiplication(self):
		self.assertTrue(state.is_done(ircbot.cmd_calc("1 * 1")))
		self.assertEqual(ircbot.cmd_calc("1 * 1").value, "1")

	def test_division(self):
		self.assertTrue(state.is_done(ircbot.cmd_calc("1 / 1")))
		self.assertEqual(ircbot.cmd_calc("1 / 1").value, "1")

		self.assertTrue(state.is_next(ircbot.cmd_calc("1 / 0")))
		self.assertEqual(ircbot.cmd_calc("1 / 0").value, "1 / 0")

if __name__ == '__main__':
	unittest.main()