#!/usr/bin/python

"""
This module serves a client for the remote logging server.

@author: Marek Osvald
@version: 2012.1221
@since: 2012.0510

@undocumented: __package__
"""
import socket
from plugins import state

class RemoteClient(object):
	"""
	Remote client class that forwards the messages to remote logging server.
	"""
	def __init__(self, host, port):
		"""
		Parametric constructor. constructors. Sets client's socket to given hostname
		and port.

		@param host: host to connect to
		@type host: str
		@param port: port to connect to
		@type port: int
		"""
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket.connect((host, port))

	def send(self, msg):
		"""
		Sends a message to client's server.

		@param msg: message to send
		@type msg: str
		@return: next state with the original message
		@rtype: state.next
		@raise socket.error: When sending fails
		"""
		try:
			self._socket.sendall(msg)
		except socket.error:
			print "[ERROR] ", "Remote logging attempt failed!", msg

		return state.next(msg)

	def close(self):
		"""
		Closes the clients

		@return: None
		@rtype: None
		@raise socket.error: When the socket has been already closed
		"""
		try:
			self._socket.shutdown(socket.SHUT_WR)
			self._socket.close()
		except socket.error:
			pass
