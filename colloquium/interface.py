#!/usr/bin/python

"""
This module contains interface for the IRCBot. Currently available are Shell
interface and Telnet interface.

@author: Daniel Mach
@author: Martin Sivak
@author: Marek Osvald
@version: 2012.1216
@since: 2012.1019

@undocumented: __package__
"""
from __future__ import print_function
import re
import socket
import getpass

class IRCBotInterface(object):
	"""
	Class representing general I/O interface for an IRC bot.
	"""
	def read(self):
		"""
		Common reading method. Not implemented.
		@raise NotImplemented: every time
		@return: None
		@rtype: None
		"""
		raise NotImplemented

	def write(self, msg):
		"""
		Common writing method. Not implemented.
		@raise NotImplemented: every time
		@return: None
		@rtype: None
		"""
		raise NotImplemented

	def open(self):
		"""
		Common method initializing the bot. Not implemented.
		@raise NotImplemented: every time
		@return: None
		@rtype: None
		"""
		raise NotImplemented

	def close(self):
		"""
		Common method shutting down the bot. Not implemented.
		@raise NotImplemented: every time
		@return: None
		@rtype: None
		"""
		raise NotImplemented


class IRCBotShellInterface(IRCBotInterface):
	"""
	This is command line interface of an IRC bot.
	"""
	def __init__(self):
		"""
		Parameterless constructor.
		"""
		pass

	def read(self, read_function = raw_input):
		"""
		Reads input and returns it.

		@param read_function: function to use for input (mainly for testing
		purposes)
		@type read_function: function
		@return: read data
		@rtype: str
		"""
		return read_function("> ")

	def write(self, arg, write_function = print):
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

	def open(self):
		"""
		Does nothing.
		@return: None
		@rtype: None
		"""
		pass

	def close(self):
		"""
		Does nothing.
		@return: None
		@rtype: None
		"""
		pass


class IRCBotTelnetInterface(IRCBotInterface):
	"""
	Class representing a telnet interface for an IRCBot.
	"""
	def __init__(self, address = None, port = 8080):
		"""
		Parametric constructor. Initializes bot with given address and port.
		@param address: address to initialize bot with, default is None
		@type address: str
		@param port: port to initialize bot with, default is 8080
		@type port: int
		"""

		self._timeout = 60 * 10
		self._listen = None
		self._sfile = None
		self._socket = None

		self._addr = address
		self._port = port

	def client(self):
		"""
		If there is no designated socket object, it creates one. Returns
		designated socket object for bot's telnet interface.

		@return: socket file object
		@rtype: file
		"""

		if not self._socket:
			# wait for incoming connection
			conn, addr = self._listen.accept()

			# prepare python File object
			self._sfile = conn.makefile()
			self._socket = conn

		return self._sfile

	def disconnected(self):
		"""
		Designates the bot as disconnected from the network.

		@return: None
		@rtype: None
		"""
		self._socket = None
		self._sfile = None

	def read(self):
		"""
		Gets valid _sfile for current client and then reads one line from
		network. In case the line was empty or exception was thrown, calls
		self.disconnect() and tries again.

		@return: None
		@rtype: None
		"""
		while True:
			try:
				data = self.client().readline()
				if data == "":
					self.disconnected()
				else:
					return data.rstrip()
			except (socket.error, socket.timeout, IOError) as ex:
				self.disconnected()


	def write(self, msg):
		"""
		Writes message over the network.

		@param msg: message to write
		@type msg: str
		@return: None
		@rtype: None
		"""
		self._sfile.write(msg + "\n")
		self._sfile.flush()


	def open(self):
		"""
		Makes a socket connection.

		@return: None
		@rtype: None
		@raise Exception: When no valid address for a socket has been found.
		"""
		for (family, socktype, proto, canonname, sockaddr) in socket.getaddrinfo(self._addr, self._port):
			try:
				if socktype != socket.SOCK_STREAM:
					continue
				if family != socket.AF_INET:
					continue

				sock = socket.socket(family, socktype, proto)
				sock.settimeout(self._timeout)

				# listen on the selected address
				sock.bind(sockaddr)
				sock.listen(0)
				self._listen = sock

			except (socket.error, socket.timeout, IOError) as ex:
				print(str(ex))

		if self._listen == None:
			raise Exception("No valid address found")

	def close(self):
		"""
		Closes a socket connection.

		@return: None
		@rtype: None
		"""
		if self._listen:
			self._listen.close()

		if self._socket:
			self._socket.close()

if __name__ == "__main__":
	x = IRCBotTelnetInterface("localhost", 8082)
	x.open()

	while True:
		data = x.read()
		if data == "":
			break

		print("Received:", data)
		x.write(data)
