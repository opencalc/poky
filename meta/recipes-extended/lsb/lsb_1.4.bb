DESCRIPTION = "LSB support for Poky Linux"
SECTION = "console/utils"
HOMEPAGE = "http://prdownloads.sourceforge.net/lsb"
PRIORITY = "required"
LICENSE = "GPLv2+"
PR = "r0"

LIC_FILES_CHKSUM = "file://README;md5=12da544b1a3a5a1795a21160b49471cf"

SRC_URI = "http://cdnetworks-kr-1.dl.sourceforge.net/project/lsb/lsb_release/${PV}/lsb-release-${PV}.tar.gz"
S = ${WORKDIR}/lsb-release-${PV}

do_install(){
	oe_runmake install prefix=${D}  mandir=${D}/man/ DESTDIR=${D} 
	mkdir -p ${D}/bin
	mkdir -p ${D}/lib
	mkdir -p ${D}/etc/lsb-release.d
	echo -n "LSB_VERSION=\"core-2.0-noarch:core-3.2-noarch:core-4.0-noarch:" > ${D}/etc/lsb-release
	
	if [ "${TARGET_ARCH}" == "i586" ];then
		echo -n "core-2.0-ia32:core-3.2-ia32:core-4.0-ia32" >>  ${D}/etc/lsb-release
	else
		echo -n "core-2.0-${TARGET_ARCH}:core-3.2-${TARGET_ARCH}:core-4.0-${TARGET_ARCH}" >>  ${D}/etc/lsb-release
	fi
	echo "\"" >> ${D}/etc/lsb-release
	
	if [ "${TARGET_ARCH}" == "i586" ];then
		mkdir -p ${D}/etc/lsb-release.d
		touch ${D}/etc/lsb-release.d/graphics-2.0-noarch
		touch ${D}/etc/lsb-release.d/graphics-3.2-noarch
		touch ${D}/etc/lsb-release.d/graphics-${PV}-noarch
		touch ${D}/etc/lsb-release.d/desktop-${PV}-noarch
		touch ${D}/etc/lsb-release.d/graphics-2.0-ia32
		touch ${D}/etc/lsb-release.d/graphics-3.2-ia32
		touch ${D}/etc/lsb-release.d/graphics-${PV}-ia32
		touch ${D}/etc/lsb-release.d/desktop-${PV}-ia32
	elif [ "${TARGET_ARCH}" == "x86_64" ];then
		touch ${D}/etc/lsb-release.d/graphics-2.0-amd64
		touch ${D}/etc/lsb-release.d/graphics-3.2-amd64
		touch ${D}/etc/lsb-release.d/graphics-${PV}-amd64
		touch ${D}/etc/lsb-release.d/desktop-${PV}-amd64
	fi
	if [ "${TARGET_ARCH}" = "powerpc" ];then
		touch ${D}/etc/lsb-release.d/graphics-2.0-ppc32
		touch ${D}/etc/lsb-release.d/graphics-3.2-ppc32
		touch ${D}/etc/lsb-release.d/graphics-${PV}-ppc32
		touch ${D}/etc/lsb-release.d/desktop-${PV}-ppc32
	elif [ "${TARGET_ARCH}" = "powerpc64" ];then
		touch ${D}/etc/lsb-release.d/graphics-2.0-ppc64
		touch ${D}/etc/lsb-release.d/graphics-3.2-ppc64
		touch ${D}/etc/lsb-release.d/graphics-${PV}-ppc64
		touch ${D}/etc/lsb-release.d/desktop-${PV}-ppc64
	fi
}

do_install_append(){
       if [ "${TARGET_ARCH}" == "x86_64" ];then
	       cd ${D}
	       ln -sf lib lib64
	       cd ${D}/lib
               ln -sf ld-linux-x86-64.so.2 ld-lsb-x86-64.so.2
               ln -sf ld-linux-x86-64.so.2 ld-lsb-x86-64.so.3
       fi
       if [ "${TARGET_ARCH}" == "i586" ];then
	       cd ${D}/lib
               ln -sf ld-linux.so.2 ld-lsb.so.2
               ln -sf ld-linux.so.2 ld-lsb.so.3
       fi
 
       if [ "${TARGET_ARCH}" == "powerpc64" ];then
  	       cd ${D}
	       ln -sf lib lib64
               cd ${D}/lib
               ln -sf ld64.so.1 ld-lsb-ppc64.so.2
               ln -sf ld64.so.1 ld-lsb-ppc64.so.3
       fi
       if [ "${TARGET_ARCH}" == "powerpc" ];then
	       cd ${D}/lib
               ln -sf ld.so.1 ld-lsb-ppc32.so.2
               ln -sf ld.so.1 ld-lsb-ppc32.so.3
       fi	
}
FILES_${PN} += "/lib64"