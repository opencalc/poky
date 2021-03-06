#
# BitBake Graphical GTK User Interface
#
# Copyright (C) 2011        Intel Corporation
#
# Authored by Joshua Lock <josh@linux.intel.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import gtk
from bb.ui.crumbs.configurator import Configurator

class HobPrefs(gtk.Dialog):
    """
    """
    def empty_combo_text(self, combo_text):
        model = combo_text.get_model()
        if model:
            model.clear()

    def output_type_changed_cb(self, combo, handler):
        ot = combo.get_active_text()
        if ot != self.curr_output_type:
            self.curr_output_type = ot
            handler.set_image_output_type(ot)

    def sdk_machine_combo_changed_cb(self, combo, handler):
        sdk_mach = combo.get_active_text()
	if sdk_mach != self.curr_sdk_mach:
            self.curr_sdk_mach = sdk_mach
            self.configurator.setLocalConfVar('SDKMACHINE', sdk_mach)
            handler.set_sdk_machine(sdk_mach)

    def update_sdk_machines(self, handler, sdk_machines):
        active = 0
        # disconnect the signal handler before updating the combo model
        if self.sdk_machine_handler_id:
            self.sdk_machine_combo.disconnect(self.sdk_machine_handler_id)
            self.sdk_machine_handler_id = None

        self.empty_combo_text(self.sdk_machine_combo)
        for sdk_machine in sdk_machines:
            self.sdk_machine_combo.append_text(sdk_machine)
            if sdk_machine == self.curr_sdk_mach:
                self.sdk_machine_combo.set_active(active)
            active = active + 1

        self.sdk_machine_handler_id = self.sdk_machine_combo.connect("changed", self.sdk_machine_combo_changed_cb, handler)

    def distro_combo_changed_cb(self, combo, handler):
        distro = combo.get_active_text()
	if distro != self.curr_distro:
            self.curr_distro = distro
            self.configurator.setLocalConfVar('DISTRO', distro)
            handler.set_distro(distro)
            self.reload_required = True

    def update_distros(self, handler, distros):
        active = 0
        # disconnect the signal handler before updating combo model
        if self.distro_handler_id:
            self.distro_combo.disconnect(self.distro_handler_id)
            self.distro_handler_id = None

        self.empty_combo_text(self.distro_combo)
	for distro in distros:
	    self.distro_combo.append_text(distro)
	    if distro == self.curr_distro:
                self.distro_combo.set_active(active)
	    active = active + 1

	self.distro_handler_id = self.distro_combo.connect("changed", self.distro_combo_changed_cb, handler)

    def package_format_combo_changed_cb(self, combo, handler):
        package_format = combo.get_active_text()
        if package_format != self.curr_package_format:
            self.curr_package_format = package_format
            self.configurator.setLocalConfVar('PACKAGE_CLASSES', 'package_%s' % package_format)
            handler.set_package_format(package_format)

    def update_package_formats(self, handler, formats):
        active = 0
        # disconnect the signal handler before updating the model
        if self.package_handler_id:
            self.package_combo.disconnect(self.package_handler_id)
            self.package_handler_id = None

        self.empty_combo_text(self.package_combo)
        for format in formats:
            self.package_combo.append_text(format)
            if format == self.curr_package_format:
                self.package_combo.set_active(active)
            active = active + 1

        self.package_handler_id = self.package_combo.connect("changed", self.package_format_combo_changed_cb, handler)
    
    def include_gplv3_cb(self, toggle):
        excluded = toggle.get_active()
        self.handler.toggle_gplv3(excluded)
        if excluded:
            self.configurator.setLocalConfVar('INCOMPATIBLE_LICENSE', 'GPLv3')
        else:
            self.configurator.setLocalConfVar('INCOMPATIBLE_LICENSE', '')
        self.reload_required = True

    def change_bb_threads_cb(self, spinner):
        val = spinner.get_value_as_int()
        self.handler.set_bbthreads(val)
        self.configurator.setLocalConfVar('BB_NUMBER_THREADS', val)

    def change_make_threads_cb(self, spinner):
        val = spinner.get_value_as_int()
        self.handler.set_pmake(val)
        self.configurator.setLocalConfVar('PARALLEL_MAKE', "-j %s" % val)

    def toggle_toolchain_cb(self, check):
        enabled = check.get_active()
        self.handler.toggle_toolchain(enabled)

    def toggle_headers_cb(self, check):
        enabled = check.get_active()
        self.handler.toggle_toolchain_headers(enabled)

    def set_parent_window(self, parent):
        self.set_transient_for(parent)

    def write_changes(self):
        self.configurator.writeLocalConf()

    def prefs_response_cb(self, dialog, response):
        if self.reload_required:
            glib.idle_add(self.handler.reload_data)

    def __init__(self, configurator, handler, curr_sdk_mach, curr_distro, pclass,
                 cpu_cnt, pmake, bbthread, image_types):
        """
        """
        gtk.Dialog.__init__(self, "Preferences", None,
                            gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CLOSE, gtk.RESPONSE_OK))

        self.set_border_width(6)
        self.vbox.set_property("spacing", 12)
        self.action_area.set_property("spacing", 12)
        self.action_area.set_property("border-width", 6)

        self.handler = handler
        self.configurator = configurator

        self.curr_sdk_mach = curr_sdk_mach
        self.curr_distro = curr_distro
        self.curr_package_format = pclass
        self.curr_output_type = None
        self.cpu_cnt = cpu_cnt
        self.pmake = pmake
        self.bbthread = bbthread
        self.reload_required = False
        self.distro_handler_id = None
        self.sdk_machine_handler_id = None
        self.package_handler_id = None

        left = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)
        right = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)

        label = gtk.Label()
        label.set_markup("<b>Policy</b>")
        label.show()
        frame = gtk.Frame()
        frame.set_label_widget(label)
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.show()
        self.vbox.pack_start(frame)
        pbox = gtk.VBox(False, 12)
        pbox.show()
        frame.add(pbox)
        hbox = gtk.HBox(False, 12)
        hbox.show()
        pbox.pack_start(hbox, expand=False, fill=False, padding=6)
        # Distro selector
        label = gtk.Label("Distribution:")
        label.show()
        hbox.pack_start(label, expand=False, fill=False, padding=6)
        self.distro_combo = gtk.combo_box_new_text()
        self.distro_combo.set_tooltip_text("Select the Yocto distribution you would like to use")
        self.distro_combo.show()
        hbox.pack_start(self.distro_combo, expand=False, fill=False, padding=6)
        # Exclude GPLv3
        check = gtk.CheckButton("Exclude GPLv3 packages")
        check.set_tooltip_text("Check this box to prevent GPLv3 packages from being included in your image")
        check.show()
        check.connect("toggled", self.include_gplv3_cb)
        hbox.pack_start(check, expand=False, fill=False, padding=6)
        hbox = gtk.HBox(False, 12)
        hbox.show()
        pbox.pack_start(hbox, expand=False, fill=False, padding=6)
        # Package format selector
        label = gtk.Label("Package format:")
        label.show()
        hbox.pack_start(label, expand=False, fill=False, padding=6)
        self.package_combo = gtk.combo_box_new_text()
        self.package_combo.set_tooltip_text("Select the package format you would like to use in your image")
        self.package_combo.show()
        hbox.pack_start(self.package_combo, expand=False, fill=False, padding=6)
        # Image output type selector
        label = gtk.Label("Image output type:")
        label.show()
        hbox.pack_start(label, expand=False, fill=False, padding=6)
        output_combo = gtk.combo_box_new_text()
        if image_types:
            for it in image_types.split(" "):
                output_combo.append_text(it)
            output_combo.connect("changed", self.output_type_changed_cb, handler)
        else:
            output_combo.set_sensitive(False)
        output_combo.show()
        hbox.pack_start(output_combo)
        # BitBake
        label = gtk.Label()
        label.set_markup("<b>BitBake</b>")
        label.show()
        frame = gtk.Frame()
        frame.set_label_widget(label)
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.show()
        self.vbox.pack_start(frame)
        pbox = gtk.VBox(False, 12)
        pbox.show()
        frame.add(pbox)
        hbox = gtk.HBox(False, 12)
        hbox.show()
        pbox.pack_start(hbox, expand=False, fill=False, padding=6)
        label = gtk.Label("BitBake threads:")
        label.show()
        spin_max = 9 #self.cpu_cnt * 3
        hbox.pack_start(label, expand=False, fill=False, padding=6)
        bbadj = gtk.Adjustment(value=self.bbthread, lower=1, upper=spin_max, step_incr=1)
        bbspinner = gtk.SpinButton(adjustment=bbadj, climb_rate=1, digits=0)
        bbspinner.show()
        bbspinner.connect("value-changed", self.change_bb_threads_cb)
        hbox.pack_start(bbspinner, expand=False, fill=False, padding=6)
        label = gtk.Label("Make threads:")
        label.show()
        hbox.pack_start(label, expand=False, fill=False, padding=6)
        madj = gtk.Adjustment(value=self.pmake, lower=1, upper=spin_max, step_incr=1)
        makespinner = gtk.SpinButton(adjustment=madj, climb_rate=1, digits=0)
        makespinner.connect("value-changed", self.change_make_threads_cb)
        makespinner.show()
        hbox.pack_start(makespinner, expand=False, fill=False, padding=6)
        # Toolchain
        label = gtk.Label()
        label.set_markup("<b>External Toolchain</b>")
        label.show()
        frame = gtk.Frame()
        frame.set_label_widget(label)
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.show()
        self.vbox.pack_start(frame)
        pbox = gtk.VBox(False, 12)
        pbox.show()
        frame.add(pbox)
        hbox = gtk.HBox(False, 12)
        hbox.show()
        pbox.pack_start(hbox, expand=False, fill=False, padding=6)
        toolcheck = gtk.CheckButton("Build external development toolchain with image")
        toolcheck.show()
        toolcheck.connect("toggled", self.toggle_toolchain_cb)
        hbox.pack_start(toolcheck, expand=False, fill=False, padding=6)
        hbox = gtk.HBox(False, 12)
        hbox.show()
        pbox.pack_start(hbox, expand=False, fill=False, padding=6)
        label = gtk.Label("Toolchain host:")
        label.show()
        hbox.pack_start(label, expand=False, fill=False, padding=6)
        self.sdk_machine_combo = gtk.combo_box_new_text()
        self.sdk_machine_combo.set_tooltip_text("Select the host architecture of the external machine")
        self.sdk_machine_combo.show()
        hbox.pack_start(self.sdk_machine_combo, expand=False, fill=False, padding=6)
        headerscheck = gtk.CheckButton("Include development headers with toolchain")
        headerscheck.show()
        headerscheck.connect("toggled", self.toggle_headers_cb)
        hbox.pack_start(headerscheck, expand=False, fill=False, padding=6)
        self.connect("response", self.prefs_response_cb)
