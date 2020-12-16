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
from ..Utilities.DeepInspect import (
    isModalRunning
)


def active_tool():
    return view3d_tools.tool_active_from_context(bpy.context)


def get_tools():
    return view3d_tools.tools_from_context(bpy.context)

def set_pivot(axis):
    obj = bpy.context.active_object
    axes = [
        mathutils.Quaternion((0.0, 1.0, 0.0), math.radians(90.0)), # X axis — 'Positive' (blender's axis order is fucky)
        mathutils.Quaternion((1.0, 0.0, 0.0), math.radians(-90.0)), # Y axis — Positive
        mathutils.Quaternion((0.0, 0.0, 1.0), math.radians(00.0)), # Z axis — Positive (no need to rotate)
        mathutils.Quaternion((0.0, 1.0, 0.0), math.radians(-90.0)), # X axis — Negative
        mathutils.Quaternion((1.0, 0.0, 0.0), math.radians(90.0)), # Y axis — Negative
        mathutils.Quaternion((1.0, 0.0, 0.0), math.radians(180.0)) # Z axis — Negative
        ]

    if obj:
        if bpy.context.workspace.modals.mm_use_cursor:
            pivot = mathutils.Matrix.Translation((obj.matrix_world.to_translation())).to_4x4()
            piv_axis = bpy.context.scene.cursor.matrix.to_quaternion().to_matrix().to_4x4()
            piv_axis = piv_axis @ axes[axis].to_matrix().to_4x4()
            # piv_axis = bpy.context.scene.cursor.matrix
        else:
            pivot = obj.matrix_world
            piv_axis = axes[axis].to_matrix().to_4x4()

        return pivot @ piv_axis

def set_color(axis):
    colors = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (0.85, 0.35, 0.35),
        (0.35, 0.85, 0.35),
        (0.35, 0.35, 0.85)
    ]
    return colors[axis]

def set_op(arrow, axis):
    axes = (
        "POSITIVE_X",
        "POSITIVE_Y",
        "POSITIVE_Z",
        "NEGATIVE_X",
        "NEGATIVE_Y",
        "NEGATIVE_Z",
    )
    props = arrow.target_set_operator("atb.quick_symmetry")
    props.mirror_axis = axes[axis]
    props.do_modal = False
    return axes[axis]


class ATB_MirrorGizmoGroup(GizmoGroup):
    bl_idname = "atb_mirror_gizmo_group"
    bl_label = "ATB Mirror Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'SHOW_MODAL_ALL'}

    @classmethod
    def poll(cls, context):
        if bpy.context.workspace.modals.mirror_modal:
            if isModalRunning():
                return True

    def setup(self, context):
        arrows = []
        for i in range(6):
            arrows.append(self.gizmos.new('GIZMO_GT_arrow_3d'))
            arrows[i].matrix_basis = set_pivot(axis=i)
            arrows[i].color = set_color(axis=i)
            arrows[i].draw_style = 'BOX'
            arrows[i].scale_basis = 2.5
            arrows[i].length = 0.5
            # arrows[i].line_width = 5.75
            set_op(arrows[i], i)
            # print(str(i))

        self.arrows = arrows


    def draw_prepare(self, context):
        arrows = self.arrows

        for i in range(6):
            arrows[i].matrix_basis = set_pivot(axis=i)
            arrows[i].color = set_color(axis=i)