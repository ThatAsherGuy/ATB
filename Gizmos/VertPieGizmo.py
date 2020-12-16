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
# import math
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
                normal = bm.select_history.active.normal
            elif bpy.context.scene.tool_settings.mesh_select_mode[1]:
                vert_one = active.verts[0].co
                vert_two = active.verts[1].co
                normal = active.verts[0].normal + active.verts[1].normal
                active = (vert_one + vert_two) / 2
            elif bpy.context.scene.tool_settings.mesh_select_mode[2]:
                normal = active.normal.copy()
                normal = mathutils.geometry.normal(v.co for v in active.verts)
                active = active.calc_center_median()

            # Normal Rotation
            norm = normal.to_track_quat('Z', 'X')
            n_mat = norm.to_matrix()

            # Object Matrix
            w_mat = obj.matrix_world.copy()
            w_mat = w_mat.to_3x3()

            matrix_new = w_mat.to_3x3().inverted().transposed()
            foik = matrix_new @ n_mat
            foik = foik.to_4x4()

            # Translation Component
            sel_loc = active.copy()
            sel_loc_mat = mathutils.Matrix.Translation(sel_loc)
            sel_loc_mat = w_mat.to_4x4() @ sel_loc_mat

            a_mat = mathutils.Matrix.Translation(sel_loc_mat.to_translation())

            final = a_mat @ foik

            return final

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


class ATVertexGizmoGroup(GizmoGroup):
    bl_idname = "OBJECT_GGT_vertex_gizmo"
    bl_label = "Vertex Menu Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT', 'SHOW_MODAL_ALL'}

    @classmethod
    def poll(cls, context):
        if active_tool().idname == 'builtin.select_box' and context.scene.act_gizmo_pick[0]:
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
        # print("Pivot:   " + str(pivot))

        line_width = 4 + (bpy.context.scene.gz_scale * 1)
        scale_curve = math.sqrt(line_width * 0.1)
        sbias = scale_curve * (0.1 + bpy.context.scene.gz_scale)
        self.sbias = sbias

        vbutton = self.gizmos.new('GIZMO_GT_move_3d')
        vbutton.draw_options = {'ALIGN_VIEW'}

        props = vbutton.target_set_operator("wm.call_menu_pie")
        props.name = "VIEW3D_MT_PIE_orbit_lock"

        v_mat = mathutils.Matrix.Diagonal((1, 1, 1, 1))
        v_mat = mathutils.Matrix.Rotation(math.radians(90), 4, 'Z')
        vbutton.matrix_basis = pivot
        vbutton.matrix_offset = v_mat

        vbutton.line_width = line_width

        vbutton.color = giz_color()
        vbutton.alpha = 0.95

        vbutton.color_highlight = 1.0, 1.0, 1.0
        vbutton.alpha_highlight = 1.0

        vbutton.use_draw_scale = True
        vbutton.scale_basis = sbias * 0.2

        self.vbutton = vbutton

        #######

        z_ax = self.gizmos.new('GIZMO_GT_arrow_3d')
        z_ax.use_draw_offset_scale = True
        z_ax.use_draw_scale = True

        props = z_ax.target_set_operator("atb.context_op")
        props.def_op = "transform.translate"
        props.def_op_args = "'INVOKE_DEFAULT', True"
        props.def_op_props = (
                              "{"
                              "'orient_type': 'NORMAL',"
                              "'constraint_axis': (False, False, True),"
                              "}"
                            )

        props.shift_op = "view3d.edit_mesh_extrude_move_normal"
        props.shift_op_args = "'INVOKE_DEFAULT', True"
        props.shift_op_props = ""

        props.alt_op = "mesh.bevel"
        props.alt_op_args = "'INVOKE_DEFAULT', True"
        props.alt_op_props = ""

        q_mat = mathutils.Matrix.Translation((0, 0, 0, 1.5))

        z_ax.matrix_basis = pivot
        z_ax.matrix_offset = q_mat

        z_ax.line_width = 4

        z_ax.color = 0.5, 0.9, 0.9
        z_ax.alpha = 0.95

        z_ax.color_highlight = 1.0, 1.0, 1.0
        z_ax.alpha_highlight = 1.0

        z_ax.use_draw_scale = True
        z_ax.scale_basis = sbias * 1.5
        z_ax.select_bias = 2

        self.z_ax = z_ax

    def draw_prepare(self, context):
        pivot = set_pivot()
        vbutton = self.vbutton
        z_ax = self.z_ax
        vbutton.color = giz_color()

        vbutton.matrix_basis = pivot
        z_ax.matrix_basis = pivot

        line_width = 4 / (bpy.context.scene.gz_scale)
        scale_curve = math.sqrt(bpy.context.scene.gz_scale)

        # scale_curve = 2
        sbias = scale_curve * (bpy.context.scene.gz_scale)
        vbutton.scale_basis = sbias * 0.2
        z_ax.scale_basis = sbias * 1.5

        vbutton.line_width = line_width
        z_ax.line_width = line_width

    def refresh(self, context):
        pivot = set_pivot()
        vbutton = self.vbutton
        z_ax = self.z_ax
        vbutton.color = giz_color()

        vbutton.matrix_basis = pivot
        z_ax.matrix_basis = pivot

        line_width = 4 / (bpy.context.scene.gz_scale)
        scale_curve = math.sqrt(bpy.context.scene.gz_scale)

        sbias = scale_curve * (bpy.context.scene.gz_scale)
        vbutton.scale_basis = sbias
        z_ax.scale_basis = sbias * 1.5

        vbutton.line_width = line_width
        z_ax.line_width = line_width
