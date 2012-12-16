#!/usr/bin/python

"""
This module is a logging plugin for IRC bot.

@author: Marek Osvald
@version: 2012.1216
@since: 2012.1019

@undocumented: __package__
"""
import logging
import state

def f_logging(msg, logfile = "ircbot.log"):
	"""
	Logs a message.

	@param msg: message to log
	@type msg: str
	@return: next state with the original message
	@rtype: state.next
	"""
	logging.basicConfig(format = "%(asctime)s  %(message)s",
		datefmt = "%d.%m.%Y %H:%M:%S",
		filename = logfile,
		level = logging.DEBUG
	)
	logging.info(msg)

	return state.next(msg)