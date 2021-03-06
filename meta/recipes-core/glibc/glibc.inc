DESCRIPTION = "GNU C Library"
HOMEPAGE = "http://www.gnu.org/software/libc/libc.html"
BUGTRACKER = "http://sources.redhat.com/bugzilla/"
SECTION = "libs"
LICENSE = "LGPLv2.1+ & GPLv2+"
LIC_FILES_CHKSUM = "file://COPYING;md5=393a5ca445f6965873eca0259a17f833 \
                    file://elf/cache.c;beginline=1;endline=17;md5=926aac25497b1de7d630b4749005d208 \
                    file://COPYING.LIB;md5=bbb461211a33b134d42ed5ee802b37ff \
                    file://bits/types.h;beginline=1;endline=18;md5=267938e7c0538e76f734551ec6ea908d"
# nptl needs unwind support in gcc, which can't be built without glibc.
DEPENDS = "virtual/${TARGET_PREFIX}gcc-intermediate linux-libc-headers"
RDEPENDS_${PN}-dev = "linux-libc-headers-dev"
#this leads to circular deps, so lets not add it yet
#RDEPENDS_ldd += " bash"
#RDEPENDS_${PN} += "${@['','libgcc']['nptl' in '${GLIBC_ADDONS}']}"
PROVIDES = "virtual/libc virtual/${TARGET_PREFIX}libc-for-gcc"
PROVIDES += "virtual/libintl virtual/libiconv"

STAGINGCC = "gcc-cross-intermediate"
STAGINGCC_virtclass-nativesdk = "gcc-crosssdk-intermediate"
PATH_prepend = "${STAGING_BINDIR_TOOLCHAIN}.${STAGINGCC}:"

TOOLCHAIN_OPTIONS = " --sysroot=${STAGING_DIR_TCBOOTSTRAP}"

# siteconfig.bbclass runs configure which needs a working compiler
# For the compiler to work we need a working libc yet libc isn't
# in the sysroots directory at this point. This means the libc.so
# linker script won't work as the --sysroot setting isn't correct.
# Here we create a hacked up libc linker script and pass in the right
# flags to let configure work. Ugly.
EXTRASITECONFIG = "CFLAGS='${CFLAGS} -Wl,-L${WORKDIR}/site_config_libc -L${WORKDIR}/site_config_libc -L${SYSROOT_DESTDIR}${libdir} -L${SYSROOT_DESTDIR}${base_libdir} -Wl,-L${SYSROOT_DESTDIR}${libdir} -Wl,-L${SYSROOT_DESTDIR}${base_libdir}'"
siteconfig_do_siteconfig_gencache_prepend = " \
	mkdir -p ${WORKDIR}/site_config_libc; \
	cp ${SYSROOT_DESTDIR}${libdir}/libc.so ${WORKDIR}/site_config_libc; \
	sed -i -e 's# ${base_libdir}# ${SYSROOT_DESTDIR}${base_libdir}#g' -e 's# ${libdir}# ${SYSROOT_DESTDIR}${libdir}#g' ${WORKDIR}/site_config_libc/libc.so; \
"

inherit autotools

GLIBC_EXTRA_OECONF ?= ""
INHIBIT_DEFAULT_DEPS = "1"

do_rig_locales() {
	# If indicated, only build a limited selection of locales
	if [ "x${LIMIT_BUILT_LOCALES}" != "x" ]; then
		INFILE="${S}/localedata/SUPPORTED"
		OUTFILE="${S}/localedata/SUPPORTED.tmp"
		head -n 3 $INFILE > $OUTFILE
		for i in ${LIMIT_BUILT_LOCALES}; do
			echo 
			grep $i $INFILE >> $OUTFILE
		done
		head --lines=-1 $OUTFILE > $INFILE
		tail --lines=1 $OUTFILE | sed 's#\\##' >> $INFILE
	fi
}

addtask rig_locales before do_compile after do_configure

ARM_INSTRUCTION_SET = "arm"
