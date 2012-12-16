#!/usr/bin/python

"""
This module is a word count plugin for IRC bot.

@author: Marek Osvald
@version: 2012.1216
@since: 2012.1019

@undocumented: __package__
"""

import state


WORDCOUNT = 0 #: Global variable for storing the number of received words

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