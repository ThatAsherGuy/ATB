# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import os
import rna_keymap_ui
from . dicts import keys as keysdict
from . dicts import keys_for_humans as humankeysdict

# Keymap stuff stolen from MESHmachine
# Get Machine's addons, they're awesome!


def get_path():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_name():
    return os.path.basename(get_path())


def get_prefs():
    return bpy.context.preferences.addons[get_name()].preferences


def get_keys(dictname="keysdict"):
    if dictname == "keysdict":
        keydict = keysdict
    elif dictname == "humankeysdict":
        keydict = humankeysdict
    keylists = []

    keylists.append(keydict["PIES"])
    keylists.append(keydict["MENUS"])
    keylists.append(keydict["PANELS"])
    keylists.append(keydict["OPERATORS"])

    return keylists


def restore_keymaps(keylists, debug=False):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if debug:
        print("++++++")
        print("Top-Level List Count: " + str(len(keylists)))

    for keylist in keylists:

        for item in keylist:
            keymap = item.get("keymap")
            space_type = item.get("space_type", "EMPTY")

            if debug:
                print("     " + str(item.get("idname")) + ": " + str(keymap) + " | " + str(space_type))

            if keymap:
                km = kc.keymaps.find(name=keymap, space_type=space_type)

                if km:
                    idname = item.get("idname")
                    # type = item.get("type")
                    # value = item.get("value")

                    # shift = item.get("shift", False)
                    # ctrl = item.get("ctrl", False)
                    # alt = item.get("alt", False)

                    kmi = km.keymap_items.find_from_operator(
                                                            idname,
                                                            )

                    if kmi:
                        if debug:
                            print("Item Found: " + str(kmi.idname))
                            print("     User Defined: " + str(kmi.is_user_defined))
                            print("     User Modified: " + str(kmi.is_user_modified))

                    else:
                        if debug:
                            print("Missing Item: " + str(item.get("idname")))

    if debug:
        print("++++++\n")


def register_keymaps(keylists):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    refmap = wm.keyconfigs.active
    # kc = wm.keyconfigs.user
    debug = 0

    keymaps = []
    i = 1

    for keylist in keylists:
        for item in keylist:
            keymap = item.get("keymap")
            space_type = item.get("space_type", "EMPTY")
            if debug == 2:
                print("Items Added: ", i)
                print(str(keymap) + " | " + str(space_type))

            if keymap:
                i += 1

                ref = refmap.keymaps.find(name=str(keymap), space_type=space_type)
                # if debug == 2:
                #     print("KM Found: " + str(km.name))

                if ref:
                    km = kc.keymaps.new(name=str(keymap), space_type=space_type)

                    idname = item.get("idname")
                    type = item.get("type")
                    value = item.get("value")

                    shift = item.get("shift", False)
                    ctrl = item.get("ctrl", False)
                    alt = item.get("alt", False)

                    kmi = km.keymap_items.new(idname, type, value, shift=shift, ctrl=ctrl, alt=alt)

                    if debug == 1:
                        print(str(kmi.idname)
                              + " | "
                              + "Is Active: " + str(kmi.name)
                              + " | "
                              + str(kmi.type)
                              )

                    if kmi:
                        properties = item.get("properties")

                        if properties:
                            for name, value in properties:
                                setattr(kmi.properties, name, value)

                        keymaps.append((km, kmi))
                else:
                    print("Keymap Not Found: " + keymap)
            else:
                print("KM Not Found for " + str(item.get("idname")))
    return keymaps


def unregister_keymaps(keymaps):
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)


def draw_keymap_items(kc, name, keylist, layout, debug=False):
    drawn = False

    for item in keylist:
        keymap = item.get("keymap")

        if debug:
            print("+++++ \n" + str(item.get("idname")))
            print(str(keymap))

        if keymap:
            km = kc.keymaps.get(keymap)

            if debug:
                print(str(km) + "\n+++++ \n")

            kmi = None
            if km:
                idname = item.get("idname")

                for kmitem in km.keymap_items:
                    if kmitem.idname == idname:
                        properties = item.get("properties")

                        if properties:
                            if all(
                                    [getattr(kmitem.properties, name, None)
                                        == value for name, value in properties]):
                                kmi = kmitem
                                break

                        else:
                            kmi = kmitem
                            break

            # draw keymap item

            if kmi:
                box = layout.column()
                if debug:
                    pre = box.column()
                    pre.label(text=str(kmi.idname))
                    pre.label(text=str(keymap))

                col = box.column()

                rna_keymap_ui.draw_kmi(["ADDON", "USER", "DEFAULT"], kc, km, kmi, col, 0)

                drawn = True

    return drawn


def get_keymap_item(name, idname, key, alt=False, ctrl=False, shift=False):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    km = kc.keymaps.get(name)
    kmi = km.keymap_items.get(idname)

    if kmi:
        if all([kmi.type == key and kmi.alt is alt and kmi.ctrl is ctrl and kmi.shift is shift]):
            return True
    return False


def update_panel(self, context):
    message = "Asher's Custom Tools: Panel update has failed"

    panels = (
            ATB_PT_ViewOverlaysPanel,
            )

    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        for panel in panels:
            panel.bl_category = context.preferences.addons[__name__].preferences.category
            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass


class ATBAddonPreferences(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    path = get_path()
    bl_idname = __package__

    prefs_tab_items = [
                        ("GENERAL", "General", ""),
                        ("KEYS", "Keymap", ""),
                        # ("ABOUT", "About", "")
                      ]

    prefs_baseKeymap_items = [
                              ("ASHER", "Asher's Config",
                               "Restart Blender or click the "
                               "refresh button on the right to enable"),
                              ("HUMANS", "Basic Config",
                               "Restart Blender or click the "
                               "refresh button on the right to enable"),
                              # ("ABOUT", "About", "")
                             ]

    tabs: bpy.props.EnumProperty(
                                name="Tabs",
                                items=prefs_tab_items,
                                default="GENERAL",
                                )

    baseKeymap: bpy.props.EnumProperty(
                                name="Tabs",
                                items=prefs_baseKeymap_items,
                                default="HUMANS",
                                )

    category: bpy.props.StringProperty(
            name="Tab Category",
            description="Choose a name for the category of the panel",
            default="Dev",
            update=update_panel
            )

    def draw_keymaps(self, layout, kmap=0, debug=False):
        wm = bpy.context.window_manager

        # Hacky selector to change what key config we're showing
        if kmap == 0:
            kc = wm.keyconfigs.addon
        elif kmap == 1:
            kc = wm.keyconfigs.active
        elif kmap == 2:
            kc = wm.keyconfigs.user

        from . dicts import keys as keysdict
        from . dicts import keys_for_humans as humankeysdict

        column = layout.column(align=True)
        column.separator()

        header = column.row(align=False)
        header.label(text="Base Keymap")
        header.prop(self, "baseKeymap", expand=True)
        header.operator(
            "script.reload",
            text="",
            icon='FILE_REFRESH'
        )

        column.separator()

        if debug:
            # for item in keysdict.items():
            #     print(str(item[1][0]))
            #     print("----- + -----")
            debug = False

        if self.baseKeymap == 'ASHER':
            for name, keylist in keysdict.items():
                draw_keymap_items(kc, name, keylist, column, debug)
        else:
            for name, keylist in humankeysdict.items():
                draw_keymap_items(kc, name, keylist, column, debug)

    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)
        row = column.row(align=True)
        row.prop(self, "tabs", expand=True)

        box = column.column(align=True)

        if self.tabs == "GENERAL":
            self.draw_general_tab(box)
        elif self.tabs == "KEYS":
            self.draw_keymap_tab(box)
        # elif self.tabs == "ABOUT":
        #     self.draw_about_tab(box)

    def draw_general_tab(self, box):
        col = box.column(align=True)

        col.separator(factor=2)

        labelrow = col.row(align=True)
        labelrow.alignment = 'CENTER'
        labelrow.label(text="ATB Sidebar Tab:"
                            ""
                            ""
                            "")

        subcol = col.column(align=True)

        subrow = subcol.split(factor=0.2)
        subrow.label(text="Overlays:")
        subrow.label(text="A massive panel "
                          "with (almost) every overlay "
                          "setting")

        subrow = subcol.split(factor=0.2)
        subrow.label(text="Fast Panel:")
        subrow.label(text="A tabbed panel with "
                          "common viewport settings"
                          "")

        subrow = subcol.split(factor=0.2)
        subrow.label(text="Meta Panel:")
        subrow.label(text="A tabbed panel/popover with "
                          "Overlays, Object Properties, etc, "
                          "for fullscreen modeling"
                          "")

        col.separator(factor=2)

        labelrow = col.row(align=True)
        labelrow.alignment = 'CENTER'
        labelrow.label(text="Pies:"
                            ""
                            ""
                            "")

        subcol = col.column(align=True)

        subrow = subcol.split(factor=0.2)
        subrow.label(text="ATB View Pie:")
        subrow.label(text="Viewport snapping, "
                          "Rotation Modes, "
                          "and related settings")

        subrow = subcol.split(factor=0.2)
        subrow.label(text="ATB Selection Pie:")
        subrow.label(text="Select Inner/Outer, "
                          "Flat Faces, Loops, NGons, etc"
                          "")

        subrow = subcol.split(factor=0.2)
        subrow.label(text="ATB Transform Pie:")
        subrow.label(text="Toggle or cycle common "
                          "transformation settings "
                          "(snapping mode, pivot, etc)")

        subrow = subcol.split(factor=0.2)
        subrow.label(text="ATB Orientation Pie:")
        subrow.label(text="Switch between various "
                          "transform orientations "
                          "")

        subrow = subcol.split(factor=0.2)
        subrow.label(text="ATB Cursor Pie:")
        subrow.label(text="Does 3D Cursor Things"
                          ""
                          "")

        col.separator(factor=2)

        labelrow = col.row(align=True)
        labelrow.alignment = 'CENTER'
        labelrow.label(text="Menus:"
                            ""
                            ""
                            "")

        subcol = col.column(align=True)

        subrow = subcol.split(factor=0.2)
        subrow.label(text="ATB Modeling Menu:")
        subrow.label(text="A shortlist of common "
                          "operators, with shortcuts for "
                          "quick access")

        col.separator(factor=2)

        labelrow = col.row(align=True)
        labelrow.alignment = 'CENTER'
        labelrow.label(text="Operators:"
                            ""
                            ""
                            "")

        subcol = col.column(align=True)

        subrow = subcol.split(factor=0.2)
        subrow.label(text="ATB Set Axis:")
        subrow.label(text="Snaps the viewport to an "
                          "isometric angle"
                          "")

    def draw_keymap_tab(self, box, debug=False):

        split = box.split()
        b = split.box()
        self.draw_keymaps(b, 2, True)

    # def draw_about_tab(self, box):
    #     split = box.split()
    #     b = split.box()
    #     self.draw_keymaps(b)
