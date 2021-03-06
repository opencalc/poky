SUMMARY = "The Cairo 2D vector graphics library"
DESCRIPTION = "Cairo is a multi-platform library providing anti-aliased \
vector-based rendering for multiple target backends. Paths consist \
of line segments and cubic splines and can be rendered at any width \
with various join and cap styles. All colors may be specified with \
optional translucence (opacity/alpha) and combined using the \
extended Porter/Duff compositing algebra as found in the X Render \
Extension."
HOMEPAGE = "http://cairographics.org"
BUGTRACKER = "http://bugs.freedesktop.org"
SECTION = "libs"
LICENSE = "MPL-1 & LGPLv2.1"
DEPENDS = "libpng fontconfig pixman"

#check for TARGET_FPU=soft and inform configure of the result so it can disable some floating points 
require cairo-fpu.inc
EXTRA_OECONF += "${@get_cairo_fpu_setting(bb, d)}"

inherit autotools pkgconfig
