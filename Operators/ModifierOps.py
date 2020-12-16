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
import mathutils
from bpy.props import (
    StringProperty,
    IntProperty,
    IntVectorProperty,
    EnumProperty,
    BoolProperty,
    FloatProperty,
    PointerProperty
)

# Some utility functions for mucking with operators


def has_obj_pointer(mod):
    if mod.type in {'ARRAY', 'MIRROR'}:
        return True
    else:
        return False


def get_mod_object(mod):
    if mod.type == 'ARRAY':
        if mod.offset_object:
            return mod.offset_object
    elif mod.type == 'MIRROR':
        if mod.mirror_object:
            return mod.mirror_object
    elif mod.type in {'BOOLEAN', 'SCREW', 'HOOK',}:
        if mod.object:
            return mod.object
    elif mod.type == 'SIMPLE_DEFORM':
        if mod.origin:
            return mod.origin
    elif mod.type == 'WARP':
        objs = []
        if mod.object_from:
            objs.append(mod.object_from)
        if mod.object_to:
            objs.append(mod.object_to)
        if len(objs) > 0:
            return objs
    elif mod.type == 'WAVE':
        objs = []
        if mod.start_position_object:
            objs.append(mod.start_position_object)
        if mod.texture_coords_object:
            objs.append(mod.texture_coords_object)
        if len(objs) > 0:
            return objs
    elif mod.type == 'SHRINKWRAP':
        objs = []
        if mod.auxiliary_target:
            objs.append(mod.auxiliary_target)
        if mod.target:
            objs.append(mod.target)
        if len(objs) > 0:
            return objs


def get_mod_objects(context):
    empties = []
    for obj in context.selected_editable_objects:
        if obj.type == 'MESH':
            for mod in obj.modifiers:
                if has_obj_pointer(mod):
                    empties.append(get_mod_object(mod))
    return empties


def delta_value(mod, propname, val, sub=0):
    prop = getattr(mod, propname)
    if type(prop) == mathutils.Vector:
        prop[sub] += val
    else:
        prop += val
    setattr(mod, propname, prop)

def set_value(mod, propname, val, sub=0):
    prop = getattr(mod, propname)
    if type(prop) == mathutils.Vector:
        prop[sub] = val
    else:
        prop = val
    setattr(mod, propname, prop)


def get_mod_modal_hook(mod, sub):
    if mod.type == 'BEVEL':
        if sub == 0:
            return 'width'
        elif sub == 1:
            return 'segments'
        elif sub == 2:
            return 'profile'

    if mod.type == 'SOLIDIFY':
        if sub == 0:
            return 'thickness'
        elif sub == 1:
            return 'offset'
        elif sub == 2:
            return 'bevel_convex'

    if mod.type == 'ARRAY':
        if sub == 0:
            return 'constant_offset_displace'
        elif sub == 1:
            return 'count'
        elif sub == 2:
            return 'bevel_convex'


class ATB_OT_AddModifier(bpy.types.Operator):
    """Edit Mode Context menu for out-of-mode objects"""
    bl_idname = "atb.add_modifier"
    bl_label = "ATB Add Modifier"
    bl_description = "Adds modifiers to one or more objects, with an optional adjustment modal"
    bl_options = {'REGISTER', 'UNDO', 'GRAB_CURSOR_X'}

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
        ("ARMATURE", "Armature", ""),
        ("CAST", "Cast", ""),
        ("CURVE", "Curve", ""),
        ("DISPLACE", "Displace", ""),
        ("HOOK", "Hook", ""),
        ("LAPLACIANDEFORM", "Laplacian Deform", ""),
        ("LATTICE", "Lattice", ""),
        ("MESH_DEFORM", "Mesh Deform", ""),
        ("SHRINKWRAP", "Shrinkwrap", ""),
        ("SIMPLE_DEFORM", "Simple Deform", ""),
        ("SMOOTH", "Smooth", ""),
        ("CORRECTIVE_SMOOTH", "Corrective Smooth", ""),
        ("LAPLACIANSMOOTH", "Laplacian Smooth", ""),
        ("SURFACE_DEFORM", "Surface Deform", ""),
        ("WARP", "Warp", ""),
        ("WAVE", "Wave", ""),
        ("VOLUME_DISPLACE", "Volume Displace", ""),
        ("CLOTH", "Cloth", ""),
        ("COLLISION", "Collision", ""),
        ("DYNAMIC_PAINT", "Dynamic Paint", ""),
        ("EXPLODE ", "Explode", ""),
        ("FLUID", "Fluid", ""),
        ("OCEAN", "Ocean", ""),
        ("PARTICLE_INSTANCE", "Particle Instance", ""),
        ("PARTICLE_SYSTEM", "Particle System", ""),
        ("SOFT_BODY", "Soft Body", ""),
        ("SURFACE", "Surface", ""),
        ("SIMULATION", "Simulation", ""),
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

    do_modal: BoolProperty(
        name="Do Modal Adjustment",
        description="",
        default=False
    )


    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) > 0:
            return True


    def prep_modifier(self, obj, mod, type):

        if type == 'BEVEL':
            mod.limit_method = 'WEIGHT'

        if type =='SOLIDIFY':
            mod.offset = 1
            mod.use_even_offset = True
            mod.use_quality_normals = True

        if type == 'ARRAY':
            mod.use_relative_offset = False
            mod.use_constant_offset = True


    def modal(self, context, event):

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            if event.value == 'PRESS':
                context.area.header_text_set(None)

                for pair in self.mod_dict:
                    pair[0].modifiers.remove(pair[1])

                return {'CANCELLED'}

        if event.type in {'LEFTMOUSE', 'ENTER'}:
            if event.value == 'PRESS':
                context.area.header_text_set(None)
                return {'FINISHED'}

        if event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:

            if event.type == 'WHEELUPMOUSE':
                delta = 1
            else:
                delta = -1

            for mod in self.mods:
                prop = get_mod_modal_hook(mod, 1)
                delta_value(mod, prop, delta)

            return {'RUNNING_MODAL'}

        if event.type in {'MOUSEMOVE'}:
            for mod in self.mods:
                x_delta = 0.1*abs(self.start_loc[0] - event.mouse_x)
                prop = get_mod_modal_hook(mod, 0)
                set_value(mod, prop, x_delta)
            return {'RUNNING_MODAL'}

        return {'RUNNING_MODAL'}


    def execute(self, context):
        return {'FINISHED'}


    def invoke(self, context, event):
        self.start_loc = (event.mouse_x, event.mouse_y)

        mods = []

        mod_dict = []

        for obj in bpy.context.selected_editable_objects:
            if obj.type == 'MESH':
                mod = obj.modifiers.new(self.name, self.modifier)
                self.prep_modifier(obj, mod, self.modifier)
                mods.append(mod)
                mod_dict.append((obj, mod))

        self.mods = mods
        self.mod_dict = mod_dict
        bpy.context.area.tag_redraw()
        bpy.context.scene.frame_current = bpy.context.scene.frame_current

        if self.do_modal:
            context.area.header_text_set("In ATB Modifier Modal")
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            return {'FINISHED'}


class ATB_OT_Modifier_Pie(bpy.types.Operator):
    """Edit Mode Context menu for out-of-mode objects"""
    bl_idname = "atb.mod_pie"
    bl_label = "ATB Modifier Pie"
    bl_description = "A pie menu for adding modifiers to multiple objects"

    def invoke(self, context, event): 
        def draw_pie(self, context):
            pie = self.layout.menu_pie()
            pie.operator_context = 'INVOKE_DEFAULT'

            # LEFT
            op = pie.operator(
                "atb.add_modifier",
                text="Bevel"
            )
            op.modifier = 'BEVEL'
            op.name = "ATB Bevel"
            op.do_modal = True

            # RIGHT
            op = pie.operator(
                "atb.add_modifier",
                text="Mirror"
            )
            op.modifier = 'MIRROR'
            op.name = "ATB Mirror"
            op.do_modal = False

            # BOTTOM
            op = pie.operator(
                "atb.add_modifier",
                text="Array"
            )
            op.modifier = 'ARRAY'
            op.name = "ATB Array"
            op.do_modal = True

            # TOP
            op = pie.operator(
                "atb.add_modifier",
                text="Solidify"
            )
            op.modifier = 'SOLIDIFY'
            op.name = "ATB Solidify"
            op.do_modal = True

            # TOP LEFT
            # TOP RIGHT
            # BOTTOM LEFT
            # BOTTOM RIGHT

        wm = context.window_manager
        wm.popup_menu_pie(event, draw_func=draw_pie, title="", icon='NONE')
        return {'FINISHED'}