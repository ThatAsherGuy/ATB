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
import bpy_extras
from bpy_extras import view3d_utils
import blf
import bgl
# import bmesh
import mathutils
import math
from bl_ui.space_toolsystem_toolbar import (
    VIEW3D_PT_tools_active as view3d_tools
)
from bpy.types import (
    # WorkSpaceTool,
    # Operator,
    GizmoGroup,
    Gizmo
)
from bpy.props import (
    BoolProperty,
)
from random import random

fonting = False

handle = None
font_info = {
    "font_id": 0,
    "handler": None,
}


def text_init(loc, rot):
    import os
    global fonting
    global handle
    font_path = bpy.path.abspath('//Zeyada.ttf')

    if os.path.exists(font_path):
        font_info["font_id"] = blf.load(font_path)
    else:
        font_info["font_id"] = 1

    loc_2d = bpy_extras.view3d_utils.location_3d_to_region_2d(bpy.context.region, bpy.context.space_data.region_3d, loc)

    handle = bpy.types.SpaceView3D.draw_handler_add(
        draw_callback_px, (None, None, loc_2d, rot), 'WINDOW', 'POST_PIXEL'
    )
    fonting = True


def draw_callback_px(self, context, position, rotation):
    font_id = font_info["font_id"]
    blf.enable(font_id, blf.ROTATION)

    blf.rotation(font_id, math.radians(45))
    blf.position(font_id, position[0] - 280, position[1] - 280, 0)
    # blf.position(font_id, 3, 3, 0)

    blf.size(font_id, 10, 300)
    blf.draw(font_id, "Hello World")


def text_remove():
    bpy.types.SpaceView3D.draw_handler_remove(font_info["handler"], 'WINDOW')


def random_color():
    r = random()
    g = random()
    b = random()
    _rand_color = (r, g, b)
    rand_color = _rand_color
    return rand_color


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


class AxisButton(Gizmo):
    bl_idname = "GIZMO_GT_dial_3d"
    bl_target_properties = (
        {"id": "offset", "type": 'FLOAT', "array_length": 1},
    )
    __slots__ = (
        "init_mouse_y",
        "init_value",
    )

    # def setup(self):
    #     # self.gizmos.new('GIZMO_GT_dial_3d')
    #     # cursor = bpy.context.scene.cursor
    #     # region = bpy.context.region_data

    def invoke(self, context, event):
        self.init_mouse_y = event.mouse_y
        self.init_value = self.target_get_value("offset")
        return {'RUNNING_MODAL'}

    def exit(self, context, cancel):
        context.area.header_text_set(None)
        if cancel:
            self.target_set_value("offset", self.init_value)

    def draw(self, context):
        self.matrix_offset.col[3][2] = self.target_get_value("offset") * 10.0

    def modal(self, context, event, tweak):
        delta = (event.mouse_y - self.init_mouse_y)
        value = (self.init_value - delta) * 8000
        self.target_set_value("offset", value)
        context.area.header_text_set("My Gizmo: %.4f" % value)

        return {'RUNNING_MODAL'}


class AxisGizmo(GizmoGroup):
    bl_idname = "OBJECT_GGT_axis_gizmo"
    bl_label = "Dick Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT', 'SHOW_MODAL_ALL'}

    @classmethod
    def poll(cls, context):
        if context.scene.act_gizmo_pick[3]:
            return True

    def update(self, context, gizmo, color, rotation, boig):
        region = context.region_data
        global fonting
        global handle

        wm = bpy.context.window_manager
        mp_props = wm.ATB

        if gizmo.bl_idname == 'GIZMO_GT_dial_3d':
            gizmo.arc_partial_angle = math.radians(320)
            # if rotation == 0 or rotation == 90 or rotation == 180 or rotation == 270:
            #     gizmo.arc_partial_angle = math.radians(280)
            # else:
            #     gizmo.arc_partial_angle = math.radians(290)
            # gizmo.draw_options = {'ANGLE_MIRROR'}

        gizmo.use_draw_offset_scale = True
        gizmo.use_draw_scale = True

        gizmo.use_draw_value = True

        if gizmo.bl_idname == 'GIZMO_GT_dial_3d':
            gizmo.scale_basis = 1
            gizmo.line_width = 2
        elif gizmo.bl_idname == 'GIZMO_GT_move_3d':
            gizmo.draw_style = 'RING_2D'
            gizmo.scale_basis = 0.6
            gizmo.line_width = 3

        gizmo.color = color
        gizmo.color_highlight = color
        gizmo.alpha = 0.75
        gizmo.alpha_highlight = 1
        gizmo.use_event_handle_all = False

        center = [0, 1]
        center[1] = (bpy.context.region.height / 2)
        center[0] = (bpy.context.region.width / 2)

        center_offset = [0, 1]
        center_offset[1] = (120)
        center_offset[0] = (120)

        hud_loc = bpy_extras.view3d_utils.region_2d_to_location_3d(
                                                                    bpy.context.region,
                                                                    context.region_data,
                                                                    center,
                                                                    region.view_location
                                                                    )

        hud_offset = bpy_extras.view3d_utils.region_2d_to_location_3d(
                                                                    bpy.context.region,
                                                                    context.region_data,
                                                                    center_offset,
                                                                    region.view_location
                                                                    )

        hud_mat = mathutils.Matrix.Translation(hud_loc)

        querg = mathutils.Matrix.Translation(region.view_location)
        querg.resize_4x4()

        # Align Rotation
        view_quat = region.view_rotation.to_euler()
        _offset = mathutils.Matrix.Identity(3)
        _offset = hud_mat.to_3x3()

        z_rot = mathutils.Matrix.Rotation(math.radians(rotation), 3, 'Z')
        x_rot = mathutils.Matrix.Rotation(math.radians(90), 3, 'X')

        _offset.rotate(z_rot)
        _offset.rotate(view_quat)
        # _offset.rotate(x_rot)
        _offset.resize_4x4()

        gizmo.matrix_basis = hud_mat
        # # gizmo.matrix_space = hud_mat
        gizmo.matrix_offset = _offset

        props = gizmo.target_set_operator("transform.translate")

        if boig:
            gizmo.alpha = 0.5

        if gizmo.is_highlight:

            gizmo.use_event_handle_all = True
            if gizmo.bl_idname == 'GIZMO_GT_dial_3d':
                gizmo.draw_options = {'FILL_SELECT'}
                gizmo.arc_partial_angle = math.radians(290)
                # gizmo.arc_inner_factor = 0.9
                gizmo.line_width = 1
                gizmo.scale_basis *= 1.2
                if boig:
                    gizmo.scale_basis *= 3.2
                    gizmo.alpha = 1.0
                    gizmo.draw_options = {'FILL'}

            elif gizmo.bl_idname == 'GIZMO_GT_move_3d':
                gizmo.line_width = 5
                gizmo.scale_basis *= 1.2
                gizmo.draw_options = {'FILL_SELECT'}

        if mp_props.mp_debug[1]:
            props = gizmo.target_set_operator("view3d.dolly")
        elif mp_props.mp_debug[2]:
            props = gizmo.target_set_operator("view3d.rotate")
            props.use_cursor_init = False
        else:
            props = gizmo.target_set_operator("wm.call_menu_pie")
            props.name = "VIEW3D_MT_PIE_orbit_lock"

        if gizmo.bl_idname == 'GIZMO_GT_move_3d':
            props = gizmo.target_set_operator("view3d.move")
            props.use_cursor_init = False

        if (rotation == 135):
            # props = gizmo.target_set_operator("view3d.dolly")
            loc = hud_mat.to_translation()

            if gizmo.is_highlight:
                if fonting is False:
                    text_init(loc, rotation)
                    fonting = True

            if not gizmo.is_highlight:
                if fonting is True:
                    # print(str(fonting))
                    bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')
                    fonting = False

    def setup(self, context):
        a_giz = self.gizmos.new(AxisButton.bl_idname)
        self.update(context, a_giz, (0.5, 0.9, 0.9), 0, False)
        self.a_giz = a_giz

        b_giz = self.gizmos.new(AxisButton.bl_idname)
        self.update(context, b_giz, (0.9, 0.5, 0.9), 45, False)
        self.b_giz = b_giz

        c_giz = self.gizmos.new(AxisButton.bl_idname)
        self.update(context, c_giz, (0.9, 0.9, 0.5), 90, False)
        self.c_giz = c_giz

        d_giz = self.gizmos.new(AxisButton.bl_idname)
        self.update(context, d_giz, (0.9, 0.5, 0.5), 135, False)
        self.d_giz = d_giz

        e_giz = self.gizmos.new("GIZMO_GT_move_3d")
        self.update(context, e_giz, (0.9, 0.5, 0.5), 0, False)
        e_giz.draw_style = 'RING_2D'
        # e_giz.draw_options = {'FILL'}
        self.e_giz = e_giz

        f_giz = self.gizmos.new(AxisButton.bl_idname)
        self.update(context, f_giz, (0.5, 0.9, 0.5), 180, False)
        self.f_giz = f_giz

        g_giz = self.gizmos.new(AxisButton.bl_idname)
        self.update(context, g_giz, (0.5, 0.5, 0.9), 225, False)
        self.g_giz = g_giz

        h_giz = self.gizmos.new(AxisButton.bl_idname)
        self.update(context, h_giz, (0.9, 0.9, 0.9), 270, False)
        self.h_giz = h_giz

        i_giz = self.gizmos.new(AxisButton.bl_idname)
        self.update(context, i_giz, (0.45, 0.45, 0.45), 315, False)
        self.i_giz = i_giz

        j_giz = self.gizmos.new("GIZMO_GT_move_3d")
        self.update(context, j_giz, (0.9, 0.75, 0.45), 0, False)
        j_giz.draw_style = 'RING_2D'
        j_giz.scale_basis *= 0.6
        self.j_giz = j_giz

    def draw_prepare(self, context):
        a_giz = self.a_giz
        self.update(context, a_giz, (0.5, 0.9, 0.9), 0, False)

        b_giz = self.b_giz
        self.update(context, b_giz, (0.9, 0.5, 0.9), 45, False)

        c_giz = self.c_giz
        self.update(context, c_giz, (0.9, 0.9, 0.5), 90, False)

        d_giz = self.d_giz
        self.update(context, d_giz, (0.9, 0.5, 0.5), 135, False)

        e_giz = self.e_giz
        self.update(context, e_giz, (0.9, 0.5, 0.5), 0, False)

        f_giz = self.f_giz
        self.update(context, f_giz, (0.5, 0.9, 0.5), 180, False)

        g_giz = self.g_giz
        self.update(context, g_giz, (0.5, 0.5, 0.9), 225, False)

        h_giz = self.h_giz
        self.update(context, h_giz, (0.9, 0.9, 0.9), 270, False)

        i_giz = self.i_giz
        self.update(context, i_giz, (0.45, 0.45, 0.45), 315, False)

        j_giz = self.j_giz
        self.update(context, j_giz, (0.9, 0.75, 0.45), 0, False)
        j_giz.scale_basis *= 0.6

    def refresh(self, context):
        a_giz = self.a_giz
        self.update(context, a_giz, (0.5, 0.9, 0.9), 0, False)

        b_giz = self.b_giz
        self.update(context, b_giz, (0.9, 0.5, 0.9), 45, False)

        c_giz = self.c_giz
        self.update(context, c_giz, (0.9, 0.9, 0.5), 90, False)

        d_giz = self.d_giz
        self.update(context, d_giz, (0.9, 0.5, 0.5), 135, False)

        e_giz = self.e_giz
        self.update(context, e_giz, (0.9, 0.5, 0.5), 0, False)

        f_giz = self.f_giz
        self.update(context, f_giz, (0.5, 0.9, 0.5), 180, False)

        g_giz = self.g_giz
        self.update(context, g_giz, (0.5, 0.5, 0.9), 225, False)

        h_giz = self.h_giz
        self.update(context, h_giz, (0.9, 0.9, 0.9), 270, False)

        i_giz = self.i_giz
        self.update(context, i_giz, (0.45, 0.45, 0.45), 315, False)

        j_giz = self.j_giz
        self.update(context, j_giz, (0.9, 0.75, 0.45), 0, False)
        j_giz.scale_basis *= 0.6
