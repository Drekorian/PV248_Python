#!/usr/bin/python

"""
This module contains a class that represents a thread for delaying messages.

@author: Marek Osvald
@version: 2012.1216
@since: 2012.1105

@undocumented: __package__
"""

from plugins import state
import time
import threading
import Queue

class DelayThread(threading.Thread):
	"""
	Class representing a thread that delay received message by a few seconds.
	"""
	def __init__(self, interface, delay):
		"""
		Parametric constructor.

		@param interface: interface to use for writing the messages
		@type interface: interface.IrcBotInterface
		@param delay: delay time in seconds, default is 5
		@type delay: int
		"""
		threading.Thread.__init__(self)

		self._interface = interface
		self._delay = delay
		self._running = True
		self._queue = Queue.Queue()

	def run(self):
		"""
		While the thread is designated as running, runs an endless loop while
		taking the messages from the queue and writing them via the interface.
		@return: None
		@rtype: None
		"""
		while self._running:
			if not self._queue.empty():
				msg = self._queue.get()
				print msg
				time.sleep(self._delay)
				self._interface.write(msg)

	def stop(self):
		"""
		Designates the thread as not running.

		@return: None
		@rtype: None
		"""
		self._running = False

	def put_msg(self, msg):
		"""
		Adds a message to the queue.

		@param msg: message to enqueue
		@type msg: str
		@return: done statement with received message
		@rtype: state.done
		"""
		self._queue.put(msg)
		return state.done() # returns none in order to force delay
