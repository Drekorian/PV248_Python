#!/usr/bin/python

"""
This module parses command line options indicating server address, port and
delay of an IRC Bot and also command line arguments specifying configuration
files. The module is capable of merging these using priority command line >
configuration files > defaults and properly handles multiple configuration files
with different configuration sections.

@author: Marek Osvald
@version: 2012.1217
@since: 2012.1116

@undocumented: __package__
"""
import optparse
import re
import sys
import ConfigParser


DEFAULTS = dict() #: Global dictionary for storing of the default values.


def get_filename():
	"""
	Returns name of the file that's currently being executed.

	@return: name of the file that's currently being executed
	@rtype: str
	"""
	full_path = sys.argv[0]
	pattern = ".*[\\\/](?P<file>.*)\.py"

	file = re.search(pattern, full_path).groups("file")[0]

	if file == "conf_parse":
		return "ircbot"

	return file


def parse_argv():
	"""
	Parses the command line argument and options.

	@return: pair that contains optparse.OptionValues instance with parsed
	options and an array of command line arguments
	@rtype: tuple
	"""
	parser = optparse.OptionParser("%prog [options] arg1 arg2")

	confs = {
		"ircbot": [{
			"long":		"server",
			"short":	"s",
			"help":		"sets the address of a server, default is localhost",
			"dest":		"server",
			"type":		"string",
			"action":	"store",
			"default":	"localhost"
		}, {
			"long":		"port",
			"short":	"p",
			"help":		"sets the port of a server, default is 8082",
			"dest":		"port",
			"type":		"int",
			"action":	"store",
			"default":	8082
		}, {
			"long":		"remote",
			"short":	"r",
			"help":		"sets the address of a remote logging server, default is"
							" localhost",
			"dest":		"remote",
			"type":		"string",
			"action":	"store",
			"default":	"localhost"
		}, {
		   "long":		"rport",
		   "short":		"o",
		   "help":		"sets the port of a remote logging server, default is"
							" 9999",
		   "dest":		"rport",
		   "type":		"int",
		   "action":	"store",
		   "default":	9999
	    }, {
			"long":		"delay",
			"short":	"d",
			"help":		"sets the delay time of the delay command in seconds, "
							"default is 5",
			"dest":		"delay",
			"type":		"int",
			"action":	"store",
			"default":	5
		}],

		"remote_server": [{
			"long":		"server",
			"short":	"s",
			"help":		"sets the address of a server, default is localhost",
			"dest":		"server",
			"type":		"string",
			"action":	"store",
			"default":	"localhost"
		}, {
			"long":		"port",
			"short":	"p",
			"help":		"sets the port of a server, default is 9999",
			"dest":		"port",
			"type":		"int",
			"action":	"store",
			"default":	9999
		}, {
			"long":		"file",
			"short":	"f",
			"help":		"gzipped file for storing incoming messages",
			"dest":		"file",
			"type":		"string",
			"action":	"store",
			"default":	"log.tar.gz"
		}]
	}

	for option in confs[get_filename()]:
		parser.add_option(
			"-%s" % option["short"],
			"--%s" % option["long"],
			help = option["help"],
			dest = option["dest"],
			type = option["type"],
			action = option["action"]
		)
		DEFAULTS[option["long"]] = option["default"]

	return parser.parse_args()


def load_config(config_files):
	"""
	Parses the options set in given configuration file(s).

	@param config_files: configuration file(s) to parse
	@type config_files: str|array|tuple
	@return: parsed options
	@rtype: dict
	"""

	parser = ConfigParser.SafeConfigParser()

	options = dict()

	try:
		parser.read(config_files)

		for section in parser.sections():
			for option in DEFAULTS.keys():
				options[option] = parser.get(section, option)

	except (ConfigParser.MissingSectionHeaderError, ConfigParser.NoOptionError,
		ConfigParser.NoSectionError) as ex:
		pass

	return options


def load():
	"""
	Loads and merges configuration options from both command line and
	configuration files passed via the command line.

	@return: parsed and merged options from both command and configuration
	file(s)
	@rtype: dictionary
	"""
	cmd_options, conf_files = parse_argv()
	cmd_options = cmd_options.__dict__
	conf_options = load_config(conf_files)

	options = dict()

	for option in DEFAULTS.keys():
		options[option] = cmd_options.get(option) or conf_options.get(option)\
			or DEFAULTS[option]

	return options
