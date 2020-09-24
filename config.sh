#!/bin/sh

export EMU_MNT=/mnt/emu-root
EMU_TGT="$(uname -m)-emu-linux-gnu"
export EMU_TGT
export BUILD_USER=mike
export BUILD_GROUP=mike
export PATH="${EMU_MNT}/tools/bin:${PATH}"
