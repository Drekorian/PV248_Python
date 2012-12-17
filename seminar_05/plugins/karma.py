#!/usr/bin/python

"""
This module is a karma plugin for IRC bot.

@author: Marek Osvald
@version: 2012.1216
@since: 2012.1019

@undocumented: __package__
"""
import state

KARMA = {} #: Global dictionary for storing users' karma

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

	for exp in msg.split():
		exp = exp.lower()

		if exp == "c++":
			continue

		if exp.endswith("++") or msg.endswith("--"):
			user = exp[:-2].lower()
			action = exp[-2:]

			if user == "":
				continue

			KARMA.setdefault(user, 0)

			if action == "++":
				KARMA[user] += 1
			else:
				KARMA[user] -= 1

			if KARMA[user] == 0:
				del KARMA[user]

	return state.next(msg)