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
from . import GizmoGeometry
from bl_ui.space_toolsystem_toolbar import (
    VIEW3D_PT_tools_active as view3d_tools
)
from bpy.types import (
    # WorkSpaceTool,
    # Operator,
    GizmoGroup,
)
from ..Utilities.DeepInspect import (
    isModalRunning
)

def active_tool():
    return view3d_tools.tool_active_from_context(bpy.context)


def get_tools():
    return view3d_tools.tools_from_context(bpy.context)

def get_transform():
    if bpy.context.mode == 'EDIT_MESH':
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        active = bm.select_history.active
    elif bpy.context.mode == 'OBJECT':
        obj = bpy.context.active_object

def make_button2d(group):
    button = group.gizmos.new('GIZMO_GT_move_3d')
    # button.shape = GizmoGeometry.ur_tab
    button.draw_options = {'ALIGN_VIEW', }
    # button.draw_style = 'CROSS_2D'

    button.scale_basis = 0.5
    button.alpha = 0.75
    button.line_width = 2.0

    button.color = (0.35, 0.55, 0.55)
    button.color_highlight = (0.45, 0.75, 0.75)

    button.use_draw_modal = True
    button.use_draw_value = True
    button.use_draw_offset_scale = True
    button.use_draw_scale = True

    return button


class ATB_TabletGizmoGroup(GizmoGroup):
    bl_idname = "ATB_TG_GG"
    bl_label = "Tablet Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'SHOW_MODAL_ALL', }

    @classmethod
    def poll(cls, context):
        if bpy.context.workspace.modals.tablet_modal:
            if isModalRunning():
                return True

    def setup(self, context):
        scene = context.scene
        cursor = scene.cursor

        button_a = make_button2d(self)

        op = button_a.target_set_operator("act.context_op")


        op.def_op = "wm.call_menu_pie"
        op.def_op_args = "'INVOKE_DEFAULT', True"
        op.def_op_props = (
                              "{"
                              "'name': 'VIEW3D_MT_ATB_tablet_pie',"
                              "}"
                            )

        op.ctrl_op = "wm.call_menu_pie"
        op.ctrl_op_args = "'INVOKE_DEFAULT', True"
        op.ctrl_op_props = (
                              "{"
                              "'name': 'VIEW3D_MT_PIE_quick_snap',"
                              "}"
                            )

        op.alt_op = "wm.call_panel"
        op.alt_op_args = "'INVOKE_DEFAULT', True"
        op.alt_op_props = (
                              "{"
                              "'name': 'VIEW3D_PT_view3d_fast_panel',"
                              "}"
                            )

        op.shift_op = "transform.translate"
        op.shift_op_args = "'INVOKE_DEFAULT', True"
        op.shift_op_props = (
                              "{"
                              "'cursor_transform': True,"
                              "}"
                            )

        button_a.matrix_basis = cursor.matrix

        self.button_a = button_a

    def refresh(self, context):
        scene = context.scene
        cursor = scene.cursor

        button_a = self.button_a

        button_a.matrix_basis = cursor.matrix

        self.button_a = button_a

    def draw_prepare(self, context):
        scene = context.scene
        cursor = scene.cursor

        button_a = self.button_a

        button_a.matrix_basis = cursor.matrix

        self.button_a = button_a