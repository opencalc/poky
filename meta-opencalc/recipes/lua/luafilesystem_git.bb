DESCRIPTION = "LUA filesystem"
SECTION = "libs"
LICENSE = "Kepler"
LIC_FILES_CHKSUM = "file://doc/us/license.html;md5=8bdace4588f41a2e7ba5cdf220545a3e"

DEPENDS = "luajit"

SRC_URI = "git://github.com/keplerproject/luafilesystem.git;protocol=git"
SRCREV = "HEAD"

S = "${WORKDIR}/git"

TARGET_CC_ARCH += "${LDFLAGS}"

EXTRA_OEMAKE = "CC='${CC}' INCS=$(pkg-config --cflags luajit) PLATFORM=linux"

do_install() {
	oe_runmake install LUA_LIBDIR=${D}/${libdir}/lua/5.1
}

PACKAGES = "liblua5.1-filesystem-dbg liblua5.1-filesystem"

FILES_liblua5.1-filesystem-dbg = "${libdir}/lua/5.1/.debug"
FILES_liblua5.1-filesystem = "${libdir} ${datadir}"
