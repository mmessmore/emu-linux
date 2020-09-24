#!/bin/sh

if [ "$1" = "-v" ]; then
	set -x
fi

. ./config.sh
. common/functions.sh

####################
# Get a block device by UUID
#
# Arguments
#	UUID
# Outputs
#	Block device path (eg. /dev/sdb1)
####################
uuid_to_block() {
	UUID=$1
	blkid -l -t "PARTUUID=${UUID}" | cut -d: -f1
}

####################
# Find UUIDS in fstab for a given fs type
#
# Arguments
#	fstyoe
# Outputs
#	Line separated list of UUIDS (lowercased)
####################
find_uuids_by_fs() {
	fstype=$1
	awk '$3 == "'"$fstype"'" && $1 ~ /^UUID/ {split($1, uuid, "="); print tolower(uuid[2])}' < fstab
}

check_root

disk=/dev/null
prompt disk "What disk?"

while ! [ -b "$disk" ]; do
	echo "${disk} is not a valid block device.  Try again."
	prompt disk "What disk?"
done

title "Current disk layout"
sfdisk -d "$disk"
echo

title "About to lay this on disk ${disk}"
cat layout
echo

yn_prompt "This will destroy ${disk}.  You sure?" || exit 1

title "Setting Disk Label"
sfdisk "$disk" < layout

title "Formatting filesystems"
find_uuids_by_fs ext4 | while read -r uuid; do
	mkfs.ext4 "$(uuid_to_block "$uuid")"
done
find_uuids_by_fs swap | while read -r uuid; do
	mkswap "$(uuid_to_block "$uuid")"
done

title "Mounting root in ${EMU_MNT}"
mkdir -p "$EMU_MNT"
if ! mount -t ext4 "$(uuid_to_block "$(grep -v '[[:blank:]]*#' fstab | awk '$2 == "/" {split($1, uuid, "="); print tolower(uuid[2])}')")" "$EMU_MNT"; then
	echo "Error mounting new / to ${EMU_MNT}"
	echo "Troubleshoot and try again?"
fi

title "Making basic directories"
for dir in bin etc lib sbin usr var lib64 tools src; do
	target_dir="${EMU_MNT}/${dir}"
	mkdir -p "$target_dir"
	chown "${BUILD_USER}:${BUILD_GROUP}" "$target_dir"
done
