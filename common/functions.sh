#!/bin/sh

bail() {
	status="$1"
	shift
	echo "$@" >&2
	exit "$status"
}

check_root() {
	[ $(id -u) = 0 ] || bail "This script needs to be run as root"
}
