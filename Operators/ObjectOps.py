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
from bpy.props import (
    StringProperty,
    # EnumProperty,
    # IntProperty
)

class ATB_OT_AddBasePlane(bpy.types.Operator):
    bl_idname = "atb.add_base_plane"
    bl_label = "ATB Add Base Plane"
    bl_description = ("Cycles between cameras in a scene "
                      "by changing the view layer's active camera.")
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.mesh.primitive_plane_add(
            size=1, calc_uvs=False, enter_editmode=False)
        # bpy.ops.transform.resize(value=[xdim, ydim, 1.0])
        # bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # bpy.context.active_object.hide_viewport = True
        bpy.context.active_object.hide_render = True
        bpy.context.active_object.display_type = "WIRE"
        bpy.context.active_object.display.show_shadows = False

        # bpy.context.active_object.name = objname

        new_obj = bpy.context.active_object
        bpy.ops.object.select_all(action='DESELECT')
        return {"FINISHED"}