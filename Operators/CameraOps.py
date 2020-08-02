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


class ATB_OT_Zoop(bpy.types.Operator):
    """Lets the user cycle between cameras in the scene.
        Mostly meant to be called from the UI, given how it handles
        input properties."""
    bl_idname = "atb.zoop"
    bl_label = "ATB Set Camera"
    bl_description = ("Cycles between cameras in a scene "
                      "by changing the view layer's active camera.")
    bl_options = {'REGISTER'}

    target_camera: StringProperty(
                        name="Target Camera",
                        description="The camera to cycle to.",
                        maxlen=1024,
    )

    def invoke(self, context, event):
        target = self.target_camera

        speed_default = context.preferences.view.smooth_view

        context.preferences.view.smooth_view = 500

        if (target == context.space_data.camera.name):
            bpy.ops.view3d.view_camera(
                        'INVOKE_DEFAULT',
                        False,
            )
        else:
            if context.region_data.view_perspective == 'CAMERA':
                context.region_data.view_perspective = 'PERSP'

            bpy.ops.wm.context_set_id(
                    'INVOKE_DEFAULT',
                    False,
                    data_path="space_data.camera",
                    value=target
            )

            bpy.ops.view3d.view_camera(
                        'INVOKE_DEFAULT',
                        False,
            )

        context.preferences.view.smooth_view = speed_default

        return {'FINISHED'}


class ATB_OT_Lock_Camera(bpy.types.Operator):
    """Locks the location and rotation of the selected camera"""
    bl_idname = "atb.lock_camera"
    bl_label = "ATB Lock Camera"
    bl_description = ("Toggles rotation and location locks "
                      "for the selected camera.")
    bl_options = {'BLOCKING', 'UNDO', 'REGISTER'}

    target_object: StringProperty(
                        name="Target Object",
                        description="The object to select.",
    )

    def invoke(self, context, event):

        obj = bpy.data.objects.get(self.target_object)

        if False in obj.lock_location or False in obj.lock_rotation:
            obj.lock_location = [True, True, True]
            obj.lock_rotation = [True, True, True]
        else:
            obj.lock_location = [False, False, False]
            obj.lock_rotation = [False, False, False]

        return {'FINISHED'}


class ATB_OT_Add_Camera_Keying_Set(bpy.types.Operator):
    """A UI-Only Operator for setting the active object selection"""
    bl_idname = "atb.add_camera_keyset"
    bl_label = "ATB Add Camera Keyset"
    bl_description = ("Adds and activates a keying set  "
                      "for camera settings.")
    bl_options = {'BLOCKING', 'UNDO', 'REGISTER'}

    target_object: StringProperty(
                        name="Target Object",
                        description="The object to select.",
    )

    def invoke(self, context, event):

        bpy.ops.anim.keying_set_add(
                'INVOKE_DEFAULT',
                False,
                )

        context.scene.keying_sets.active.bl_label = "CameraKeys"

        return {'FINISHED'}
