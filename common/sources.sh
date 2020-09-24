#!/bin/sh

export BINUTILS_VERSION="2.35"
export BINUTILS_URL="http://mirrors.kernel.org/gnu/binutils/binutils-${BINUTILS_VERSION}.tar.xz"

export GCC_VERSION="10.1.0"
export GCC_URL="http://www.netgull.com/gcc/releases/gcc-${GCC_VERSION}/gcc-${GCC_VERSION}.tar.xz"

export MPFR_VERSION="4.1.0"
export MPFR_URL="https://www.mpfr.org/mpfr-current/mpfr-${MPFR_VERSION}.tar.xz"

export GMP_VERSION="6.2.0"
export GMP_URL="https://gmplib.org/download/gmp/gmp-${GMP_VERSION}.tar.xz"

export MPC_VERSION="1.2.0"
export MPC_URL="https://ftp.gnu.org/gnu/mpc/mpc-${MPC_VERSION}.tar.gz"

export LINUX_MAJOR="5.x"
export LINUX_VERSION="5.8.11"
export LINUX_URL="https://cdn.kernel.org/pub/linux/kernel/v${LINUX_MAJOR}/linux-${LINUX_VERSION}.tar.xz"

export GLIBC_VERSION="2.32"
export GLIBC_URL="https://ftp.gnu.org/gnu/glibc/glibc-${GLIBC_VERSION}.tar.xz"
