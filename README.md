# tools

This repo contains general purpose tools useful in building systems.

## daemon.sh - Daemon Template

The daemon runs processes continuously until stopped with a kill. A few sample command-line
arguments are given. These can be wrapped into a configuration file and run with rc.py.

Example 1: Run the sample daemon specifying all necessary command-line arguments.
```
$ ./daemon.sh --processes 5
...
^C
```
Example 2: Run the sample daemon wrapped by rc.py.
```
$ ./rc.py -c daemon.sh.json
...
^C
```



An example rc.py configuration file daemon.sh.json is included

## rc.py - Run Configured Wrapper

rc.py (run configured) - Wrap command-line command to allow configuration via json file

Example: Run the kafkacat configuration to consume a single file.
```
$ ./rc.py -c kc.json -s consume-one > kafka-data/file
...
```
Arguments:

-e/--executable - path to executable to run (optional if executable specified in configuration)

-c/--config - path to JSON configuration file

-s/--section - name of configuration object in JSON file

The json file specifies objects that name various run configurations. Each configuration
consists of name-value pairs. The name is used as a flag and the value is the flag's value.
Empty ("") values indicate no value is required.

The special object name "_executable" is used to specify a default pathname to the
exectuable. This makes it unnecessary to specify the executable on the command-line.
This can be overriden from with the -e/--executable flag.

The special object name "_help" is for documentation. I use it to remind myself what the
argument flags mean.
