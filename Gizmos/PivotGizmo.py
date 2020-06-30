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
import bmesh
import mathutils
import math
from bl_ui.space_toolsystem_toolbar import (
    VIEW3D_PT_tools_active as view3d_tools
)
from bpy.types import (
    # WorkSpaceTool,
    # Operator,
    GizmoGroup,
)


def active_tool():
    return view3d_tools.tool_active_from_context(bpy.context)


def get_tools():
    return view3d_tools.tools_from_context(bpy.context)


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


def set_pivot():
    if bpy.context.mode == 'EDIT_MESH':
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        active = bm.select_history.active

        if bpy.context.scene.gz_piv_enum == '0':
            if bpy.context.scene.tool_settings.mesh_select_mode[0]:
                active = bm.select_history.active.co
            elif bpy.context.scene.tool_settings.mesh_select_mode[1]:
                vert_one = active.verts[0].co
                vert_two = active.verts[1].co
                active = (vert_one + vert_two) / 2
            elif bpy.context.scene.tool_settings.mesh_select_mode[2]:
                active = active.calc_center_median()

            w_mat = obj.matrix_world
            sel_loc = active.copy()
            sel_loc_mat = mathutils.Matrix.Translation(sel_loc)
            pivot = w_mat @ sel_loc_mat

            return pivot

        elif bpy.context.scene.gz_piv_enum == '1':
            pivot = obj.matrix_world
            return pivot
        elif bpy.context.scene.gz_piv_enum == '2':
            cursor = bpy.context.scene.cursor
            pivot = cursor.matrix
            return pivot

    elif bpy.context.mode == 'OBJECT':
        obj = bpy.context.active_object

        if bpy.context.scene.gz_piv_enum == '0':
            pivot = obj.matrix_world
            return pivot
        if bpy.context.scene.gz_piv_enum == '1':
            pivot = obj.matrix_world
            return pivot
        if bpy.context.scene.gz_piv_enum == '2':
            cursor = bpy.context.scene.cursor
            pivot = cursor.matrix
            return pivot


class ATPivotGizmoGroup(GizmoGroup):
    bl_idname = "OBJECT_GGT_pivot_gizmo"
    bl_label = "Pivot Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT', 'SHOW_MODAL_ALL', 'SCALE'}

    @classmethod
    def poll(cls, context):
        if active_tool().idname == 'builtin.select_box' and context.scene.act_gizmo_pick[1]:
            # return True
            if len(context.selected_objects) > 0:
                if bpy.context.scene.gz_piv_enum == '0':
                    if getattr(context.active_object, 'type', '') == 'MESH':
                        if bpy.context.mode == 'EDIT_MESH':
                            obj = bpy.context.edit_object
                            me = obj.data
                            bm = bmesh.from_edit_mesh(me)
                            return bm.select_history.active
                        elif bpy.context.mode == 'OBJECT':
                            return True
                else:
                    return True

    def setup(self, context):
        pivot = set_pivot()
        scene = context.scene

        vbutton = self.gizmos.new('GIZMO_GT_dial_3d')
        vbutton.draw_options = {'CLIP'}
        # vbutton.draw_style = 'BOX'
        # vbutton.aspect = (1.1, 0.1)

        vbutton.matrix_basis = pivot
        vbutton.line_width = 4
        vbutton.scale_basis = 0.5

        vbutton.color = giz_color()
        vbutton.alpha = 0.95

        vbutton.color_highlight = 1.0, 1.0, 1.0
        vbutton.alpha_highlight = 1.0

        vbutton.use_draw_scale = True
        vbutton.use_draw_offset_scale = False

        props = vbutton.target_set_operator("act.rotate_around_pivot")
        offset = (scene.piv_gz_x, scene.piv_gz_y, scene.piv_gz_z)

        offset_mat = mathutils.Matrix.Translation(offset)
        erm = mathutils.Matrix.Rotation(math.radians(-90), 4, 'X')
        offset_mat = offset_mat @ erm

        vbutton.matrix_offset = offset_mat
        _off = pivot @ offset_mat
        _offset = _off.to_translation()
        props.offset = _offset

        self.vbutton = vbutton

        x_arrow = self.gizmos.new('GIZMO_GT_arrow_3d')
        xa_rot = mathutils.Matrix.Rotation(math.radians(90), 4, 'Y')
        x_arrow.matrix_basis = pivot @ xa_rot
        x_arrow.line_width = 4
        x_arrow.color = 1, 0.5, 0.5
        # x_arrow.matrix_offset = offset_mat
        x_arrow.target_set_prop("offset", context.scene, "piv_gz_x", index=0)
        self.x_arrow = x_arrow

        z_arrow = self.gizmos.new('GIZMO_GT_arrow_3d')
        z_arrow.matrix_basis = pivot
        z_arrow.line_width = 4
        z_arrow.color = 0.5, 0.5, 1
        z_arrow.target_set_prop("offset", context.scene, "piv_gz_z", index=0)
        self.z_arrow = z_arrow

    def draw_prepare(self, context):
        pivot = set_pivot()
        scene = context.scene

        vbutton = self.vbutton
        vbutton.color = giz_color()
        vbutton.matrix_basis = pivot

        vbutton.use_draw_scale = True
        vbutton.use_draw_offset_scale = False

        props = vbutton.target_set_operator("act.rotate_around_pivot")
        offset = (scene.piv_gz_x, scene.piv_gz_y, scene.piv_gz_z)

        offset_mat = mathutils.Matrix.Translation(offset)
        erm = mathutils.Matrix.Rotation(math.radians(-90), 4, 'X')
        offset_mat = offset_mat @ erm

        vbutton.matrix_offset = offset_mat
        _off = pivot @ offset_mat
        _offset = _off.to_translation()
        props.offset = _offset

        x_arrow = self.x_arrow
        xa_rot = mathutils.Matrix.Rotation(math.radians(90), 4, 'Y')
        x_arrow.matrix_basis = pivot @ xa_rot
        x_arrow.line_width = 4
        x_arrow.color = 1, 0.5, 0.5
        x_arrow.target_set_prop(
                            "offset",
                            context.scene,
                            "piv_gz_x",
                            index=0
        )

        z_arrow = self.z_arrow
        z_arrow.matrix_basis = pivot
        z_arrow.line_width = 4
        z_arrow.color = 0.5, 0.5, 1
        z_arrow.target_set_prop(
                            "offset",
                            context.scene,
                            "piv_gz_z",
                            index=0
        )

    def refresh(self, context):
        scene = context.scene
        pivot = set_pivot()

        vbutton = self.vbutton
        vbutton.matrix_basis = pivot
        vbutton.color = giz_color()

        vbutton.use_draw_scale = True
        vbutton.use_draw_offset_scale = True

        props = vbutton.target_set_operator("act.rotate_around_pivot")
        offset = (scene.piv_gz_x, scene.piv_gz_y, scene.piv_gz_z)

        offset_mat = mathutils.Matrix.Translation(offset)
        erm = mathutils.Matrix.Rotation(math.radians(-90), 4, 'X')
        offset_mat = offset_mat @ erm

        vbutton.matrix_offset = offset_mat
        _off = pivot @ offset_mat
        _offset = _off.to_translation()
        props.offset = _offset

        x_arrow = self.x_arrow
        xa_rot = mathutils.Matrix.Rotation(math.radians(90), 4, 'Y')
        x_arrow.matrix_basis = pivot @ xa_rot
        x_arrow.line_width = 4
        x_arrow.color = 1, 0.5, 0.5
        x_arrow.target_set_prop(
                            "offset",
                            context.scene,
                            "piv_gz_x",
                            index=0
        )

        z_arrow = self.z_arrow
        z_arrow.matrix_basis = pivot
        z_arrow.line_width = 4
        z_arrow.color = 0.5, 0.5, 1
        z_arrow.target_set_prop(
                            "offset",
                            context.scene,
                            "piv_gz_z",
                            index=0
        )
