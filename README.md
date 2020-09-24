# emu-linux
trying to make my own LFS-esqe distro


# Instructions

## Config

### layout

Layout needs to be sfdisk-formatted partion layout for a disk

### fstab

The intended fstab for the target host.  All block devices need to be specified
by UUID (see the previous file).

We use this for other stuff like laying filesystems down on the partitions.
