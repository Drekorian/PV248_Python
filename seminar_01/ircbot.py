#!/usr/bin/python
import re
import state

KARMA = {}

def cmd_shutdown(msg):
	"""
	Raises SystemExit exception.

	@return: None
	@rtype: None
	"""
	raise SystemExit

def cmd_calc(exp):
	"""
	Calculates mathematical expression.

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
	return state.done("Actual word count is " + str(WORDCOUNT) + " words.")

def cmd_karma(msg):
	points = KARMA.get(msg, 0)

	return state.done("'" + msg + "' has " + str(points) + " points of karma")

COMMANDS = {
	"SHUTDOWN":   cmd_shutdown,
	"calc":       cmd_calc,
	"word-count": cmd_word_count,
	"karma":      cmd_karma,
}


WORDCOUNT = 0

def f_word_count(msg):
	global WORDCOUNT
	WORDCOUNT += len(msg.split(" "))
	return state.next(msg)

def f_karma(msg):
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

FILTERS = [f_word_count, f_karma]

def change_karma(msg, inc = True):
	try:
		user, action = msg.split(" ", 1)
	except ValueError:
		return state.next(msg)

	KARMA.setdefault(user, 0)

	if action == "++":
		KARMA[user] += 1
		log = user + "'s karma was increased by 1."
	elif action == "--":
		KARMA[user] -= 1
		log = user + "'s karma was decreased by 1."
	else:
		return state.next(msg)

	if KARMA[user] == 0:
		del KARMA[user]

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
	@type arg: str
	"""
	print(arg)

def parse(msg):
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
			pass #FIXME: continue processing?
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