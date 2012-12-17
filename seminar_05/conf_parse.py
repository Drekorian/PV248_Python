#!/usr/bin/python

"""
This module parses command line options indicating server address, port and
delay of an IRC Bot and also command line arguments specifying configuration
files. The module is capable of merging these using priority command line >
configuration files > defaults and properly handles multiple configuration files
with different configuration sections.

When executed, prints all loaded configurations to the standard output.

@author: Marek Osvald
@version: 2012.1217
@since: 2012.1116

@undocumented: __package__
"""
import optparse
import ConfigParser


SERVER_DEFAULT = "localhost"
""" Global variable that stores default server address value"""
PORT_DEFAULT   = 8082
""" Global variable that stores default server port value"""
DELAY_DEFAULT  = 5
""" Global variable that stores default delay value"""


def parse_argv():
	"""
	Parses the command line argument and options.

	@return: pair that contains optparse.OptionValues instance with parsed
	options and an array of command line arguments
	@rtype: tuple
	"""
	parser = optparse.OptionParser("%prog [options] arg1 arg2")

	parser.add_option(
		"-s", "--server",
		help = "sets the address of a server, default is localhost",
		dest = "server",
		type = "string",
		action = "store"
	)

	parser.add_option(
		"-p", "--port",
		help = "sets the port of a server, default is 8082",
		dest = "port",
		type = "int",
		action = "store"
	)

	parser.add_option(
		"-d", "--delay",
		help = "sets the delay time of the delay command in seconds, default is "
				"5",
		dest = "delay",
		type = "int",
		action = "store"
	)

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
			options["server"] = parser.get(section, "server")
			options["port"]   = parser.get(section, "port")
			options["delay"]  = parser.get(section, "delay")
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

	options["server"] = cmd_options.get("server") or conf_options.get("server")\
		or SERVER_DEFAULT
	options["port"]   = cmd_options.get("port")   or conf_options.get("port")\
		or PORT_DEFAULT
	options["delay"]  = cmd_options.get("delay")  or conf_options.get("delay")\
		or DELAY_DEFAULT

	return options


if __name__ == "__main__":
	conf = load()
	print "Loaded configuration: "

	for key in conf:
		print "\t%s: %s" % (key, str(conf[key]))
