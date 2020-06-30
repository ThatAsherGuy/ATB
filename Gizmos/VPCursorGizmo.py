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
import bpy
# import bmesh
# import mathutils
from bl_ui.space_toolsystem_toolbar import (
    VIEW3D_PT_tools_active as view3d_tools
)
from bpy.types import (
    WorkSpaceTool,
    # Operator,
    GizmoGroup,
)
import os

plus_button = (
    0x5f, 0xfb, 0x40, 0xee, 0x25, 0xda, 0x11, 0xbf, 0x4,  0xa0, 0x0,  0x80, 0x4,  0x5f, 0x11, 0x40,
    0x25, 0x25, 0x40, 0x11, 0x5f, 0x4,  0x7f, 0x0,  0xa0, 0x4,  0xbf, 0x11, 0xda, 0x25, 0xee, 0x40,
    0xfb, 0x5f, 0xff, 0x7f, 0xfb, 0xa0, 0xee, 0xbf, 0xda, 0xda, 0xbf, 0xee, 0xa0, 0xfb, 0x80, 0xff,
    0x6e, 0xd7, 0x92, 0xd7, 0x92, 0x90, 0xd8, 0x90, 0xd8, 0x6d, 0x92, 0x6d, 0x92, 0x27, 0x6e, 0x27,
    0x6e, 0x6d, 0x28, 0x6d, 0x28, 0x90, 0x6e, 0x90, 0x6e, 0xd7, 0x80, 0xff, 0x5f, 0xfb, 0x5f, 0xfb,
)
csv_b = bytes(plus_button)

custom_shape_verts = (
    0x84, 0x10, 0x87, 0x11, 0xdc, 0x42, 0xde,
    0x44, 0xe0, 0x46, 0xe2, 0x49, 0xe3, 0x4c,
    0xe3, 0x4e, 0xe3, 0xb1, 0xe3, 0xb3, 0xe2,
    0xb6, 0xe0, 0xb9, 0xde, 0xbb, 0xdc, 0xbd,
    0x87, 0xee, 0x84, 0xef, 0x81, 0xf0, 0x7e,
    0xf0, 0x7b, 0xef, 0x78, 0xee, 0x23, 0xbd,
    0x21, 0xbb, 0x1f, 0xb9, 0x1d, 0xb6, 0x1c,
    0xb3, 0x1c, 0xb1, 0x1c, 0x4e, 0x1c, 0x4c,
    0x1d, 0x49, 0x1f, 0x46, 0x21, 0x44, 0x23,
    0x42, 0x78, 0x11, 0x7b, 0x10, 0x7e, 0x0f,
    0x7e, 0x28, 0x7b, 0x28, 0x78, 0x29, 0x38,
    0x4e, 0x36, 0x50, 0x34, 0x52, 0x33, 0x55,
    0x32, 0x58, 0x31, 0x5b, 0x31, 0xa4, 0x32,
    0xa7, 0x33, 0xaa, 0x34, 0xad, 0x36, 0xaf,
    0x38, 0xb1, 0x78, 0xd6, 0x7b, 0xd7, 0x7e,
    0xd7, 0x81, 0xd7, 0x84, 0xd7, 0x87, 0xd6,
    0xc7, 0xb1, 0xc9, 0xaf, 0xcb, 0xad, 0xcc,
    0xaa, 0xcd, 0xa7, 0xce, 0xa4, 0xce, 0x5b,
    0xcd, 0x58, 0xcc, 0x55, 0xcb, 0x52, 0xc9,
    0x50, 0xc7, 0x4e, 0x87, 0x29, 0x84, 0x28,
    0x81, 0x28, 0x81, 0x0f, 0x81, 0x0f, 0x7e,
    0x28, 0x7e, 0x0f, 0x81, 0x0f, 0x81, 0x28,
    0x81, 0x28, 0x7e, 0x36, 0x81, 0x36, 0x84,
    0x37, 0x87, 0x38, 0xba, 0x56, 0xbc, 0x57,
    0xbe, 0x5a, 0xc0, 0x5c, 0xc1, 0x5f, 0xc1,
    0x62, 0xc1, 0x9d, 0xc1, 0xa0, 0xc0, 0xa3,
    0xbe, 0xa5, 0xbc, 0xa8, 0xba, 0xa9, 0x87,
    0xc7, 0x84, 0xc8, 0x81, 0xc9, 0x7e, 0xc9,
    0x7b, 0xc8, 0x78, 0xc7, 0x45, 0xa9, 0x43,
    0xa8, 0x41, 0xa5, 0x3f, 0xa3, 0x3e, 0xa0,
    0x3e, 0x9d, 0x3e, 0x62, 0x3e, 0x5f, 0x3f,
    0x5c, 0x41, 0x5a, 0x43, 0x57, 0x58, 0x64,
    0x56, 0x66, 0x55, 0x69, 0x54, 0x6b, 0x53,
    0x6e, 0x53, 0x91, 0x54, 0x94, 0x55, 0x96,
    0x56, 0x99, 0x58, 0x9b, 0x5a, 0x9d, 0x78,
    0xae, 0x7b, 0xaf, 0x7e, 0xb0, 0x81, 0xb0,
    0x84, 0xaf, 0x87, 0xae, 0xa5, 0x9d, 0xa7,
    0x9b, 0xa9, 0x99, 0xaa, 0x96, 0xab, 0x94,
    0xac, 0x91, 0xac, 0x6e, 0xab, 0x6b, 0xaa,
    0x69, 0xa9, 0x66, 0xa7, 0x64, 0xa5, 0x62,
    0x87, 0x51, 0x84, 0x50, 0x81, 0x4f, 0x7e,
    0x4f, 0x7b, 0x50, 0x7b, 0x37, 0x7b, 0x37,
    0x78, 0x38, 0x7b, 0x37, 0x7b, 0x50, 0x78,
    0x51, 0x5a, 0x62, 0x58, 0x64, 0x43, 0x57,
    0x45, 0x56, 0x45, 0x56,
)

csv_thing = bytes(custom_shape_verts)


def active_tool():
    return view3d_tools.tool_active_from_context(bpy.context)


def giz_color():
    color = 0.5, 0.5, 0.5
    if bpy.context.scene.cp_mode_enum == '0':
        color = 0.95, 0.95, 0.5
    elif bpy.context.scene.cp_mode_enum == '1':
        color = 0.95, 0.5, 0.95
    elif bpy.context.scene.cp_mode_enum == '2':
        color = 0.5, 0.95, 0.95
    elif bpy.context.scene.cp_mode_enum == '3':
        color = 0.5, 0.95, 0.5
    return color


class ATVPCursorGizmo(GizmoGroup):
    bl_idname = "OBJECT_GGT_cursor_gizmo"
    bl_label = "Dick Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT', 'SHOW_MODAL_ALL'}

    @classmethod
    def poll(cls, context):
        toolz = active_tool()
        if toolz.idname == "AT.cursortool":
            return True

    @classmethod
    def setup_keymap(self, keys):
        # Key Map - box, not present
        if not keys.keymaps.find(name="ATB Gizmo", space_type="VIEW_3D"):
            print("No Keymap - Making a New One")
            km = keys.keymaps.new(name='ATB Gizmo', space_type="VIEW_3D")

            # Key Map Item - present, not box
            km.keymap_items.new("gizmogroup.gizmo_tweak", "LEFTMOUSE", "PRESS")

            kmi = km.keymap_items.new(
                "wm.call_menu_pie",
                'RIGHTMOUSE',
                'CLICK',
                )
            kmi.properties.name = "VIEW3D_MT_ATB_cursor_pie"
        else:
            km = keys.keymaps.find(name="ATB Gizmo", space_type="VIEW_3D")
            km.restore_to_default()
            # print("ATB Gizmo Keymap Found: " + str(len(km.keymap_items)) + " Entries")
            if (len(km.keymap_items)) < 2:
                km.restore_to_default()
                km.keymap_items.new("gizmogroup.gizmo_tweak", "LEFTMOUSE", "PRESS")

                kmi = km.keymap_items.new(
                    "wm.call_menu_pie",
                    'RIGHTMOUSE',
                    'CLICK',
                    )
                kmi.properties.name = "VIEW3D_MT_ATB_cursor_pie"
        return km

    def setup(self, context):
        cursor = context.scene.cursor

        c_button = self.gizmos.new('GIZMO_GT_button_2d')
        # c_button.draw_options = {'ALIGN_VIEW'}
        c_button.draw_options = {'OUTLINE'}
        # c_button.icon = 'NONE'
        c_button.shape = csv_thing

        # c_button.show_drag = True
        c_button.use_draw_modal = True
        c_button.use_draw_value = True
        c_button.use_draw_offset_scale = True
        c_button.use_draw_scale = True
        # c_button.use_snap = True

        c_button.scale_basis = 0.25

        c_button.color = 0.5, 0.5, 0.5
        c_button.color_highlight = 0.9, 0.9, 0.9

        c_button.alpha = 1.0
        c_button.alpha_highlight = 1.0

        c_button.line_width = 1
        c_button.use_event_handle_all = True

        props = c_button.target_set_operator("transform.translate")
        props.cursor_transform = True
        props.release_confirm = True

        # props = c_button.target_set_operator("act.mouse_context_op")
        # props.left_op = "transform.translate"
        # props.left_op_args = "'INVOKE_DEFAULT', True"
        # props.left_op_props = (
        #                       "{"
        #                       "'cursor_transform': True,"
        #                       "'release_confirm': True,"
        #                       "}"
        #                       )

        # props.right_op = "wm.call_menu_pie"
        # props.right_op_args = "'INVOKE_DEFAULT', True"
        # props.right_op_props = (
        #                       "{"
        #                       "'name': 'VIEW3D_MT_ATB_cursor_pie',"
        #                       "}"
        #                       )

        c_button.matrix_basis = cursor.matrix

        self.c_button = c_button

    def draw_prepare(self, context):
        cursor = context.scene.cursor

        c_button = self.c_button
        c_button.matrix_basis = cursor.matrix

        if c_button.is_highlight:
            c_button.scale_basis = 0.25
            c_button.draw_options = {'OUTLINE', 'BACKDROP'}
        else:
            c_button.scale_basis = 0.25
            c_button.draw_options = {'OUTLINE'}

    def refresh(self, context):
        cursor = context.scene.cursor

        c_button = self.c_button
        c_button.matrix_basis = cursor.matrix


class ATCursorTool(WorkSpaceTool):
    icon_dir = os.path.join(os.path.dirname(__file__), "icons", "asher.hex_1")

    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'OBJECT'

    bl_idname = "AT.cursortool"
    bl_label = "Cursor Gizmo"
    bl_description = ("Get off my lawn")
    bl_icon = icon_dir
    bl_widget = "OBJECT_GGT_cursor_gizmo"
    # bl_keymap = ()

    def draw_settings(context, layout, tool):
        props = tool.operator_properties("transform.translate")
        layout.prop(props, "cursor_transform")
