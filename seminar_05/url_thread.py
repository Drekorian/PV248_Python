#!/usr/bin/python

"""
This module contains a class that represents a thread for parsing titles of web
pages given its URL.

@author: Marek Osvald
@version: 2012.1216
@since: 2012.1105

@undocumented: __package__
"""

import httplib
import re
import plugins.state as state
import threading
import Queue

class URLThread(threading.Thread):
	"""
	Class representing a thread that delay received message by a few seconds.
	"""
	def __init__(self, interface):
		"""
		   Parametric constructor.

		   @param interface: interface to use for writing the messagess
		   @type interface: interface.IrcBotInterface
		   """
		threading.Thread.__init__(self)
		self._interface = interface
		self._queue = Queue.Queue()
		self._running = True

	def run(self):
		"""
		While the thread is designated as running, runs an endless loop that
		takes URLs from the input queue and writes their title to the interface.
		When faced with non 404 response code, tries to parse the data once
		again to find the redirect.

		@return: None
		@rtype: None
		"""
		while self._running:
			if not self._queue.empty():
				address = self._queue.get()
				connection = httplib.HTTPConnection(address["server"])

				try :
					connection.request("GET", address["url"])
					response = connection.getresponse()

					print "Parsing: " + address["original"], response.status, response.reason

					data = response.read()
					if response.status != 200:
						self.enqueue(data, address["original"])
						continue

					connection.close()

					title_pattern = "<title>(?P<title>.*)</title>"

					match = re.search(title_pattern, data)
					if match:
						title = match.group("title")
						print address["original"] + "   " + title
						self._interface.write(address["original"] + " >> " + title)

				except Exception:
					pass

	def stop(self):
		"""
		Designates the thread as not running.

		@return: None
		@rtype: None
		"""
		self._running = False

	def enqueue(self, msg, original = None):
		"""
		Enqueues an URL into the input queue to be parsed.

		@param msg: message to be parsed
		@param original: original URL when being parsed recursively
		@return: next state with the original message
		@rtype: state.next
		"""
		url_pattern = "(http://)?(?P<server>[a-zA-Z0-9\-\.]+\.[a-z]{2,6})(?P<url>(/([a-zA-Z0-9]|\$|\&|\+|\,|\:|\;|\=|\?|\@|\#|\%|\.|\_|\~|\-)*)*)"
		match = re.search(url_pattern, msg)

		if match:
			self._queue.put({
				"original": original if original else match.group("server") + match.group("url"),
				"server": match.group("server"),
				"url": match.group("url")
			})
		return state.next(msg)
