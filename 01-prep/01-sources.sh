#!/bin/sh

if [ "$1" = "-v" ]; then
	set -x
fi

. ./config.sh
. common/functions.sh
. common/sources.sh

check_user

cd $EMU_MNT/src || bail $? "Could not cd to ${EMU_MNT}/src"

####################
# Download, build, and install Binutils to the tools dir
####################
build_binutils() {
	title "Fetching GNU Binutils ${BINUTILS_VERSION}"
	if ! [ -f "binutils-${BINUTILS_VERSION}.tar.xz" ]; then
		wget "$BINUTILS_URL" || bail $? "Couldn't download binutils"
	fi
	if ! [ -d "binutils-${BINUTILS_VERSION}" ]; then
		tar xf "binutils-${BINUTILS_VERSION}.tar.xz" ||
			bail $? "Couldn't unpack binutils"
	fi
	cd binutils-${BINUTILS_VERSION} || bail $? "Failed cding to binutils src"

	# shellcheck disable=SC2015
	# this is a dumb warning
	mkdir build && cd build || bail $? "Error making buildir"

	title "Building Binutils"
	../configure "--prefix=${EMU_MNT}/tools" \
			     "--with-sysroot=${EMU_MNT}" \
				 "--target=${EMU_TGT}" \
				 --disable-nls \
				 --disable-werror
	make

	title "Installing Binutils"
	make install
}

####################
# Download, build, and install GCC to the tools dir
####################
build_gcc() {

	title "Downloading GCC (and associated) sources"
	if ! [ -f "gcc-${GCC_VERSION}.tar.xz" ]; then
		wget "$GCC_URL" || bail $? "Couldn't download gcc"
	fi
	if ! [ -f "mpfr-${MPFR_VERSION}.tar.xz" ]; then
		wget "$MPFR_URL" || bail $? "Couldn't download mpfr"
	fi
	if ! [ -f "gmp-${GMP_VERSION}.tar.xz" ]; then
		wget "$GMP_URL" || bail $? "Couldn't download gmp"
	fi
	if ! [ -f "mpc-${MPC_VERSION}.tar.gz" ]; then
		wget "$MPC_URL" || bail $? "Couldn't download mpc"
	fi

	title "Unpacking GCC (and associated) sources"
	if ! [ -d "gcc-${GCC_VERSION}" ]; then
		tar xf "./gcc-${GCC_VERSION}.tar.xz" ||
			bail $? "Couldn't unpack gcc"
	fi
	cd "gcc-${GCC_VERSION}" || bail $? "Couldn't cd to gcc src dir"

	if ! [ -d "mpfr" ]; then
		tar xf "../mpfr-${MPFR_VERSION}.tar.xz" ||
			bail $? "Couldn't unpack mpfr"
		mv "mpfr-${MPFR_VERSION}" mpfr
	fi
	if ! [ -d "gmp" ]; then
		tar xf "../gmp-${GMP_VERSION}.tar.xz" ||
			bail $? "Couldn't unpack gmp"
		mv "gmp-${GMP_VERSION}" gmp
	fi
	if ! [ -d "mpc" ]; then
		tar xf "../mpc-${MPC_VERSION}.tar.gz" ||
			bail $? "Couldn't unpack mpc"
		mv "mpc-${MPC_VERSION}" mpc
	fi


	title "Building GCC"
	sed -e '/m64=/s/lib64/lib/' -i.orig gcc/config/i386/t-linux64

	# shellcheck disable=SC2015
	mkdir build && cd build || bail $? "couldn't deal with build directory"
	../configure \
		--target="$EMU_TGT" \
		--prefix="${EMU_MNT}/tools" \
		--with-glibc-version=2.11 \
		--with-sysroot="$EMU_MNT" \
		--with-newlib \
		--without-headers \
		--enable-initfini-array \
		--disable-nls \
		--disable-shared \
		--disable-multilib \
		--disable-decimal-float \
		--disable-threads \
		--disable-libatomic \
		--disable-libgomp \
		--disable-libquadmath \
		--disable-libssp \
		--disable-libvtv \
		--disable-libstdcxx \
		--enable-languages=c,c++
	make
	make install

	cd ..
	cat gcc/limitx.h gcc/glimits.h gcc/limity.h > \
	  "$(dirname "$("${EMU_TGT}-gcc" -print-libgcc-file-name)")"/install-tools/include/limits.h

}

build_kernel_headers() {
	title "Fetching Linux Kernel ${LINUX_VERSION}"
	if ! [ -f "linux-${LINUX_VERSION}.tar.xz" ]; then
		wget "$LINUX_URL" || bail $? "Couldn't download binutils"
	fi
	if ! [ -d "linux-${LINUX_VERSION}" ]; then
		tar xf "linux-${LINUX_VERSION}.tar.xz" ||
			bail $? "Couldn't unpack linux"
	fi
	cd linux-${LINUX_VERSION} || bail $? "Failed cding to binutils src"

	title "Building Linux Kernel Headers"
	make mrproper
	make headers
	find usr/include -name '.*' -delete
	rm usr/include/Makefile
	cp -rv usr/include "${EMU_MNT}/usr"
}


if ! [ -f "${EMU_MNT}/tools/bin/${EMU_TGT}-ld" ]; then
	( build_binutils ) || bail $? "Couldn't build binutils"
fi

if ! [ -f "${EMU_MNT}/tools/bin/${EMU_TGT}-gcc" ]; then
	( build_gcc ) || bail $? "Couldn't build gcc"
fi

if ! [ -f "${EMU_MNT}/usr/include/asm/termios.h" ]; then
	(build_kernel_headers) || bail $? "Couldn't build Linux Kernel Headers"A
fi

