DESCRIPTION = "Lua is a powerful light-weight programming language designed \
for extending applications."
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYRIGHT;md5=e591ac54022d729e190c3465c191c2b6"
HOMEPAGE = "http://www.lua.org/"

PR = "r6"

SRC_URI = "http://luajit.org/download/LuaJIT-${PV}.tar.gz"
SRC_URI += "http://luajit.org/download/beta8_hotfix1.patch"

S = "${WORKDIR}/LuaJIT-${PV}"

inherit pkgconfig binconfig update-alternatives

# need to install lib32c-dev on ubuntu

TARGET_CC_ARCH += " -fPIC ${LDFLAGS}"
EXTRA_OEMAKE = "HOST_CC='gcc -m32' CROSS=${TARGET_PREFIX} TARGET=${TARGET_ARCH}"

ALTERNATIVE_NAME = "lua"
ALTERNATIVE_PATH = "${bindir}/luajit-${PV}"
ALTERNATIVE_LINK = "${bindir}/lua"
ALTERNATIVE_PRIORITY = "20"

do_configure_prepend() {
	sed -i -e s:/usr/local:${prefix}:g src/luaconf.h
}

do_compile () {
	oe_runmake
}

do_install () {
	oe_runmake install DESTDIR=${D} PREFIX=/usr
}

NATIVE_INSTALL_WORKS = 1
BBCLASSEXTEND = "native"
