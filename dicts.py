# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Hell is other people's code.

# These dictionaries are what I use to store the 'default' keymaps.
# I'll eventually use some sort of JSON format for this.
# You can (and should) modify them to fit your needs.

keys = {"PIES": [{"label": "3D View Global",
                  "keymap": "3D View",
                  "space_type": "VIEW_3D",
                  "idname": "wm.call_menu_pie",
                  "type": "F16",
                  "value": "PRESS",
                  "properties": [("name", "VIEW3D_MT_ATB_view_pie")]},

                 {"label": "3D View Global",
                  "keymap": "3D View",
                  "space_type": "VIEW_3D",
                  "idname": "wm.call_menu_pie",
                  "type": "F13",
                  "value": "PRESS",
                  "properties": [("name", "VIEW3D_MT_PIE_quick_snap")]},

                 {"label": "3D View Global",
                  "keymap": "3D View",
                  "space_type": "VIEW_3D",
                  "idname": "atb.meta_pie",
                  "type": "F19",
                  "value": "CLICK_DRAG",
                  },

                 {"label": "3D View Global",
                  "keymap": "3D View",
                  "space_type": "VIEW_3D",
                  "idname": "wm.call_menu_pie",
                  "type": "F17",
                  "value": "PRESS",
                  "properties": [("name", "VIEW3D_MT_PIE_quick_orientation")]},

                 {"label": "3D View Global",
                  "keymap": "3D View",
                  "space_type": "VIEW_3D",
                  "idname": "atb.super_tablet_pie",
                  "type": "RIGHTMOUSE",
                  "alt": True,
                  "shift": True,
                  "ctrl": True,
                  "value": "DOUBLE_CLICK"},

                 {"label": "3D View Global",
                  "keymap": "3D View",
                  "space_type": "VIEW_3D",
                  "idname": "atb.mod_pie",
                  "type": "F14",
                  "value": "PRESS"},

                 {"label": "3D View Global",
                  "keymap": "3D View",
                  "space_type": "VIEW_3D",
                  "idname": "atb.save_pie",
                  "type": "S",
                  "ctrl": True,
                  "value": "PRESS"},

                 {"label": "3D View Global",
                  "keymap": "3D View",
                  "space_type": "VIEW_3D",
                  "idname": "wm.call_menu_pie",
                  "type": "F19",
                  "value": "DOUBLE_CLICK",
                  "properties": [("name", "VIEW3D_MT_ATB_cursor_pie")]}],

        "MENUS": [{"label": "3D View Global",
                   "keymap": "Mesh",
                   "space_type": "EMPTY",
                   "idname": "wm.call_menu",
                   "type": "F19",
                   "alt": True,
                   "shift": True,
                   "value": "PRESS",
                   "properties": [("name", "VIEW3D_MT_actc_root")]}],

        "PANELS": [{"label": "3D View Global",
                    "keymap": "3D View",
                    "space_type": "VIEW_3D",
                    "idname": "wm.call_panel",
                    "type": "F20",
                    "value": "PRESS",
                    "properties": [("name", "VIEW3D_PT_view3d_fast_panel")]},

                   {"label": "3D View Global",
                    "keymap": "3D View",
                    "space_type": "VIEW_3D",
                    "idname": "wm.call_panel",
                    "type": "F18",
                    "value": "PRESS",
                    "properties": [("name", "VIEW3D_PT_meta_panel")]}],

        "OPERATORS": [{"label": "3D View Global",
                       "keymap": "3D View",
                       "space_type": "VIEW_3D",
                       "idname": "atb.set_axis",
                       "type": "PAGE_DOWN",
                       "alt": True,
                       "value": "PRESS",
                       },

                      {"label": "3D View Global",
                       "keymap": "3D View",
                       "space_type": "VIEW_3D",
                       "idname": "atb.super_select",
                       "type": "F15",
                       "value": "PRESS"},

                      {"label": "3D View Global",
                       "keymap": "3D View",
                       "space_type": "VIEW_3D",
                       "idname": "atb.tap_it",
                       "type": "F21",
                       "value": "PRESS"},

                      {"label": "3D View Edit Mesh",
                       "keymap": "3D View",
                       "space_type": "VIEW_3D",
                       "idname": "atb.quick_symmetry",
                       "type": "MIDDLEMOUSE",
                       "value": "DOUBLE_CLICK",
                       "ctrl": True,
                       "properties": [("do_modal",
                                        True)]},

                      {"label": "3D View Global",
                       "keymap": "3D View",
                       "space_type": "VIEW_3D",
                       "idname": "atb.view_axis",
                       "type": "F16",
                       "ctrl": True,
                       "alt": True,
                       "value": "PRESS"},

                      {"label": "3D View Edit Mesh",
                       "keymap": "Mesh",
                       "space_type": "EMPTY",
                       "idname": "atb.add_to_mode",
                       "type": "F16",
                       "ctrl": True,
                       "value": "PRESS"},

                      {"label": "3D View Global",
                       "keymap": "3D View",
                       "space_type": "VIEW_3D",
                       "idname": "view3d.move",
                       "type": "F22",
                       "value": "PRESS"},

                      {"label": "3D View Global",
                       "keymap": "3D View",
                       "space_type": "VIEW_3D",
                       "idname": "view3d.zoom",
                       "type": "F22",
                       "value": "DOUBLE_CLICK"},

                      {"label": "3D View Global",
                       "keymap": "3D View",
                       "space_type": "VIEW_3D",
                       "idname": "view3d.rotate",
                       "type": "F23",
                       "value": "PRESS"},

                      {"label": "3D View Global",
                       "keymap": "3D View",
                       "space_type": "VIEW_3D",
                       "idname": "atb.context_modal_mouse",
                       "type": "F23",
                       "ctrl": True,
                       "value": "PRESS"},

                      {"label": "3D View Global",
                       "keymap": "3D View",
                       "space_type": "VIEW_3D",
                       "idname": "atb.drop_tool",
                       "type": "ESC",
                       "value": "PRESS"},

                      {"label": "3D View Global",
                       "keymap": "3D View",
                       "space_type": "VIEW_3D",
                       "idname": "atb.group_select",
                       "type": "F14",
                       "ctrl": True,
                       "alt": True,
                       "value": "PRESS"}]
        }

keys_for_humans = {"PIES": [{"label": "3D View Global",
                             "keymap": "3D View",
                             "space_type": "VIEW_3D",
                             "idname": "wm.call_menu_pie",
                             "type": "MIDDLEMOUSE",
                             "value": "DOUBLE_CLICK",
                             "properties": [("name",
                                             "VIEW3D_MT_ATB_view_pie")]},

                            {"label": "3D View Global",
                             "keymap": "3D View",
                             "space_type": "VIEW_3D",
                             "idname": "wm.call_menu_pie",
                             "type": "T",
                             "value": "PRESS",
                             "shift": True,
                             "properties": [("name",
                                             "VIEW3D_MT_PIE_quick_snap")]},

                            {"label": "3D View Global",
                             "keymap": "3D View",
                             "space_type": "VIEW_3D",
                             "idname": "wm.call_menu_pie",
                             "type": "F7",
                             "value": "PRESS",
                             "properties": [("name",
                                            "VIEW3D_MT_PIE_quick_orientation")]},

                            {"label": "3D View Global",
                             "keymap": "3D View",
                             "space_type": "VIEW_3D",
                             "idname": "wm.call_menu_pie",
                             "type": "D",
                             "ctrl": True,
                             "value": "PRESS",
                             "properties": [("name",
                                             "VIEW3D_MT_ATB_cursor_pie")]}],

                   "MENUS": [{"label": "3D View Global",
                              "keymap": "Mesh",
                              "space_type": "EMPTY",
                              "idname": "wm.call_menu",
                              "type": "F6",
                              "value": "PRESS",
                              "properties": [("name",
                                              "VIEW3D_MT_actc_root")]}],

                   "PANELS": [{"label": "3D View Global",
                               "keymap": "3D View",
                               "space_type": "VIEW_3D",
                               "idname": "wm.call_panel",
                               "type": "Q",
                               "alt": True,
                               "value": "PRESS",
                               "properties": [("name",
                                               "VIEW3D_PT_view3d_fast_panel")]},

                              {"label": "3D View Global",
                               "keymap": "3D View",
                               "space_type": "VIEW_3D",
                               "idname": "wm.call_panel",
                               "type": "Q",
                               "alt": True,
                               "shift": True,
                               "value": "PRESS",
                               "properties": [("name",
                                               "VIEW3D_PT_meta_panel")]}],

                   "OPERATORS": [{"label": "3D View Global",
                                  "keymap": "3D View",
                                  "space_type": "VIEW_3D",
                                  "idname": "atb.set_axis",
                                  "type": "PAGE_DOWN",
                                  "alt": True,
                                  "value": "PRESS",
                                  },

                                 {"label": "3D View Edit Mesh",
                                  "keymap": "Mesh",
                                  "space_type": "EMPTY",
                                  "idname": "atb.super_select",
                                  "type": "A",
                                  "shift": True,
                                  "alt": True,
                                  "value": "PRESS"},

                                 {"label": "3D View Edit Mesh",
                                  "keymap": "Mesh",
                                  "space_type": "EMPTY",
                                  "idname": "atb.add_to_mode",
                                  "type": "S",
                                  "ctrl": True,
                                  "alt": True,
                                  "value": "PRESS"},

                                 {"label": "3D View Global",
                                  "keymap": "3D View",
                                  "space_type": "VIEW_3D",
                                  "idname": "atb.drop_tool",
                                  "type": "ESC",
                                  "value": "PRESS"},

                                 {"label": "3D View Global",
                                  "keymap": "3D View",
                                  "space_type": "VIEW_3D",
                                  "idname": "atb.group_select",
                                  "type": "RIGHTMOUSE",
                                  "alt": True,
                                  "value": "PRESS"}]
                   }
