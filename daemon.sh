#!/bin/bash

#
# daemon - Daemon template
#

function usage() {
	echo "Usage: $0 --processes n"
}

function log() {
	echo `date "+%F %T %z %Z"` $*
}

# Process arguments
PLIMIT=5
SLEEP=5
while (($#)); do
	if [ "$1" == "--plimit" ]; then shift; PLIMIT=$1; 
	elif [ "$1" == "--processes" ]; then shift; PROCESSES=$1; 
	elif [ "$1" == "--sleep" ]; then shift; SLEEP=$1; 
	else
		echo "ERROR: Unrecognzied arg $1"; usage; exit 1
	fi
	shift
done
if [ -z "$PROCESSES" ]; then echo "ERROR: Missing --processes arg"; usage; exit 1; fi

RUN=true
function cleanup() {
	RUN=false
	#kill 0
}

trap cleanup SIGINT SIGTERM SIGTSTP

# Enter daemon loop
PLIMIT=4
P=0
PID=0
CYCLE=0
while $RUN; do
	((CYCLE++))
	log CYCLE $CYCLE

	for ((i = 0; i < $PROCESSES; i++)); do
		((PID++))
		if [ $P -ge $PLIMIT ]; then
			log "WAIT $P"
			wait
			P=0
		fi
		# Don't start new processes if we've been stopped
		if ! $RUN; then break; fi
		((P++))
		(
			# Process commands go here
			log START $PID
			sleep $SLEEP
			log END $PID
		)&
	done
	if [ $P -gt 0 ]; then log "WAIT $P final"; fi
	wait
done
wait
