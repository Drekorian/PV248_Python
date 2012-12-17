#!/usr/bin/python

"""
This module describes processing states for the main process queue.

@author: Daniel Mach
@author: Martin Sivak
@author: Marek Osvald
@version: 2012.1213
@since: 2012.0921

@undocumented: __package__
"""

class state(object):
	"""
	Class representing common parsing state.
	"""
	def __init__(self, value = None):
		"""
		Parametric constructor. Initializes state with given value.

		@param value: value associated with the state, optional, default None
		"""
		self.value = value

class done(state):
	"""
	Class representing that the message is done being parsed.
	"""
	pass

class next(state):
	"""
	Class representing that the message should be processed by next command or
	filter.
	"""
	pass

class replace(state):
	"""
	Class representing that the message or part of the message has been
	replaced.
	"""
	pass

def is_done(o):
	"""
	Returns True if the state is done, False otherwise.

	@param o: object to check
	@type o: object
	@return: True if the state is done, False otherwise
	@rtype: bool
	"""
	return isinstance(o, done)

def is_next(o):
	"""
	Returns True if the state is next, False otherwise.

	@param o: object to check
	@type o: object
	@return: True if the state is next, False otherwise
	@rtype: bool
	"""
	return isinstance(o, next)

def is_replace(o):
	"""
	Returns True if the state is replace, False otherwise.

	@param o: object to check
	@type o: object
	@return: True if the state is replace, False otherwise
	@rtype: bool
	"""
	return isinstance(o, replace)
