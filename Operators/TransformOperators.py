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

import bpy
from bpy.props import (
    FloatVectorProperty,
)


class ATB_OT_RotateAroundPivot(bpy.types.Operator):
    """Wrapper for transform.rotate"""
    bl_idname = "act.rotate_around_pivot"
    bl_label = "ATB Rotate Around Pivot"
    bl_description = "Wrapper for transform.rotate"
    bl_options = {'REGISTER', 'UNDO'}

    offset: FloatVectorProperty(
        name="Pivot Offset",
        description="Pivot offset vector",
        default=(0.0, 0.0, 0.0)
    )

    def invoke(self, context, event):
        bpy.ops.transform.rotate(
            'INVOKE_DEFAULT',
            orient_axis='Z',
            orient_type='GLOBAL',
            center_override=self.offset,
            constraint_axis=(True, True, True)
        )
        bpy.context.area.tag_redraw()
        return {'FINISHED'}
