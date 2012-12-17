#!/usr/bin/python

"""
This module contains all plugins for IRC bot.

@author: Marek Osvald
@version: 2012.1216
@since: 2012.1019

@undocumented: __package__
"""

from calculator import cmd_calc
from karma import cmd_karma
from karma import f_karma
from shutdown import cmd_shutdown
from wordcount import cmd_word_count
from wordcount import f_word_count
from local_logging import f_logging


COMMANDS = {
	"SHUTDOWN":   cmd_shutdown,
	"calc":       cmd_calc,
	"word-count": cmd_word_count,
	"karma":      cmd_karma,
} #: Global dictionary for storing commands

FILTERS = [f_logging, f_word_count, f_karma] #: Array for storing of the filters
