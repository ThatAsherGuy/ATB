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
    IntProperty,
    IntVectorProperty,
    EnumProperty,
    BoolProperty,
    FloatProperty,
    PointerProperty
)

class ATB_OT_AddModifier(bpy.types.Operator):
    """Edit Mode Context menu for out-of-mode objects"""
    bl_idname = "act.add_modifier"
    bl_label = "ATB Add Modifier"
    bl_description = "Moar, Moar, Moar, MOAR!"

    modifier_types = [
        ("DATA_TRANSFER", "Data Transfer", ""),
        ("MESH_CACHE", "Mesh Cache", ""),
        ("MESH_SEQUENCE_CACHE", "Mesh Sequence Cache", ""),
        ("NORMAL_EDIT", "Normal Edit", ""),
        ("WEIGHTED_NORMAL", "Weighted Normal", ""),
        ("UV_PROJECT", "UV Project", ""),
        ("UV_WARP", "UV Warp", ""),
        ("VERTED_WEIGHT_EDIT", "Vertex Weight Edit", ""),
        ("VERTEX_WEIGHT_MIX", "Vertex Weight Mix", ""),
        ("VERTEX_WEIGHT_PROXIMITY", "Vertex Weight Proximity", ""),
        ("ARRAY", "Array", ""),
        ("BEVEL", "Bevel", ""),
        ("BOOLEAN", "Boolean", ""),
        ("BUILD", "Build", ""),
        ("DECIMATE", "Decimate", ""),
        ("EDGE_SPLIT", "Edge Split", ""),
        ("MASK", "Mask", ""),
        ("MIRROR", "Mirror", ""),
        ("MESH_TO_VOLUME", "Mesh to Volume", ""),
        ("MULTIRES", "Multi-Res", ""),
        ("REMESH", "Remesh", ""),
        ("SCREW", "Screw", ""),
        ("SKIN", "Skin", ""),
        ("SOLIDIFY", "Solidify", ""),
        ("SUBSURF", "Subdivision Surface", ""),
        ("TRIANGULATE", "Triangulate", ""),
        ("VOLUME_TO_MESH", "Volume to Mesh", ""),
        ("WELD", "Weld", ""),
        ("WIREFRAME", "Wireframe", ""),
    ]

    modifier: EnumProperty(
        items=modifier_types,
        name="Modifier",
        default='BEVEL'
    )

    name: StringProperty(
        name="Operator Name",
        description="",
        maxlen=1024,
        default="Fred"
    )

    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) > 0:
            return True

    def execute(self, context):
        bpy.context.active_object.modifiers.new(self.name, self.modifier)
        bpy.context.area.tag_redraw()
        bpy.context.scene.frame_current = bpy.context.scene.frame_current
        return {'FINISHED'}

    def invoke(self, context, event): 
        self.execute(context)
        return {'FINISHED'}

