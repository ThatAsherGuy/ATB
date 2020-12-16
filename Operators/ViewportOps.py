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
    EnumProperty,
    IntProperty
)
import math


def get_view_orientation_from_matrix(view_matrix):
    def r(x): return round(x, 2)
    view_rot = view_matrix.to_euler()

    orientation_dict = {(0.0, 0.0, 0.0): 'TOP',
                        (r(math.pi), 0.0, 0.0): 'BOTTOM',
                        (r(-math.pi/2), 0.0, 0.0): 'FRONT',
                        (r(math.pi/2), 0.0, r(-math.pi)): 'BACK',
                        (r(-math.pi/2), r(math.pi/2), 0.0): 'LEFT',
                        (r(-math.pi/2), r(-math.pi/2), 0.0): 'RIGHT'}

    return orientation_dict.get(tuple(map(r, view_rot)), view_rot)


def get_view_orientation_from_quaternion(view_quat):
    def r(x): return round(x, 3)
    view_rot = view_quat.to_euler()

    orientation_dict = {(0.0, 0.0, 0.0): 'TOP',
                        (r(math.pi), 0.0, 0.0): 'BOTTOM',
                        (r(math.pi/2), 0.0, 0.0): 'FRONT',
                        (r(math.pi/2), 0.0, r(math.pi)): 'BACK',
                        (r(math.pi/2), 0.0, r(-math.pi/2)): 'LEFT',
                        (r(math.pi/2), 0.0, r(math.pi/2)): 'RIGHT'}

    return orientation_dict.get(tuple(map(r, view_rot)), 'UNDEFINED')

# This axis operator was stolen from Machin3Tools


axisitems = [("FRONT", "Front", ""),
             ("BACK", "Back", ""),
             ("LEFT", "Left", ""),
             ("RIGHT", "Right", ""),
             ("TOP", "Top", ""),
             ("BOTTOM", "Bottom", "")]


def invert_view_axis(axis):
    if axis == 'FRONT':
        return 'BACK'
    elif axis == 'BACK':
        return 'FRONT'
    elif axis == 'LEFT':
        return 'RIGHT'
    elif axis == 'RIGHT':
        return 'LEFT'
    elif axis == 'TOP':
        return 'BOTTOM'
    elif axis == 'BOTTOM':
        return 'TOP'
    else:
        return 'BATMAN'


class ATB_OT_ViewAxis(bpy.types.Operator):
    """Select operator wrapper with a pie menu for fancy things"""
    bl_idname = "atb.view_axis"
    bl_label = "ATB View Axis"
    bl_description = (
                    "Click: Align View\n"
                    "Ctrl + Click: Align View to Positive Normal\n"
                    "Ctrl + Shift + Click: Align View to Negative Normal"
                    )
    bl_options = {'REGISTER'}

    axis: EnumProperty(name="Axis", items=axisitems, default="FRONT")

    speed: IntProperty(
        name="Transition Speed",
        default=200,
        min=0,
        max=1000,
    )

    def invoke(self, context, event):
        region = context.region_data
        view_quat = region.view_rotation
        view = get_view_orientation_from_quaternion(view_quat)

        speed_default = context.preferences.view.smooth_view

        context.preferences.view.smooth_view = self.speed

        # Flip view when calling current view, but not when holding Ctrl
        axis_flip = self.axis
        if self.axis == view and not event.ctrl:
            axis_flip = invert_view_axis(self.axis)

        # align to active when holding Ctrl
        align = False
        if event.ctrl:
            align = True

        # allow flipping when both are held
        if event.ctrl and event.shift:
            axis_flip = invert_view_axis(self.axis)

        bpy.ops.view3d.view_axis('INVOKE_DEFAULT', True, type=axis_flip, align_active=align)
        context.preferences.view.smooth_view = speed_default
        return {'FINISHED'}

# XXX Has issues getting region data


class ATB_OT_set_axis(bpy.types.Operator):
    """Select operator wrapper with a pie menu for fancy things"""
    bl_idname = "atb.set_axis"
    bl_label = "ATB Set Axis"
    bl_description = "Turn arbitrary inputs into viewport camera alignments"
    bl_options = {'REGISTER'}

    def invoke(self, context, event):

        srt_mat = mathutils.Matrix.Identity(3)
        swing_1 = mathutils.Matrix.Rotation(math.radians(45), 3, 'Z')
        swing_2 = mathutils.Matrix.Rotation(math.atan(math.sqrt(2)), 3, 'X')
        iso_mat = srt_mat @ swing_1 @ swing_2

        region = context.region_data

        if region:
            region.view_rotation = iso_mat.to_quaternion()
        else:
            print("NOPE")
        return {'FINISHED'}
