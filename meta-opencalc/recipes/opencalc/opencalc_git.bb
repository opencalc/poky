DESCRIPTION = "Opencalc application"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=b234ee4d69f5fce4486a80fdaf4a4263"
HOMEPAGE = "http://www.opencalc.me"

DEPENDS="luajit cairo mpfr"

RDEPENDS="liblua5.1-filesystem"

PR = "r3"

SRC_URI = "git://github.com/opencalc/opencalc.git;protocol=git"
SRCREV = "HEAD"

S = "${WORKDIR}/git"

TARGET_CC_ARCH += "${LDFLAGS}"

EXTRA_OEMAKE = "UI=fb LUAPKG=luajit"

do_install() {
	OPTDIR=${D}/opt/opencalc

	for F in $(cd ${S}; find . -name \*.so); do
		mkdir -p ${OPTDIR}/$(dirname $F)
		install -m 0755 ${S}/${F} ${OPTDIR}/${F}
	done

	for F in $(cd ${S}; find . -name \*.lua); do
		mkdir -p ${OPTDIR}/$(dirname $F)
		install -m 0644 ${S}/${F} ${OPTDIR}/${F}
	done
}

PACKAGES = "${PN} ${PN}-dbg"

FILES_${PN}-dbg = "/opt/opencalc/.debug/*"
FILES_${PN} = "/opt/opencalc"
