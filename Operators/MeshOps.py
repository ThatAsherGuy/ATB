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
    FloatVectorProperty,
    EnumProperty,
    BoolProperty
)

class ATB_OT_QuickSymmetry(bpy.types.Operator):
    """A wrapper for the symmetrize operator with an (optional) modal gizmo"""
    bl_idname = "atb.quick_symmetry"
    bl_label = "ATB Quick Symmetry"
    bl_description = "A wrapper for the symmetrize operator with an (optional) modal gizmo"
    bl_options = {'UNDO_GROUPED'}

    axes = [
        ("POSITIVE_Z", "Z+", "", 1),
        ("NEGATIVE_Z", "Z-", "", 2),
        ("POSITIVE_Y", "Y+", "", 3),
        ("NEGATIVE_Y", "Y-", "", 4),
        ("POSITIVE_X", "X+", "", 5),
        ("NEGATIVE_X", "X-", "", 6),
    ]

    mirror_axis: EnumProperty(
        items=axes,
        name="Axis",
        description="Which axis to mirror",
        default='POSITIVE_Z'
    )

    do_modal: BoolProperty(
        name="Do Modal",
        default=True
    )

    use_cursor: BoolProperty(
        name="Use Cursor Orientation",
        default=False
    )

    def modal(self, context, event):

        if bpy.context.gizmo_group:
            print(bpy.context.gizmo_group.bl_idname)

        if bpy.context.workspace.modals.mirror_modal == False:
            context.area.header_text_set(None)
            bpy.context.window_manager.gizmo_group_type_unlink_delayed("atb_mirror_gizmo_group")
            return {'FINISHED'}

        if (event.type in {'LEFT_SHIFT', 'RIGHT_SHIFT', 'SPACE'}) and (event.value == 'PRESS'):
            bpy.context.workspace.modals.mm_use_cursor = True
            bpy.context.area.tag_redraw()

        if (event.type in {'LEFT_SHIFT', 'RIGHT_SHIFT', 'SPACE'}) and (event.value == 'RELEASE'):
            bpy.context.workspace.modals.mm_use_cursor = False
            bpy.context.area.tag_redraw()

        if event.type in {'LEFTMOUSE', 'MIDDLEMOUSE', 'MOUSEMOVE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            if event.value == 'CLICK':
                if bpy.context.workspace.modals.mirror_modal == False:
                    return {'PASS_THROUGH', 'FINISHED'}
            return {'PASS_THROUGH'}

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            context.area.header_text_set(None)
            bpy.context.window_manager.gizmo_group_type_unlink_delayed("atb_mirror_gizmo_group")
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        bpy.context.workspace.modals.mm_use_cursor = False
        do_mode = True if bpy.context.mode == 'EDIT_MESH' else False

        if event.shift:
            self.use_cursor = True

        if self.do_modal:
            context.area.header_text_set("In ATB Mirror Modal, Press Esc to Exit")

            bpy.context.workspace.modals.mirror_modal = True

            bpy.context.window_manager.gizmo_group_type_ensure("atb_mirror_gizmo_group")

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            if self.use_cursor:
                if not bpy.context.mode == 'OBJECT':
                    bpy.ops.object.editmode_toggle('EXEC_DEFAULT', False)

                bpy.ops.transform.create_orientation(
                                'EXEC_DEFAULT',
                                False,
                                name="_TEMPSYM",
                                use=False,
                                use_view=False)

                context.scene.tool_settings.use_transform_data_origin = True
                bpy.ops.transform.transform('EXEC_DEFAULT', False, mode='ALIGN', orient_type='CURSOR')
                context.scene.tool_settings.use_transform_data_origin = False

            if bpy.context.mode == 'OBJECT':
                bpy.ops.object.editmode_toggle('EXEC_DEFAULT', False)

            bpy.ops.mesh.select_all('EXEC_DEFAULT', False, action='SELECT')
            bpy.ops.mesh.symmetrize('EXEC_DEFAULT', False, direction=self.mirror_axis)
            bpy.ops.mesh.select_all('EXEC_DEFAULT', False, action='DESELECT')

            bpy.context.workspace.modals.mirror_modal = False
            context.area.header_text_set(None)

            if self.use_cursor:
                if not bpy.context.mode == 'OBJECT':
                    bpy.ops.object.editmode_toggle('EXEC_DEFAULT', False)

                context.scene.tool_settings.use_transform_data_origin = True
                bpy.ops.transform.transform('EXEC_DEFAULT', False, mode='ALIGN', orient_type='_TEMPSYM')
                context.scene.tool_settings.use_transform_data_origin = False

                bpy.context.scene.transform_orientation_slots[0].type = '_TEMPSYM'
                bpy.ops.transform.delete_orientation('EXEC_DEFAULT', False)

                if do_mode:
                    bpy.ops.object.editmode_toggle('EXEC_DEFAULT', False)
            return {'FINISHED'}