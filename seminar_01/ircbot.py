#!/usr/bin/python

"""
This module is a mockup of a IRC bot. When executed, it runs an endless loop
that can be interrupted with EOF keystroke or interrupt keystroke. Bot is
capable of handling commands and filters.

@author: Marek Osvald
@version: 2012.1214
@since: 2012.0921

@undocumented: __package__
"""
from __future__ import print_function
import re
import state
import sys


KARMA = {} #: Global dictionary for storing users' karma

def cmd_shutdown(msg = None):
	"""
	Raises SystemExit exception.

	@param msg: message associated with the command
	@type msg: str
	@return: None
	@rtype: None
	@raise SystemException: every time
	"""
	raise SystemExit("Shutdown command called")


def cmd_calc(exp):
	"""
	Calculates mathematical expression and returns a state with the result.

	@param exp: expression to be calculated
	@type exp: str
	@return: result of the expression
	@rtype: state.done|state.next
	"""
	if exp is None:
		return state.next(exp)

	pattern = "\(?\-?\d*.?\d+(\s*[\+\-\*\/]\(*\s*\d*.?\d+\)*)*\)?"

	if re.match(pattern, exp):
		try:
			return state.done(str(eval(exp))) # exp IS VALID math expression
		except (SyntaxError, ZeroDivisionError):
			return state.next(exp) # exp IS NOT VALID math expression

	return state.next(exp) # exp contains non-mathematical symbols


def cmd_word_count(msg = None):
	"""
	Returns the number of received words so far.

	@param msg: message associated with the command
	@type msg: str
	@return: "state withe the message 'Actual word count is <number> words'
	@rtype: state.done
	"""
	global WORDCOUNT

	return state.done("Actual word count is %d words." % WORDCOUNT)


def cmd_karma(user):
	"""
	Returns a state with number of karma points for given user.

	@param user: user whose karma is queried
	@type user: str
	@return: done state with message '<user> has <number> points of karma' or
	next statement with message '<user> has no karma'
	@rtype: state.next|state.done
	"""
	global KARMA

	if user == "":
		return state.next("karma")

	user = user.lower()

	if user not in KARMA:
		return state.done("'%s' has no karma." % user)

	return state.done("'%s' has %d points of karma." % (user, KARMA[user]))


COMMANDS = {
	"SHUTDOWN":   cmd_shutdown,
	"calc":       cmd_calc,
	"word-count": cmd_word_count,
	"karma":      cmd_karma,
} #: Global dictionary for storing commands


WORDCOUNT = 0 #: Global variable for storing the number of received words


def f_word_count(msg):
	"""
	Filter that adds the number of words in processed message.

	@param msg: message to be parsed
	@type msg: str
	@return next state with the original message
	@rtype: state.next
	"""
	global WORDCOUNT

	WORDCOUNT += len(msg.split(" "))
	return state.next(msg)


def f_karma(msg):
	"""
	Checks the message for sequence 'something++' and 'something--', if found,
	it calls the change_karma function. Depending whether the command is valid,
	returns either done state or next state with appropriate message.

	@param msg: message to be filtered
	@type msg: str
	@return: done state if the information is done parsing or next state if
	the information is not parseable
	@rtype: state.next|state.done
	"""
	global KARMA

	msg = msg.strip().lower()

	if msg == "c++":
		return state.next(msg)

	if msg.endswith("++") or msg.endswith("--"):
		user = msg[:-2].lower()
		action = msg[-2:]

		if user == "":
			return state.next(msg)

		changes = { "++": "increased", "--": "decreased" }

		KARMA.setdefault(user, 0)

		if action == "++":
			KARMA[user] += 1
		else:
			KARMA[user] -= 1

		if KARMA[user] == 0:
			del KARMA[user]

		return state.done(user + "'s karma was " + changes[action] + " by 1.")

FILTERS = [f_word_count, f_karma] #: Global array for storing the filters


def read(read_function = raw_input):
	"""
	Reads input and returns it.

	@param read_function: function to use for input (mainly for testing purposes
	)
	@type read_function: function
	@return: read data
	@rtype: str
	"""
	return read_function("> ")


def write(arg, write_function = print):
	"""
	Write (send) argument to output.

	@param arg: text to be written to the output
	@type arg: str
	@param write_function: function to user for writing (mainly for testing
	purposes)
	@type write_function: function
	@return: None
	@rtype: None
	"""
	return write_function(arg)


def parse(msg):
	"""
	Parses given input.

	@param msg: input message to parse
	@type msg: str
	@return: return message processed with associated commands and filters
	@rtype: str
	"""
	try:
		cmd, args = msg.split(" ", 1)
	except ValueError:
		cmd, args = msg.rstrip(), ""

	if cmd in COMMANDS:
		ret = COMMANDS[cmd](args)

		if state.is_done(ret):
			return ret.value
		elif state.is_next(ret):
			pass
		else:
			raise Exception("Illegal state of command.")

	for filter in FILTERS:
		ret = filter(msg)

		if state.is_done(ret):
			return ret.value

		if state.is_replace(ret):
			msg = ret.value

	return msg


if __name__ == "__main__":
	while True:
		try:
			msg = read()
			write(parse(msg))

		except (KeyboardInterrupt, EOFError, SystemExit):
			print("Shutting down the bot")
			sys.exit(0)
