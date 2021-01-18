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
from mathutils import Matrix, Vector, Quaternion
import math
import msvcrt
import time
import datetime
import winsound

from ..Utilities.DeepInspect import (
    isModalRunning
)

from ..Utilities.DeepInspect_Alt import isModalRunning_Alt

from ..Utilities.InputCombos import add_input

from ..Utilities.Draw import draw_modal_text_px
from ..Utilities.Draw import make_batch_edges
from ..Utilities.Draw import draw_batch


class ATB_OT_SuperTabletPie(bpy.types.Operator):
    """A pie menu for tablet users, wrapped in an operator so we can do input event processing"""
    bl_idname = "atb.super_tablet_pie"
    bl_label = "ATB Super Tablet Pie"
    bl_description = """Fancy Things"""
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        val = isModalRunning()
        return not val


    def execute(self, context):
        print("FIN")
        return {'FINISHED'}


    def modal(self, context, event):
        context.area.header_text_set("In ATB Tablet Modal")

        if event.type in {'MOUSEMOVE', 'MIDDLEMOUSE'}:
            dist = abs(self.m_loc[0] - event.mouse_region_x) + abs(self.m_loc[1] - event.mouse_region_y)

            if dist > 50:
                self.lclick_down = False
                self.lclick_time = 0.0
                self.lclick_long = False
            return {'PASS_THROUGH'}

        if event.type == 'SPACE':
            if (event.value == 'PRESS') and (event.is_repeat == False):
                self.spacemod = True
            elif event.value == 'RELEASE':
                self.spacemod = False

        if event.type == 'SPACE':
            giz = context.gizmo_group
            print(str(giz))

        if event.type == 'LEFTMOUSE':
            if (event.value == 'CLICK_DRAG') and (event.pressure < 0.2):
                bpy.ops.transform.translate('INVOKE_DEFAULT', True, cursor_transform=True)
                return {'RUNNING_MODAL'}

            if (event.value == 'PRESS') and (event.is_repeat == False):

                self.m_loc = (event.mouse_region_x, event.mouse_region_y)

                self.lclick_time = time.time()
                self.lclick_down = True
                self.armed = True

                return {'PASS_THROUGH'}

            if event.value == 'CLICK':
                t = time.time() - self.lclick_time

                if (t > 0.75) and (t < 5.75) and (self.armed):

                    self.lclick_down = False
                    self.lclick_long = False

                    bpy.ops.mesh.loop_select('INVOKE_DEFAULT', True, extend=True, deselect=False, toggle=False, ring=False)

                    self.lclick_time = time.time()
                    self.armed = False
                    return {'RUNNING_MODAL'}

                self.lclick_down = False
                self.lclick_time = 0.0
                self.lclick_long = False
            return {'PASS_THROUGH'}

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            if event.value == 'CLICK':

                context.area.header_text_set(None)
                bpy.context.workspace.modals.tablet_modal = False
                bpy.context.window_manager.gizmo_group_type_unlink_delayed("ATB_TG_GG")

                return {'CANCELLED'}
            else:
                return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}


    def invoke(self, context, event):
        m_x = event.mouse_region_x
        m_y = event.mouse_region_y
        m_loc = (m_x, m_y)

        self.m_loc = m_loc
        self.victim = -1
        self.face_2d_sel = (0, 0)

        context.area.header_text_set("In ATB Tablet Modal")

        bpy.context.workspace.modals.tablet_modal = True
        bpy.context.window_manager.gizmo_group_type_ensure("ATB_TG_GG")

        self.tablet = False

        self.spacemod = False

        self.lclick_down = False
        self.lclick_time = 0.0
        self.lclick_long = False

        self.armed = True

        if event.is_tablet:
            self.tablet = True

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class ATB_OT_RhythmInvoke(bpy.types.Operator):
    bl_idname = "atb.tap_it"
    bl_label = "ATB TAP"
    bl_description = """Fancy Things"""
    # bl_options = {'REGISTER'}

    def invoke(self, context, event):
        combo_state = context.window_manager.ATB
        add_input(context, event)

        print(combo_state.combo_seq)

        if combo_state.combo_seq == "qsq":
            print("META PIE")
            combo_state.combo_seq = ""
            combo_state.last_tap = -1
            winsound.Beep(1250, 250)
            bpy.ops.atb.meta_pie('INVOKE_DEFAULT')

        if combo_state.combo_seq == "qqq":
            print("SUPER SELECT")
            combo_state.combo_seq = ""
            combo_state.last_tap = -1
            winsound.Beep(1250, 250)
            bpy.ops.atb.super_select('INVOKE_DEFAULT')

        if combo_state.combo_seq == "qss":
            print("Save Pie")
            combo_state.combo_seq = ""
            combo_state.last_tap = -1
            winsound.Beep(1250, 250)
            bpy.ops.atb.save_pie('INVOKE_DEFAULT')

        if len(combo_state.combo_seq) > 7:
            print("RESET")
            combo_state.combo_seq = ""
            combo_state.last_tap = -1

        return {'FINISHED'}

class ATB_OT_DRAW(bpy.types.Operator):
    bl_idname = "atb.draw_it"
    bl_label = "ATB DRAW"
    bl_description = """Fancy Things"""
    # bl_options = {'REGISTER'}

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'MOUSEMOVE':
            self.loc = (event.mouse_region_x, event.mouse_region_y)
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._mesh_handle, 'WINDOW')
            return {'CANCELLED'}
        else:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            args = (self, context)
            

            self.loc = (event.mouse_region_x, event.mouse_region_y)
            self.offset = (20, 20)

            self.obj = bpy.context.active_object

            mesh_batch, mesh_shader = make_batch_edges(self, context)
            mesh_args = (self, context, mesh_shader, mesh_batch)
            self._mesh_handle = bpy.types.SpaceView3D.draw_handler_add(draw_batch, mesh_args, 'WINDOW', 'POST_VIEW')

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

        return {'CANCELLED'}