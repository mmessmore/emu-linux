#!/bin/sh

. common/functions.sh

check_root

cat >/etc/apt/sources.list.d/llvm.list <<-END
	deb http://apt.llvm.org/buster/ llvm-toolchain-buster main
	deb-src http://apt.llvm.org/buster/ llvm-toolchain-buster main
END

apt-get update
apt-get install -y vim git clang lldb lld curl pipenv
