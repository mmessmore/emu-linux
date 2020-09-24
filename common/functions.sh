#!/bin/sh

################################################################################
# Some common functions used throughout these scripts
################################################################################

####################
# Die with a message and exit code
#
# Arguments:
#	Exit code
#	Message
####################
bail() {
	status="$1"

	red=$(tput setaf 1)
	normal=$(tput sgr0)
	shift
	echo "$red" "$@" "$normal"
	exit "$status"
}

####################
# Make sure we're running as root or exit
#
####################
check_root() {
	[ "$(id -u)" = 0 ] || bail 1 "This script needs to be run as root"
}

####################
# Make sure we're running as root or exit
#
####################
check_user() {
	[ "$(id -u)" != 0 ] || bail 1 "This script can't be run as root"
}

####################
# this kind of mimics read -p, since dash doesn't have that
#
# Arguments:
#   variable name to assign to
#   prompt text
# Globals:
#	The first argument (yes, it's a dirty hack)
####################
prompt() {
	var=$1
	shift

	# shellcheck disable=SC2039
	echo -n "$@" :

	# shellcheck disable=SC2229
	read -r "$var"

	# shellcheck disable=SC2163
	export "$var"
}


####################
# Yes/No prompt defaulting to No
#
# Arguments:
#   prompt text
# Returns:
#	0 for yes
#	1 for no
####################
yn_prompt() {
	# shellcheck disable=SC2039
	echo -n "$@" " (y/N):"

	# shellcheck disable=SC2229
	while read -r input; do
		case $input in
			y|Y) return 0;;
			n|N|"") return 1;;
		esac
		echo "Invalid response: ${input}"
	# shellcheck disable=SC2039
	echo -n "$@" " (y/N):"
	done
}


####################
# Print text bold for titles
#
# Arguments:
#	prompt text
####################
title() {
	bold=$(tput bold)
	normal=$(tput sgr0)
	echo
	echo "$bold" "$@" "$normal"
	echo
}
