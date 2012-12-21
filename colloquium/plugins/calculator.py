#!/usr/bin/python

"""
This module is a calculator plugin for IRC bot.

@author: Marek Osvald
@version: 2012.1216
@since: 2012.1019

@undocumented: __package__
"""
import state
import re


def cmd_calc(exp):
	"""
	Calculates mathematical expression and returns a state with the result.

	@param exp: expression to be calculated
	@type exp: str
	@return: result of the expression
	@rtype: state.done|state.next
	"""
	if exp is None:
		return state.next(exp)

	pattern = "\(?\-?\d*.?\d+(\s*[\+\-\*\/]\(*\s*\d*.?\d+\)*)*\)?"

	if re.match(pattern, exp):
		try:
			return state.done(str(eval(exp))) # exp IS VALID math expression
		except (SyntaxError, ZeroDivisionError):
			return state.next(exp) # exp IS NOT VALID math expression

	return state.next(exp) # exp contains non-mathematical symbols