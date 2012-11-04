#!/usr/bin/python

"""
This module is a mockup of a IRC bot. When executed, it runs an endless loop
that can be interrupted with EOF keystroke or interrupt keystroke. Bot is
capable of handling commands and filters.

@author: Marek Osvald
@version: 2012.1101
@since: 2012.0921

@undocumented: __package__
"""

import re
import state

KARMA = {} #: Global dictionary for storing users' karma

def cmd_shutdown(msg):
	"""
	Raises SystemExit exception.

	@param msg: message associated with the command
	@return: None
	@rtype: None
	@raise SystemException: every time
	"""
	raise SystemExit

def cmd_calc(exp):
	"""
	Calculates mathematical expression and returns a state with the result.

	@param exp: expression to be calculated
	@return: result of the expression
	@rtype: state
	"""
	pattern = "\(?\-?\d*.?\d+(\s*[\+\-\*\/]\(*\s*\d*.?\d+\)*)*\)?"

	if re.match(pattern, exp):
		try:
			return state.done(str(eval(exp))) # exp IS VALID math expression
		except (SyntaxError, ZeroDivisionError):
			return state.next(exp) # exp IS NOT VALID math expression

	return state.next(exp) # exp contains non-mathematical symbols

def cmd_word_count(msg):
	"""
	Returns the number of received words so far.

	@param msg: message associated with the command
	@type msg: str
	@return: "state withe the message 'Actual word count is <number> words'
	@rtype: str
	"""
	return state.done("Actual word count is " + str(WORDCOUNT) + " words.")

def cmd_karma(user):
	"""
	Returns a state with number of karma points for given user.

	@param user: user whose karma is queried
	@type user: str
	@return: done state with message '<user> has <number> points of karma'"
	@rtype: state
	"""
	points = KARMA.get(user, 0)

	return state.done("'" + user + "' has " + str(points) + " points of karma")


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
	@rtype: state
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
	@return: done state if the information is done parsing
	@rtype: state
	@raise Exception: in case that change_karma return other than done or next
	state
	"""

	pattern = "\S+(\+{2}|\-{2})"
	if re.match(pattern, msg):
		length = len(msg)
		user = msg[0:length-2]
		action = msg[-2:]
		ret = change_karma(user + " " + action)

		if state.is_done(ret):
			return ret
		elif state.is_next(ret):
			return state.next(msg)
		else:
			raise Exception('Illegal state of change_karma command.')
	else:
		return state.next(msg)

FILTERS = [f_word_count, f_karma] #: Global array for storing the filters

def change_karma(msg, increase = True):
	"""
	Changes users karma by one.
	"""

	try:
		msg, action = msg.split(" ", 1)
	except ValueError:
		return state.next(msg)

	KARMA.setdefault(msg, 0)

	if action == "++":
		KARMA[msg] += 1
		log = msg + "'s karma was increased by 1."
	elif action == "--":
		KARMA[msg] -= 1
		log = msg + "'s karma was decreased by 1."
	else:
		return state.next(msg)

	if KARMA[msg] == 0:
		del KARMA[msg]

	return state.done(log)

def read():
	"""
	Read input and return it.

	@return: read data
	@rtype: str
	"""
	input = raw_input()
	return input

def write(arg):
	"""
	Write (send) argument to output.

	@param arg: text to be written to the output
	@return: None
	@rtype: None
	"""
	print(arg)

def parse(msg):
	"""
	Parses given input.

	@param msg: input message to parse
	@return: return message processed with associated commands and filters
	@rtype: str
	"""
	try:
		cmd, args = msg.split(" ", 1)
	except ValueError:
		cmd = msg
		args = ""

	if cmd in COMMANDS.keys():
		ret = COMMANDS[cmd](args)

		if state.is_done(ret):
			return ret.value
		elif state.is_next(ret):
			pass
		else:
			raise Exception('Illegal state of command.')

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

		except (KeyboardInterrupt, EOFError):
			break
