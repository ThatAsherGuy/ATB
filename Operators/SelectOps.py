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
import functools


class ATB_OT_SuperContextMenu(bpy.types.Operator):
    """Edit Mode Context menu for out-of-mode objects"""
    bl_idname = "act.moar_context"
    bl_label = "ATB Moar Context"
    bl_description = "Moar, Moar, Moar, MOAR!"

    def invoke(self, context, event):
        m_x = event.mouse_region_x
        m_y = event.mouse_region_y
        m_loc = (m_x, m_y)

        self.m_loc = m_loc

        bpy.ops.view3d.select(
            'INVOKE_REGION_WIN',
            False,
            extend=False,
            center=True,
            object=True,
            location=self.m_loc
        )

        override = bpy.context.copy()

        for obj in context.selected_objects:
            for ed_obj in context.objects_in_mode:
                if not obj.data == ed_obj.data:
                    override['edit_object'] = None

        def draw_menu(self, context):
            menu = self.layout
            menu.operator_context = 'INVOKE_DEFAULT'

            op = menu.operator("act.add_to_mode", text="Add to Mode")
            op.mouse_loc = m_loc

            op = menu.operator("act.move_cursor", text="Cursor to Origin")
            op.move_mode = 'RED'

            op = menu.operator("act.move_cursor", text="FUCK YOUR ORIGIN")
            op.move_mode = 'GREEN'

        wm = context.window_manager
        wm.popup_menu(draw_func=draw_menu, title="", icon='NONE')
        return {'FINISHED'}


class ATB_OT_SelectThrough(bpy.types.Operator):
    """Wrapper for editmode_toggle that uses overrides to enable mode expansion"""
    bl_idname = "act.select_through"
    bl_label = "ATB Select Through"
    bl_description = "Give your balls a tug, Shorsey"

    def modal(self, context, event):
        def flerb(context):
            override = bpy.context.copy()
            override['window'] = context.window
            bpy.ops.mesh.select_mode(
                override,
                'INVOKE_DEFAULT',
                False,
                type='FACE',
                use_expand=True
            )

        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            bpy.app.timers.register(bpy.ops.mesh.select_mode, first_interval=1)
            return {'FINISHED', 'PASS_THROUGH'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        m_x = event.mouse_region_x
        m_y = event.mouse_region_y
        m_loc = (m_x, m_y)

        self.m_loc = m_loc

        bpy.ops.mesh.select_mode(
            'INVOKE_REGION_WIN',
            False,
            type='VERT',
        )
        op = bpy.ops.view3d.select_box(
            'INVOKE_REGION_WIN',
            False,
            wait_for_input=False
        )
        print(str(op))

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
