#!/usr/bin/python

"""
This module serves as a remote logging server for the IRC bot. When executed,
it loads the configuration (host, port, file) and starts logging into a gzipped
file.

@author: Marek Osvald
@version: 2012.1221
@since: 2012.0510

@undocumented: __package__
"""
import gzip
import SocketServer
import sys
import conf_parse


def check_file_for_append(filename):
	"""
	Checks whether a file with given filename can be oppend for append mode.

	@param filename: path and filename to check
	@type filename: str
	@return True and file object if successfuly opened, False and None otherwise
	@rtype: tuple
	"""
	file = None

	try:
		file = gzip.open(filename, "a")
	except IOError:
		return False, None

	return file.writable(), file


class RemoteLogger(SocketServer.BaseRequestHandler):
	"""
	Handler that logs every message to a gzipped file.
	"""
	def setup(self):
		"""
		Initializes the file instance variable.

		@return: None
		@rtype: None
		"""
		global file

		self._file = file

	def finish(self):
		"""
		Closes the attached file.

		@return: None
		@rtype: None
		"""

		if self._file:
			self._file.close()

	def handle(self):
		"""
		Handles an incoming message or interrupt key combination.

		@return: None
		@rtype: None
		"""
		global running

		print "===  {0:<70}  ===".format("CONNECTION ESTABLISHED")
		while True:
			try:
				data = self.request.recv(1024).strip()

				if not data:
					print "===  {0:<70}  ===".format("CONNECTION CLOSED")
					break

				print "<<", data
				self._file.write("%s\n" % data)

			except KeyboardInterrupt:
				running = False
				print "\n===  {0:<70}  ===".format("SHUTTING DOWN")
				break


file = None #: file that is used by the remote logger
config = None #: configuration for the remote logging server
running = True #: designates whether the remote logging server is running or not


if __name__ == "__main__":
	config = conf_parse.load()

	HELLO_STRING =\
"""\
================================================================================
=  This is IRCBot Remote Logging Server v1.0                                   =
=  Created by Marek Osvald, 2012                                               =
================================================================================
=  The bot is operating on:                                                    =
=      server:  {0:<62} =
=      port:    {1:<62} =
=      file:    {2:<62} =
================================================================================\
"""
	appendable, file = check_file_for_append(config["file"])

	if not appendable:
		print "[FATAL]  Unable to open logging file", config["file"]
		print "===  {0:<70}  ===".format("SHUTTING DOWN")
		sys.exit(0)

	SocketServer.TCPServer.allow_reuse_address = True
	server = SocketServer.TCPServer(("localhost", 9999), RemoteLogger)

	print HELLO_STRING.format(config["server"], config["port"], config["file"])

	while running:
		try:
			server.handle_request()
		except KeyboardInterrupt:
			print "\n===  {0:<70}  ===".format("SHUTTING DOWN")
			sys.exit(0)
