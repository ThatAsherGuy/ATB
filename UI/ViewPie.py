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
from bpy.types import (
    Menu,
    Panel
)


class VIEW3D_MT_ATB_view_pie(Menu):
    bl_label = "ATB View Pie"

    def draw(self, context):
        region = context.region_data
        layout = self.layout
        # view = context.space_data
        pie = layout.menu_pie()

        # LEFT
        op = pie.operator("act.view_axis", text="Front/Back | Y Axis")
        op.axis = 'FRONT'
        op.speed = context.preferences.view.smooth_view

        # RIGHT
        op = pie.operator("act.view_axis", text="Right/Left | X Axis")
        op.axis = 'RIGHT'
        op.speed = context.preferences.view.smooth_view

        # BOTTOM
        op = pie.operator("act.view_axis", text="Top/Bottom | Z Axis")
        op.axis = 'TOP'
        op.speed = context.preferences.view.smooth_view

        # TOP
        cam_icon = 'CAMERA_DATA'
        if region.view_perspective == 'CAMERA':
            cam_icon = 'OUTLINER_OB_CAMERA'

        if context.space_data.lock_camera:
            cam_icon = 'CON_CAMERASOLVER'

        context_op = pie.operator(
            "act.context_op",
            text="Camera",
            icon=cam_icon
        )

        if not region.view_perspective == 'CAMERA':

            if not context.scene.camera:
                if context.mode == 'OBJECT':
                    context_op.def_op = "object.camera_add"
                    context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                    context_op.def_op_props = (
                                            "{"
                                            "'enter_editmode': False, "
                                            "'align': 'VIEW'"
                                            "}"
                                            )
                else:
                    context_op.def_op = "object.editmode_toggle"
                    context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                    context_op.def_op_props = ""
            else:
                context_op.def_op = "view3d.camera_to_view"
                context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                context_op.def_op_props = ""

                context_op.ctrl_op = "view3d.view_camera"
                context_op.ctrl_op_args = "'INVOKE_DEFAULT', True,"
                context_op.ctrl_op_props = ""

                context_op.shift_op = "object.select_camera"
                context_op.shift_op_args = "'INVOKE_DEFAULT', True,"
                context_op.shift_op_props = ""

        if region.view_perspective == 'CAMERA':
            context_op.def_op = "wm.context_toggle"
            context_op.def_op_args = "'INVOKE_DEFAULT', True,"
            context_op.def_op_props = "{'data_path': 'space_data.lock_camera'}"

            if context.active_object and context.active_object.type == 'CAMERA':
                context_op.shift_op = "wm.context_toggle"
                context_op.shift_op_args = "'INVOKE_DEFAULT', True,"
                context_op.shift_op_props = "{'data_path': 'object.data.show_name'}"

                # Toggle Ortho/Perspective Lens
                context_op.alt_op = "wm.context_cycle_enum"
                context_op.alt_op_args = "'INVOKE_DEFAULT', True,"
                context_op.alt_op_props = "{'data_path': 'object.data.type', 'wrap': True}"

                context_op.ctrl_shift_op = "wm.context_toggle"
                context_op.ctrl_shift_op_args = "'INVOKE_DEFAULT', True,"
                context_op.ctrl_shift_op_props = (
                                                 "{"
                                                 "'data_path': "
                                                 "'object.data.show_composition_thirds',"
                                                 "}"
                                                 )
            else:
                context_op.ctrl_op = "view3d.view_center_camera"
                context_op.ctrl_op_props = ""

                context_op.shift_op = "view3d.camera_to_view_selected"
                context_op.shift_op_props = ""

                context_op.alt_op = "object.select_camera"
                context_op.alt_op_props = ""

        # TOP LEFT
        op = pie.operator("screen.region_quadview", text="Quad View")

        # TOP RIGHT
        persp_label = "Persp/Ortho | Manual Persp"
        persp_icon = 'VIEW_ORTHO'

        if context.preferences.inputs.use_auto_perspective:
            persp_label = "Persp/Ortho | Auto Persp"
            persp_icon = 'FORCE_CURVE'
        elif region.view_perspective == 'PERSP':
            persp_icon = 'VIEW_PERSPECTIVE'
        elif region.view_perspective == 'ORTHO':
            persp_icon = 'VIEW_ORTHO'

        context_op = pie.operator(
            "act.context_op",
            text=persp_label,
            icon=persp_icon
        )
        context_op.def_op = "view3d.view_persportho"
        context_op.def_op_props = ""

        context_op.ctrl_op = "wm.context_toggle"
        context_op.ctrl_op_props = "{'data_path': 'preferences.inputs.use_auto_perspective'}"

        context_op.shift_op = "act.set_axis"
        context_op.shift_op_props = ""

        # BOTTOM LEFT
        orbit_center_label = "Enable Orbit Selected"
        if context.preferences.inputs.use_rotate_around_active:
            orbit_center_label = "Disable Orbit Selected"

        op = pie.operator("wm.context_toggle", text=orbit_center_label)
        op.data_path = "preferences.inputs.use_rotate_around_active"

        # BOTTOM RIGHT
        orbit_mode_label = "Use Trackball Rotation"
        if context.preferences.inputs.view_rotate_method == 'TRACKBALL':
            orbit_mode_label = "Use Turntable Rotation "

        col = pie.row(align=True)
        col.emboss = 'NORMAL'
        col.alignment = 'LEFT'
        col.use_property_split = True
        col.scale_y = 1.5

        op = col.operator("wm.context_cycle_enum", text=orbit_mode_label)
        op.data_path = "preferences.inputs.view_rotate_method"
        op.wrap = True

        # if context.preferences.inputs.view_rotate_method == 'TRACKBALL':
        #     col.prop(context.preferences.inputs, "view_rotate_sensitivity_trackball")
        # else:
        #     col.prop(context.preferences.inputs, "view_rotate_sensitivity_turntable")

        op = col.operator("wm.call_panel", text="", icon='TRIA_DOWN')
        op.name = "VIEW3D_PT_viewport_rotation_panel"
        op.keep_open = True


class VIEW3D_PT_viewport_rotation_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    # bl_category = "META"
    bl_label = "View Rotation"

    # bl_ui_units_x = 12

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        if context.preferences.inputs.view_rotate_method == 'TRACKBALL':
            col.prop(context.preferences.inputs, "view_rotate_sensitivity_trackball")
        else:
            col.prop(context.preferences.inputs, "view_rotate_sensitivity_turntable")


class VIEW3D_MT_ATB_cursor_pie(Menu):
    bl_label = "ATB Cursor Pie"

    def draw(self, context):
        # region = context.region_data
        layout = self.layout
        # view = context.space_data
        pie = layout.menu_pie()

        # LEFT
        context_op = pie.operator(
            "act.context_op",
            text="Move Cursor",
            icon='ORIENTATION_CURSOR'
        )
        context_op.def_op = "transform.translate"
        context_op.def_op_args = "'INVOKE_DEFAULT', True"
        context_op.def_op_props = ("{'cursor_transform': True}")

        context_op.ctrl_op = "view3d.snap_cursor_to_active"
        context_op.ctrl_op_args = "'INVOKE_DEFAULT', True"

        # RIGHT
        context_op = pie.operator(
            "act.context_op",
            text="Reset Cursor",
            icon='CURSOR'
        )
        context_op.def_op = "view3d.snap_cursor_to_center"
        context_op.def_op_props = ""

        context_op.ctrl_op = "view3d.snap_cursor_to_active"
        context_op.ctrl_op_props = ""

        # BOTTOM
        context_op = pie.operator(
            "act.context_op",
            text="Cursor to Selected | Active",
            icon='PIVOT_CURSOR'
        )
        context_op.def_op = "view3d.snap_cursor_to_selected"
        context_op.def_op_args = "'INVOKE_DEFAULT', True"
        context_op.def_op_props = ""

        context_op.ctrl_op = "view3d.snap_cursor_to_active"
        context_op.ctrl_op_args = "'INVOKE_DEFAULT', True"
        context_op.ctrl_op_props = ""

        # TOP
        context_op = pie.operator(
            "act.context_op",
            text="Selected to Cursor | Active"
        )
        context_op.def_op = "view3d.snap_selected_to_cursor"
        context_op.def_op_props = "{'use_offset': True}"

        context_op.ctrl_op = "view3d.snap_selected_to_active"
        context_op.ctrl_op_props = ""

        context_op.alt_op = "view3d.snap_selected_to_cursor"
        context_op.alt_op_args = "'INVOKE_DEFAULT', True"
        context_op.alt_op_props = "{'use_offset': False}"

        # TOP LEFT

        # TOP RIGHT
        # pie.prop_enum(context.scene.transform_orientation_slots[1], 'type', value='GLOBAL')

        # BOTTOM LEFT
        # sub = pie.column()
        # sub.operator_context = 'EXEC_DEFAULT'
        # op = sub.operator("transform.select_orientation", text="Global")
        # op.orientation = 'GLOBAL'

        # BOTTOM RIGHT


class VIEW3D_MT_PIE_view_utilities(Menu):
    bl_label = "View Utilities"

    def draw(self, context):
        v3dtheme = context.preferences.themes[0].view_3d
        ws = bpy.context.workspace
        colorz = ws.temp_wires
        # region = context.region_data
        layout = self.layout
        # view = context.space_data
        pie = layout.menu_pie()

        # LEFT
        box = pie.box()
        col = box.column(align=True)

        col.prop(colorz, "default_obj_wire", text="")
        col.prop(colorz, "default_edit_wire", text="")

        op = col.operator("act.store_wire_color")

        col.prop(colorz, "temp_obj_wire", text="")
        col.prop(colorz, "temp_edit_wire", text="")

        # RIGHT
        col = pie.column()
        col.prop(v3dtheme, "vertex_size", text="Vertex Size", slider=True)

        # BOTTOM
        col = pie.column()
        op = col.operator("act.set_color", text="Toggle Wire Colors")
        op.tog_set = True
        op.sync_wire = True
        op.invert_wire = False
        op.tog_vert_size = False

        # TOP
        col = pie.column()
        op = col.operator("act.set_color", text="Toggle Vertex Sizes")
        op.tog_vert_size = True
        op.tog_set = False
        op.sync_wire = False
        op.invert_wire = False
        # TOP LEFT
        # TOP RIGHT
        # BOTTOM LEFT
        # BOTTOM RIGHT

class VIEW3D_MT_ATB_origin_pie(Menu):
    bl_label = "ATB Origin Pie"
    bl_description = "A pie for moving object origins"


    def draw(self, context):
        tool_settings = context.scene.tool_settings
        layout = self.layout
        pie = layout.menu_pie()

        # LEFT
        pie.prop(
            tool_settings,
            "use_transform_data_origin",
            text="Move Origins",
            # icon='TRANSFORM_ORIGINS',
            toggle=True
        )
        # RIGHT
        op = pie.operator(
            "act.set_origin",
            text='Cursor',
        )
        op.snap_mode = 'CURSOR'
        # BOTTOM
        op = pie.operator(
            "act.origin_to_bbox",
            text='Bottom',
        )
        op.box_mode = 'FACE'
        op.box_face = 'ZNEG'
        # TOP
        op = pie.operator(
            "act.origin_to_bbox",
            text='Center',
        )
        op.box_mode = 'FACE'
        op.box_face = 'CENTER'
        # TOP LEFT
        pie.separator()
        # TOP RIGHT
        pie.separator()
        # BOTTOM LEFT
        pie.separator()
        # BOTTOM RIGHT


class VIEW3D_MT_ATB_tablet_pie(Menu):
    bl_label = "ATB Tablet Pie"
    bl_description = "A pie for pen tablet stuff"


    def draw(self, context):
        # region = context.region_data
        layout = self.layout
        pie = layout.menu_pie()

        # LEFT
        op = pie.operator("wm.call_menu_pie", text="Origin")
        op.name = "VIEW3D_MT_ATB_origin_pie"
        # RIGHT
        op = pie.operator("wm.call_menu_pie", text="Cursor")
        op.name = "VIEW3D_MT_ATB_cursor_pie"
        # BOTTOM
        if context.mode == "OBJECT":
            op = pie.operator("act.group_select", text="Select Hierachy")
        else:
            op = pie.operator("act.super_select", text="Select Topology")
            op.action = "0"
        # TOP
        op = pie.operator("wm.call_menu_pie", text="View")
        op.name = "VIEW3D_MT_ATB_view_pie"
        # TOP LEFT
        pie.separator()
        # TOP RIGHT
        pie.separator()
        # BOTTOM LEFT
        pie.separator()
        # BOTTOM RIGHT
        op = pie.operator("view3d.object_mode_pie_or_toggle", text="Editor Mode")