#!/usr/bin/python

"""
This module is a shutdown plugin for IRC bot.

@author: Marek Osvald
@version: 2012.1216
@since: 2012.1019

@undocumented: __package__
"""

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