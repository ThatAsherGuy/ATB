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


class ATB_PreselectGizmoGroup(GizmoGroup):
    bl_idname = "ATB_preselect_gizmo"
    bl_label = "Pivot Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'SHOW_MODAL_ALL', 'SCALE'}

    @classmethod
    def poll(cls, context):
        # return False
        if bpy.context.mode == 'EDIT_MESH':
            return True

    def setup(self, context):
        self.giz = self.gizmos.new('GIZMO_GT_mesh_preselect_elem_3d')

    # def draw_prepare(self, context):
    #     # vert = self.giz.vert_index
    #     print(str("vert"))

    def refresh(self, context):
        scene = context.scene
