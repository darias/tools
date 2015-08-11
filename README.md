# tools

This repo contains general purpose tools useful in building systems.

## daemon.sh - Daemon Template

The daemon runs processes continuously until stopped with a kill. A few sample command-line
arguments are given. These can be wrapped into a configuration file and run with rc.py.

An example rc.py configuration file daemon.sh.json is included

## rc.py - Run Configured Wrapper

rc.py (run configured) - Wrap command-line command to allow configuration via json file

The json file specifies objects that name various run configurations. Each configuration
consists of name-value pairs. The name is used as a flag and the value is the flag's value.
Empty ("") values indicate no value is required.

The special object name "_executable" is used to specify a default pathname to the
exectuable. This can be overriden from with the -e/--executable flag.

The special object name "_help" is for documentation.

An example file for driving kafkacat  kc.json is included.
