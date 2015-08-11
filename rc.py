#!/usr/bin/python
import os
import sys
from optparse import OptionParser
import subprocess
import json
import string

#
# rc (run configured) - Wrap command-line command to allow configuration via json file
#
# The json file specifies objects that name various run configurations. Each configuration
# consists of name-value pairs. The name is used as a flag and the value is the flag's value.
# Empty ("") values indicate no value is required.
#
# The special object name "_executable" is used to specify a default pathname to the
# exectuable. This can be overriden from with the -e/--executable flag.
#
# The special object name "_help" is for documentation.
#


op = OptionParser()
op.add_option("-e", "--executable", dest="executable", help="Path to executable")
op.add_option("-c", "--config", dest="jsonconfig", help="Path to json configuration file")
op.add_option("-s", "--section", dest="section", help="json file object name")
op.add_option("-d", "--debug", dest="debug", action="store_true", help="Debug: Only show command")
(opts, args) = op.parse_args()

if opts.jsonconfig == None:
	print >> sys.stderr, "ERROR: Missing --config arg"
	raise SystemExit(1)
else:
	# Parse the configuration
	with open(opts.jsonconfig, "r") as f:
		try:
			config = json.load(f)
		except Exception as e:
			print >> sys.stderr, "ERROR: %s: %s" % (opts.jsonconfig, e)
			raise SystemExit(1)

	# Determine the executable
	if opts.executable != None:
		base = os.path.basename(opts.executable)
	elif config.has_key("_executable"):
		opts.executable = config["_executable"]
		base = os.path.basename(opts.executable)
	else:
		print >> sys.stderr, "ERROR: Missing -e (executable) arg"
		raise SystemExit(1)

	if opts.section == None:
		# Use basename of executable as section name in config file
		opts.section = base

	if not config.has_key(opts.section): 
		print >> sys.stderr, "ERROR: Config file %s missing object %s" % (opts.jsonconfig, opts.section)
		raise SystemExit(1)

	# Build the command arg array
	cmd = [ opts.executable ]
	for o in config[opts.section]:
		cmd.append(o)
		if config[opts.section][o] != "":
			s = config[opts.section][o]
			if len(args) > 0:
				# Break into segments on the value $
				a = s.split('$')
				t = [ a[0] ]
				first = True
				for w in a[1:]:
					d = w[0:1]
					if d in string.digits and d != '':
						# Evaluate the argument--only $0-$9 are allowed
						i = int(d)
						# Args start at index 1; missing args eval to ""
						if i - 1 < len(args):
							# Append the value
							t.append(args[i - 1])
				
						# Append the rest of the segment
						t.append(w[1:])
					else:
						# Just append the string with the $ restored
						t.append('$' + w)

				s = "".join(t)
				

			cmd.append(s)


if opts.debug:
	print " ".join(cmd)
	raise SystemExit(0)

try:
	subprocess.call(cmd)
except Exception as e:
	print >> sys.stderr, "ERROR: %s: %s" % (" ".join(cmd), e)
except KeyboardInterrupt as e:
	print >> sys.stderr, "BREAK"
