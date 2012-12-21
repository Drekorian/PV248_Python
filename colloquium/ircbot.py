#!/usr/bin/python

"""
This module is a mockup of a IRC bot. When executed, it runs an endless loop
that can be interrupted with EOF keystroke or interrupt keystroke. Bot is
capable of handling commands and filters.

@author: Marek Osvald
@version: 2012.1214
@since: 2012.0510

@undocumented: __package__
"""
import sys
import conf_parse
import delay_thread
import interface
import plugins
from plugins import state
import remote_client
import socket
import url_thread


class IrcBot(object):
	"""
	Class representing the bot with a local shell interface.
	"""
	COMMANDS = plugins.COMMANDS #: A dictionary of commands processed by bot.
	FILTERS = plugins.FILTERS #: An array of filters processed by bot.

	def __init__(self, interface):
		"""
		Parametric constructor. Specifies an interface for the bot.

		@param interface: implementation of the I/O interface
		@type interface: object
		"""
		self._if = interface

	def parse(self, msg):
		"""
		Parses given input.

		@param msg: input message to parse
		@type msg: str
		@return: return message processed with associated commands and filters
		@rtype: str
		"""

		print "<<", msg

		try:
			cmd, args = msg.split(" ", 1)
		except ValueError:
			cmd, args = msg.rstrip(), ""

		if cmd in self.COMMANDS:
			ret = self.COMMANDS[cmd](args)

			if state.is_done(ret):
				return ret.value
			elif state.is_next(ret):
				pass
			else:
				raise Exception("Illegal state of command.")

		for filter in self.FILTERS:
			ret = filter(msg)

			if state.is_done(ret):
				return ret.value

			if state.is_replace(ret):
				msg = ret.value

		return msg

	def run(self):
		"""
		Runs an endless loop that creates the gist of the bot.
		"""
		while True:
			msg = self._if.read()
			msg = self.parse(msg)
			if msg:
				print ">>", msg
				self._if.write(msg)


if __name__ == "__main__":
	HELLO_STRING =\
"""\
================================================================================
=  This is IRCBot 1.0                                                          =
=  Created by Marek Osvald, 2012                                               =
================================================================================
=  The bot is operating on:                                                    =
=      server:  {0:<62} =
=      port:    {1:<62} =
================================================================================
=  The delay command delay in seconds:  {2:<38} =
================================================================================\
"""

	REMOTE_LOG_SERVER_SUCCESS =\
"""\
=  Remote logging server is alive and working at:                              =
=      server:  {0:<62} =
=      port:    {1:<62} =
================================================================================\
"""

	REMOTE_LOG_SERVER_FAIL =\
"""\
=  Connection to remote logging server failed!                                 =
================================================================================\
"""

	config = conf_parse.load()

	ifc = interface.IRCBotTelnetInterface(config["server"], config["port"])
	ifc.open()
	bot = IrcBot(ifc)

	print HELLO_STRING.format(config["server"], config["port"], config["delay"])

	delay = delay_thread.DelayThread(ifc, config["delay"])
	bot.COMMANDS["delay"] = delay.put_msg

	url = url_thread.URLThread(ifc)
	bot.FILTERS.append(url.enqueue)

	client = None

	try:
		client = remote_client.RemoteClient(config["remote"], config["rport"])
		bot.FILTERS.append(client.send)
		print REMOTE_LOG_SERVER_SUCCESS.format(config["remote"], config["rport"])
	except socket.error:
		print REMOTE_LOG_SERVER_FAIL

	try:
		delay.start()
		url.start()
		bot.run()
	except (KeyboardInterrupt, EOFError, SystemExit):
		print "\n===  {0:<70}  ===".format("SHUTTING DOWN")
		delay.stop()
		url.stop()
		url.stop()

		if client:
			client.close()

		ifc.close()
		sys.exit(0)
