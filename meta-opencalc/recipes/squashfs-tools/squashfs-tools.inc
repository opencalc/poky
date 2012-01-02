DESCRIPTION = "Squashfs is a highly compressed read-only filesystem for Linux."
SECTION = "base"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://mksquashfs.c;beginline=4;endline=20;md5=a02792b0d0958b34d7afedd7f994d075"
DEPENDS = "attr zlib"
INC_PR = "r5"

S = "${WORKDIR}/squashfs${@bb.data.getVar('PV',d,1).replace('r','-r')}/squashfs-tools"

BBCLASSEXTEND = "native"
NATIVE_INSTALL_WORKS = "1"

# required to share same place with -lzma specific packages
FILESPATHPKG =. "squashfs-tools-${PV}:"

SRC_URI ?= "${SOURCEFORGE_MIRROR}/squashfs/squashfs${@bb.data.getVar('PV',d,1).replace('r','-r')}.tar.gz"

prefix = ""

do_compile() {
	oe_runmake mksquashfs
}

do_install () {
	install -d ${D}${sbindir}
	install -m 0755 mksquashfs ${D}${sbindir}/
}

