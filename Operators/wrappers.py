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
import ast
from . import ViewportOps
import mathutils
from bpy.props import (
    StringProperty,
    IntProperty,
    IntVectorProperty,
    EnumProperty,
    BoolProperty,
    FloatProperty,
    FloatVectorProperty,
    IntVectorProperty,
    PointerProperty
)
import bpy_extras
import bmesh
import math
import types
import os
import re
import sys


# Yoinked directly from MachineTools
def add_path_to_recent_files(path):
    enc = sys.getfilesystemencoding()

    try:
        recent_path = bpy.utils.user_resource('CONFIG', "recent-files.txt")
        with open(recent_path, "r+", encoding=enc) as f:
            content = f.read()
            f.seek(0, 0)
            f.write(path.rstrip('\r\n') + '\n' + content)

    except (IOError, OSError, FileNotFoundError):
        pass


class ATB_OT_SaveIncremental(bpy.types.Operator):
    """Pretty much the save function from MachineTools"""
    bl_idname = "atb.save_incremental"
    bl_label = "ATB Incremental Save"
    bl_description = "Creates an incremental save"

    def increment_path(self, current):
        path = os.path.dirname(current)
        name = os.path.basename(current)

        name_regex = re.compile(r"(.+)\.blend\d*$")

        do = name_regex.match(name)

        if do:
            save_name = do.group(1)
            number_regex = re.compile(r"(.*?)(\d+)$")

            do = number_regex.match(save_name)

            if do:
                base = do.group(1)
                number = do.group(2)
            else:
                base = save_name + "_"
                number = "000"

            incr = int(number) + 1
            incrstr = str(incr).zfill(len(number))
            incrname = base + incrstr + ".blend"

            return os.path.join(path, incrname)

    def execute(self, context):
        current = bpy.data.filepath

        if current:
            path = self.increment_path(current)
            add_path_to_recent_files(path)

            if os.path.exists(path):
                self.report({'ERROR'}, "FAILED TO INCREMENT")
            else:
                bpy.ops.wm.save_as_mainfile(filepath=path)
                print("Saved Incrementally: ", path)
        else:
            bpy.ops.save_mainfile('INVOKE_DEFAULT')
        
        return {'FINISHED'}

# For header buttons, doesn't push an undo
class ATB_OT_BoolToEnum(bpy.types.Operator):
    """Takes a BoolVector and an Enum, makes them play nice"""
    bl_idname = "atb.bool_to_enum"
    bl_label = "ATB Bool to Enum"
    bl_description = "Takes a BoolVector and an Enum, makes them play nice"

    bool_prop: StringProperty(
                        name="Bool Path",
                        description="Path to Bool",
                        maxlen=1024,
    )

    enum_prop_path: StringProperty(
                        name="Enum Path",
                        description="Path to Enum",
                        maxlen=1024,
    )

    bool_index: IntProperty(
                        name="Bool Index",
                        default=0,
                        min=0,
                        max=10
    )

    def invoke(self, context, event):
        bool_prop = self.bool_prop
        bool_index = self.bool_index
        bp_compl = str(bool_prop) + "[" + str(bool_index) + "]"
        enum_prop_path = self.enum_prop_path

        wm = bpy.context.window_manager
        mp_props = wm.ATB

        bpy.ops.wm.context_toggle(
                'INVOKE_DEFAULT',
                False,
                data_path=bp_compl
        )

        if mp_props.mp_shading_cavtoggle[0] and mp_props.mp_shading_cavtoggle[1]:
            bpy.ops.wm.context_set_enum(
                'INVOKE_DEFAULT',
                False,
                data_path=enum_prop_path,
                value='BOTH',
            )
        elif mp_props.mp_shading_cavtoggle[0]:
            bpy.ops.wm.context_set_enum(
                'INVOKE_DEFAULT',
                False,
                data_path=enum_prop_path,
                value='SCREEN',
            )
        elif mp_props.mp_shading_cavtoggle[1]:
            bpy.ops.wm.context_set_enum(
                'INVOKE_DEFAULT',
                False,
                data_path=enum_prop_path,
                value='WORLD',
            )

        if not mp_props.mp_shading_cavtoggle[0] and not mp_props.mp_shading_cavtoggle[1]:
            bpy.ops.wm.context_toggle(
                    'INVOKE_DEFAULT',
                    False,
                    data_path="space_data.shading.show_cavity"
            )

        if (
                not context.space_data.shading.show_cavity
                and (mp_props.mp_shading_cavtoggle[0] or mp_props.mp_shading_cavtoggle[1])):
            bpy.ops.wm.context_toggle(
                    'INVOKE_DEFAULT',
                    False,
                    data_path="space_data.shading.show_cavity"
            )
        bpy.context.area.tag_redraw()
        return {'FINISHED'}


# For header buttons, forces a re-draw, doesn't push an undo
class ATB_OT_CycleEnum(bpy.types.Operator):
    """Wrapper for context_cycle_enum that updates the 3d viewport"""
    bl_idname = "atb.cycle_enum"
    bl_label = "ATB Cycle Enum"
    bl_description = "Wrapper for context_cycle_enum"

    path: StringProperty(
        name="Data Path",
        description="Path to Enum",
        maxlen=1024,
    )

    def invoke(self, context, event):
        path = self.path
        bpy.ops.wm.context_cycle_enum(
            'INVOKE_DEFAULT',
            False,
            data_path=path,
            wrap=True
        )
        bpy.context.area.tag_redraw()
        return {'FINISHED'}


# For Panel tabs, doesn't push an undo
class ATB_OT_SetEnum(bpy.types.Operator):
    """Wrapper for context_set_enum that updates the 3d viewport"""
    bl_idname = "atb.set_enum"
    bl_label = "ATB Set Enum and Update"
    bl_description = "Wrapper for context_set_enum"

    path: StringProperty(
        name="Data Path",
        description="Path to Enum",
        maxlen=1024,
    )

    value: StringProperty(
        name="Enum Value",
        description="Enum Value",
        maxlen=1024,
    )

    def invoke(self, context, event):
        path = self.path
        value = self.value
        bpy.ops.wm.context_set_enum(
            'INVOKE_DEFAULT',
            False,
            data_path=path,
            value=value,
        )
        # bpy.context.area.tag_redraw() <-- Might re-enable this later on
        return {'FINISHED'}

# TODO: I should be able to finesse this with some **kwargs shenanigans
# A general-purpose dynamic operator operator.
class ATB_OT_ContextOp(bpy.types.Operator):
    """Root Operator for checking modifer key status on operator invocation"""
    bl_idname = "atb.context_op"
    bl_label = "ATB Context Operator"
    bl_description = """Calls different operators depending on the modifier key pressed"""
    bl_options = {'REGISTER'}

    def_op: StringProperty(
        name="Default Operator",
        description="The Operator called when no modifer keys are pressed",
        maxlen=1024,
    )
    def_op_args: StringProperty(
        name="Default Operator Arguments",
        description="Arguments used with the default operator",
        maxlen=1024,
    )
    def_op_props: StringProperty(
        name="Default Operator Arguments",
        description="Properties used with the default operator",
        maxlen=1024,
    )

    ctrl_op: StringProperty(
        name="CTRL Operator",
        description="The Operator called when the ctrl key is pressed",
        maxlen=1024,
    )
    ctrl_op_args: StringProperty(
        name="Default Operator Arguments",
        description="Arguments used with the default operator",
        maxlen=1024,
    )
    ctrl_op_props: StringProperty(
        name="Default Operator Arguments",
        description="Properties used with the default operator",
        maxlen=1024,
    )

    alt_op: StringProperty(
        name="ALT Operator",
        description="The Operator called when the alt key is pressed",
        maxlen=1024,
    )
    alt_op_args: StringProperty(
        name="Default Operator Arguments",
        description="Arguments used with the default operator",
        maxlen=1024,
    )
    alt_op_props: StringProperty(
        name="Default Operator Arguments",
        description="Properties used with the default operator",
        maxlen=1024,
    )

    shift_op: StringProperty(
        name="SHIFT Operator",
        description="The Operator called when the shift key is pressed",
        maxlen=1024,
    )
    shift_op_args: StringProperty(
        name="Default Operator Arguments",
        description="Arguments used with the default operator",
        maxlen=1024,
    )
    shift_op_props: StringProperty(
        name="Default Operator Arguments",
        description="Properties used with the default operator",
        maxlen=1024,
    )

    ctrl_shift_op: StringProperty(
        name="CTRL + SHIFT Operator",
        description="""
                    The Operator called when
                    the shift and ctrl keys are pressed""",
        maxlen=1024,
    )
    ctrl_shift_op_args: StringProperty(
        name="Default Operator Arguments",
        description="Arguments used with the default operator",
        maxlen=1024,
    )
    ctrl_shift_op_props: StringProperty(
        name="Default Operator Arguments",
        description="Properties used with the default operator",
        maxlen=1024,
    )

    def attempt(self, context, _op, args, props, db=False):
        use_args = False
        use_props = False

        op_split = _op.split(".")

        if not _op.startswith("atb."):
            operator = getattr(getattr(bpy.ops, op_split[0]), op_split[1])

        if args:
            args_split = args.split(", ")
            if len(args_split) == 3:
                override_context = args_split[0]
                execution_context = str(args_split[1].strip("'"))
                undo = (True if args_split[2] == "True" else False)
                args = (override_context, execution_context, undo)
                use_args = True
            elif len(args_split) == 2:
                execution_context = str(args_split[0].strip("'"))
                undo = (True if args_split[1] == "True" else False)
                args = (execution_context, undo)
                use_args = True
            else:
                self.report({'WARNING'}, "Incorrect Operator Arguments")

        if props:
            prop_dict = ast.literal_eval(props)
            use_props = True

        if db:
            self.report({'INFO'}, "Use Props: " + str(use_props))
            self.report({'INFO'}, "Use Args: " + str(use_args))

        # try:
        if _op.startswith("atb."):
            full = "bpy.ops." + _op + "('INVOKE_DEFAULT', True)"
            if db:
                self.report({'INFO'}, "Custom Operator: " + str(full))
            exec(full)
        elif use_props:
            operator.__call__(*args, **prop_dict)
        elif use_args:
            operator.__call__(*args)
        else:
            operator.__call__()
        # except RuntimeError:
        #     self.report({'INFO'}, "The developer is an idiot")

    def invoke(self, context, event):
        if event.ctrl:
            if event.shift:
                if self.ctrl_shift_op:
                    self.attempt(
                                context,
                                self.ctrl_shift_op,
                                self.ctrl_shift_op_args,
                                self.ctrl_shift_op_props
                                )
                else:
                    self.attempt(context, self.def_op, self.def_op_args, self.def_op_props)
            else:
                if self.ctrl_op:
                    self.attempt(context, self.ctrl_op, self.ctrl_op_args, self.ctrl_op_props)
                else:
                    self.attempt(context, self.def_op, self.def_op_args, self.def_op_props)
        elif event.alt:
            if self.alt_op:
                self.attempt(context, self.alt_op, self.alt_op_args, self.alt_op_props)
            else:
                self.attempt(context, self.def_op, self.def_op_args, self.def_op_props)
        elif event.shift:
            if self.shift_op:
                self.attempt(context, self.shift_op, self.shift_op_args, self.shift_op_props)
            else:
                self.attempt(context, self.def_op, self.def_op_args, self.def_op_props)
        else:
            self.attempt(context, self.def_op, self.def_op_args, self.def_op_props)
            # exec(op)

        return {'FINISHED'}


# TODO: Do I actually use this operator? Might be able to nix it.
class ATB_OT_MouseContextOp(bpy.types.Operator):
    """Root Operator for checking mouse button status on operator invocation"""
    bl_idname = "atb.mouse_context_op"
    bl_label = "ATB Mouse Context Operator"
    bl_description = """Calls different operators depending on the mouse button pressed"""
    bl_options = {'REGISTER'}

    left_op: StringProperty(
        name="Default Operator",
        description="The Operator called when no modifer keys are pressed",
        maxlen=1024,
    )
    left_op_args: StringProperty(
        name="Default Operator Arguments",
        description="Arguments used with the default operator",
        maxlen=1024,
    )
    left_op_props: StringProperty(
        name="Default Operator Arguments",
        description="Properties used with the default operator",
        maxlen=1024,
    )

    middle_op: StringProperty(
        name="CTRL Operator",
        description="The Operator called when the ctrl key is pressed",
        maxlen=1024,
    )
    middle_op_args: StringProperty(
        name="Default Operator Arguments",
        description="Arguments used with the default operator",
        maxlen=1024,
    )
    middle_op_props: StringProperty(
        name="Default Operator Arguments",
        description="Properties used with the default operator",
        maxlen=1024,
    )

    right_op: StringProperty(
        name="ALT Operator",
        description="The Operator called when the alt key is pressed",
        maxlen=1024,
    )
    right_op_args: StringProperty(
        name="Default Operator Arguments",
        description="Arguments used with the default operator",
        maxlen=1024,
    )
    right_op_props: StringProperty(
        name="Default Operator Arguments",
        description="Properties used with the default operator",
        maxlen=1024,
    )

    back_op: StringProperty(
        name="SHIFT Operator",
        description="The Operator called when the shift key is pressed",
        maxlen=1024,
    )
    back_op_args: StringProperty(
        name="Default Operator Arguments",
        description="Arguments used with the default operator",
        maxlen=1024,
    )
    back_op_props: StringProperty(
        name="Default Operator Arguments",
        description="Properties used with the default operator",
        maxlen=1024,
    )

    forward_op: StringProperty(
        name="CTRL + SHIFT Operator",
        description="""
                    The Operator called when
                    the shift and ctrl keys are pressed""",
        maxlen=1024,
    )
    forward_op_args: StringProperty(
        name="Default Operator Arguments",
        description="Arguments used with the default operator",
        maxlen=1024,
    )
    forward_op_props: StringProperty(
        name="Default Operator Arguments",
        description="Properties used with the default operator",
        maxlen=1024,
    )

    def attempt(self, context, _op, args, props, db=False):
        use_args = False
        use_props = False

        op_split = _op.split(".")

        if not _op.startswith("atb."):
            operator = getattr(getattr(bpy.ops, op_split[0]), op_split[1])

        if args:
            args_split = args.split(", ")
            if len(args_split) == 3:
                override_context = args_split[0]
                execution_context = str(args_split[1].strip("'"))
                undo = (True if args_split[2] == "True" else False)
                args = (override_context, execution_context, undo)
                use_args = True
            elif len(args_split) == 2:
                execution_context = str(args_split[0].strip("'"))
                undo = (True if args_split[1] == "True" else False)
                args = (execution_context, undo)
                use_args = True
            else:
                self.report({'WARNING'}, "Incorrect Operator Arguments")

        if props:
            prop_dict = ast.literal_eval(props)
            use_props = True

        if db:
            self.report({'INFO'}, "Use Props: " + str(use_props))
            self.report({'INFO'}, "Use Args: " + str(use_args))

        # try:
        if _op.startswith("atb."):
            full = "bpy.ops." + _op + "('INVOKE_DEFAULT', True)"
            if db:
                self.report({'INFO'}, "Custom Operator: " + str(full))
            exec(full)
        elif use_props:
            operator.__call__(*args, **prop_dict)
        elif use_args:
            operator.__call__(*args)
        else:
            operator.__call__()
        # except RuntimeError:
        #     self.report({'INFO'}, "The developer is an idiot")

    def invoke(self, context, event):
        if event.type == 'MIDDLEMOUSE':
            if self.middle_op:
                self.attempt(context, self.middle_op, self.middle_op_args, self.middle_op_props)
            else:
                self.attempt(context, self.left_op, self.left_op_args, self.left_op_props)
        elif event.type == 'RIGHTMOUSE':
            if self.right_op:
                self.attempt(context, self.right_op, self.right_op_args, self.right_op_props)
            else:
                self.attempt(context, self.left_op, self.left_op_args, self.left_op_props)
        elif event.type == 'BUTTON4MOUSE':
            if self.back_op:
                self.attempt(context, self.back_op, self.back_op_args, self.back_op_props)
            else:
                self.attempt(context, self.left_op, self.left_op_args, self.left_op_props)
        elif event.type == 'BUTTON5MOUSE':
            if self.forward_op:
                self.attempt(context, self.forward_op, self.forward_op_args, self.forward_op_props)
            else:
                self.attempt(context, self.left_op, self.left_op_args, self.left_op_props)
        else:
            self.attempt(context, self.left_op, self.left_op_args, self.left_op_props)
            # exec(op)

        return {'FINISHED'}


# TODO: Set this up to send reports, instead of printing
# Enables Fullscreen, hides overlays, headers, gizmos, etc
class ATB_OT_TogglePhotoMode(bpy.types.Operator):
    """Wrapper for context_cycle_enum that updates the 3d viewport"""
    bl_idname = "atb.toggle_photo_mode"
    bl_label = "ATB Toggle Photo Mode"
    bl_description = "Enables Fullscreen, hides overlays, headers, gizmos, etc"

    def invoke(self, context, event):

        if hasattr(context.space_data, 'overlay'):
            if len(context.window.screen.areas) > 1:
                do = False
            else:
                do = True

            context.space_data.overlay.show_overlays = do
            context.space_data.show_gizmo = do

            bpy.ops.screen.screen_full_area('INVOKE_DEFAULT', False, use_hide_panels=True)
            bpy.ops.wm.window_fullscreen_toggle('INVOKE_DEFAULT', False)
        else:
            print("WRONG")

        bpy.context.area.tag_redraw()
        return {'FINISHED'}


# The Select Operator, with Pie
class ATB_OT_EnhancedSelect(bpy.types.Operator):
    """Select operator wrapper with a pie menu for fancy things"""
    bl_idname = "atb.super_select"
    bl_label = "ATB Super Select"
    bl_description = """Fancy Things"""
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
                                    items=[
                                        (
                                            '0',
                                            "First Mode",
                                            "First Mode",
                                            'VERTEXSEL',
                                            1
                                        ),
                                        (
                                            '1',
                                            "Second Mode",
                                            "Second Mode",
                                            'EDITMODE_HLT',
                                            2
                                        ),
                                        (
                                            '2',
                                            "Third Mode",
                                            "Third Mode",
                                            'EDITMODE_HLT',
                                            3
                                        ),
                                        (
                                            '3',
                                            "Fourth Mode",
                                            "Fourth Mode",
                                            'OBJECT_ORIGIN',
                                            4
                                        )],
                                    name="Operator Actions",
                                    default='0',
                                    )

    def execute(self, context):
        # print("Test", self)
        return {'FINISHED'}

    def attempt(self, context, m_loc):
        message = "NOOOOPE"

        try:
            sel_stat = bpy.ops.view3d.select('INVOKE_DEFAULT', True, location=m_loc)
        except Exception as e:
            print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        else:
            self.report({'WARNING'}, str(sel_stat))
            return True

    # def select():
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        op = pie.operator("view3d.select", text="Set Active")
        op.location = self.face_2d_sel
        op.extend = True

        op = pie.operator("view3d.select", text="Deselect")
        op.location = self.m_loc
        op.deselect = True

    def invoke(self, context, event):
        global action
        action = self.action

        m_x = event.mouse_region_x
        m_y = event.mouse_region_y
        m_loc = (m_x, m_y)

        self.m_loc = m_loc
        self.victim = -1
        self.face_2d_sel = (0, 0)

        self.key = event

        def draw_pie(self, context):
            pie = self.layout.menu_pie()
            pie.operator_context = 'INVOKE_DEFAULT'
            global action
            # print(str(action))

            if context.mode == 'OBJECT':

                # LEFT
                pie.operator_context = 'EXEC_DEFAULT'
                op = pie.operator("view3d.select", text="Deselect")
                op.location = m_loc
                op.deselect = True

                # RIGHT
                op = pie.operator("view3d.select", text="Select")
                op.location = m_loc
                op.extend = True

                # BOTTOM
                pie.operator_context = 'INVOKE_DEFAULT'
                op = pie.operator("atb.group_select", text="Select Hierachy")
                op.location = m_loc

                # TOP
                op = pie.operator("atb.obj_display", text="Toggle Display")
                op.location = m_loc
                op.do_toggle = True
                op.mode = 'BOUNDS'

                # TOP LEFT
                pie.separator()

                # TOP RIGHT
                pie.separator()

                # BOTTOM LEFT
                pie.operator_context = 'EXEC_DEFAULT'
                op = pie.operator("object.select_all", text="Deselect All")
                op.action = 'DESELECT'

                # BOTTOM RIGHT
                op = pie.operator("object.select_all", text="Select All")
                op.action = 'SELECT'
            else:
                pie.operator_context = 'EXEC_DEFAULT'
                if action == '0':

                    # LEFT
                    op = pie.operator("mesh.loop_to_region", text="Inner")

                    # RIGHT
                    op = pie.operator("mesh.region_to_loop", text="Outer")

                    # BOTTOM
                    op = pie.operator("view3d.select", text="Select")
                    op.location = m_loc
                    op.extend = True

                    # TOP
                    op = pie.operator("mesh.faces_select_linked_flat", text="Surface")

                    # TOP LEFT
                    op = pie.operator("view3d.select", text="Deselect")
                    op.location = m_loc
                    op.deselect = True

                    # TOP RIGHT
                    op = pie.operator("mesh.loop_multi_select", text="Mult-Loops")

                    # BOTTOM LEFT
                    op = pie.operator("mesh.select_face_by_sides", text="Ngons")
                    op.number = 4
                    op.type = 'GREATER'

                    # BOTTOM RIGHT
                    op = pie.operator("mesh.vert_connect_path", text="Connect Path")

                elif action == '1':

                    # LEFT
                    op = pie.operator("mesh.select_less", text="Less")

                    # RIGHT
                    op = pie.operator("mesh.select_more", text="More")

                    # BOTTOM
                    op = pie.operator("mesh.select_axis", text="Select Axis")

                    # TOP
                    op = pie.operator("mesh.shortest_path_select", text="Tag Between")
                    op.edge_mode = 'BEVEL'

                    # TOP LEFT
                    op = pie.operator("mesh.select_linked", text="Extend To...")
                    op.delimit = {'SEAM'}

                    # TOP RIGHT
                    op = pie.operator("mesh.edges_select_sharp", text="Select Sharp")

                    # BOTTOM LEFT
                    op = pie.operator("mesh.select_prev_item", text="Prev")

                    # BOTTOM RIGHT
                    op = pie.operator("mesh.select_next_item", text="Next")

        wm = context.window_manager
        wm.popup_menu_pie(event, draw_func=draw_pie, title="", icon='NONE')
        return {'FINISHED'}


class ATB_OT_EnhancedTag(bpy.types.Operator):
    """Shortest Path Pick operator wrapper with a pie menu for fancy things"""
    bl_idname = "atb.super_tag"
    bl_label = "ATB Super Tag"
    bl_description = """Fancy Things"""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # print("Test", self)
        return {'FINISHED'}

    def invoke(self, context, event):
        m_x = event.mouse_region_x
        m_y = event.mouse_region_y
        m_loc = (m_x, m_y)

        self.m_loc = m_loc
        self.victim = -1
        self.face_2d_sel = (0, 0)

        mesh = context.object.data
        b_mesh = bmesh.from_edit_mesh(mesh)

        screen_loc = []

        if context.scene.tool_settings.mesh_select_mode[0]:
            for v in b_mesh.verts:

                local_loc = v.co
                obj_loc = context.object.matrix_basis
                world_loc = obj_loc @ local_loc

                loc_2d = bpy_extras.view3d_utils.location_3d_to_region_2d(
                                                                    context.region,
                                                                    context.space_data.region_3d,
                                                                    world_loc,
                                                                    )
                screen_loc.append(loc_2d)

                if (
                        math.isclose(loc_2d[0], m_loc[0], abs_tol=20)
                        and
                        math.isclose(loc_2d[1], m_loc[1], abs_tol=20)
                        ):
                    if context.scene.tool_settings.mesh_select_mode[0]:
                        self.victim = v.index
        elif context.scene.tool_settings.mesh_select_mode[1]:
            for e in b_mesh.edges:

                local_loc = (e.verts[0].co + e.verts[1].co) / 2
                obj_loc = context.object.matrix_basis
                world_loc = obj_loc @ local_loc

                loc_2d = bpy_extras.view3d_utils.location_3d_to_region_2d(
                                                                    context.region,
                                                                    context.space_data.region_3d,
                                                                    world_loc,
                                                                    )
                screen_loc.append(loc_2d)

                if (
                        math.isclose(loc_2d[0], m_loc[0], abs_tol=20)
                        and
                        math.isclose(loc_2d[1], m_loc[1], abs_tol=20)
                        ):
                    self.victim = (e.index + len(b_mesh.verts))

        # else:
        #     for e in b_mesh.edges:

        #         local_loc = (e.verts[0].co + e.verts[1].co) / 2
        #         obj_loc = context.object.matrix_basis
        #         world_loc = obj_loc @ local_loc

        #         loc_2d = bpy_extras.view3d_utils.location_3d_to_region_2d(
        #                                                             context.region,
        #                                                             context.space_data.region_3d,
        #                                                             world_loc,
        #                                                             )
        #         screen_loc.append(loc_2d)

        #         if (
        #                 math.isclose(loc_2d[0], m_loc[0], abs_tol=20)
        #                 and
        #                 math.isclose(loc_2d[1], m_loc[1], abs_tol=20)
        #                 ):
        #             self.victim = e.verts[0].index

        victim = self.victim
        print(str(victim))

        def draw_pie(self, context):

            pie = self.layout.menu_pie()
            pie.operator_context = 'INVOKE_DEFAULT'

            # LEFT
            op = pie.operator("mesh.shortest_path_pick", text="Select")
            op.edge_mode = 'SELECT'
            op.index = victim

            # RIGHT
            op = pie.operator("mesh.shortest_path_pick", text="Tag Seam")
            op.edge_mode = 'SEAM'
            op.index = victim

            # BOTTOM
            op = pie.operator("mesh.shortest_path_pick", text="Tag Sharp")
            op.edge_mode = 'SHARP'
            op.index = victim

            # TOP
            op = pie.operator("mesh.shortest_path_pick", text="Tag Crease")
            op.edge_mode = 'CREASE'
            op.index = victim

            # TOP LEFT
            op = pie.operator("mesh.shortest_path_pick", text="Tag Bevel")
            op.edge_mode = 'BEVEL'
            op.index = victim

            # TOP RIGHT

            # BOTTOM LEFT

            # BOTTOM RIGHT

        wm = context.window_manager
        wm.popup_menu_pie(event, draw_func=draw_pie, title="", icon='NONE')
        return {'FINISHED'}


class ATB_OT_GroupSelect(bpy.types.Operator):
    """Object-Mode Selection That Actually Makes Sense"""
    bl_idname = "atb.group_select"
    bl_label = "ATB Group Select"
    bl_description = "Jesus on a pogo stick"

    location: IntVectorProperty(
        name="Screen Location",
        size=2,
        default=(0, 0),
    )

    def execute(self, context):
        # print("Test", self)
        return {'FINISHED'}

    def invoke(self, context, event):
        stored_selection = context.selected_objects
        _obj_mode = (True if context.mode == 'OBJECT' else False)

        self.family = []

        bpy.ops.view3d.select(
            'EXEC_DEFAULT',
            True,
            extend=False,
            location = self.location)

        self.root = context.active_object

        def recurse_up(self, ob, debug=False):
            """Recursively searches for root parent"""
            if ob.parent:
                if debug:
                    print("Object: " + str(ob))
                    print("Parent: " + str(ob.parent) + "\n")
                recurse_up(self, ob=ob.parent, debug=False)
            else:
                if debug:
                    print("Returning: " + str(ob) + "\n")
                self.root = ob
                self.family.append(ob)

        def recurse_down(self, ob):
            if ob.children:
                for child in ob.children:
                    self.family.append(child)
                    if child.children:
                        recurse_down(self, child)

        active = context.active_object
        if active:
            recurse_up(self, ob=active, debug=False)
            # print("Root: " + str(self.root) + "\n")
            recurse_down(self, self.root)

            for member in self.family:
                member.select_set(state=True)

        return {'FINISHED'}


class ATB_OT_AddToMode(bpy.types.Operator):
    """Wrapper for editmode_toggle that uses overrides to enable mode expansion"""
    bl_idname = "atb.add_to_mode"
    bl_label = "ATB Add Object to Mode"
    bl_description = "Adds objects to current editor mode"

    mouse_loc: IntVectorProperty(
        name="Location",
        description="Cursor location in screen space",
        default=(0, 0),
        size=2
    )

    def invoke(self, context, event):
        m_x = event.mouse_region_x
        m_y = event.mouse_region_y
        m_loc = (m_x, m_y)

        self.mouse_loc = m_loc
        debug = False

        bpy.ops.view3d.select(
            'INVOKE_REGION_WIN',
            False,
            extend=False,
            center=True,
            object=True,
            location=self.mouse_loc
        )

        if debug:
            selected_str = str(context.selected_objects)
            num_selected_str = str(len(context.selected_objects))

            objs_in_mode_str = str(context.objects_in_mode)

            print(num_selected_str + " Objects Selected: " + selected_str + "\n"
                  + "Objects in Mode: " + objs_in_mode_str)

        override = bpy.context.copy()

        for obj in context.selected_objects:
            for ed_obj in context.objects_in_mode:
                if not obj.data == ed_obj.data:
                    override['edit_object'] = None

        bpy.ops.object.editmode_toggle(
            override,
            'INVOKE_REGION_WIN',
            False,
        )

        return {'FINISHED'}


class ATB_OT_MoveCursor(bpy.types.Operator):
    """Wrapper for various 3D Cursor Operators, with context overrides"""
    bl_idname = "atb.move_cursor"
    bl_label = "ATB Move Cursor"
    bl_description = "Does Things to the 3D Cursor"

    mode_items = [
        ("RED", "Red", "", 1),
        ("GREEN", "Green", "", 2),
        ("BLUE", "Blue", "", 3),
        ("YELLOW", "Yellow", "", 4),
    ]

    move_mode: EnumProperty(
        items=mode_items,
        name="Mode",
        description="Cursor manipulation mode",
        default='RED'
    )

    mouse_loc: IntVectorProperty(
        name="Location",
        description="Cursor location in screen space",
        default=(0, 0),
        size=2
    )

    def invoke(self, context, event):
        m_x = event.mouse_region_x
        m_y = event.mouse_region_y
        m_loc = (m_x, m_y)

        self.mouse_loc = m_loc

        mode = self.move_mode

        override = bpy.context.copy()

        if mode == 'RED':
            override['edit_object'] = None
            # override['active_object'] = None

            for obj in context.selected_objects:
                for ed_obj in context.objects_in_mode:
                    if not obj.data == ed_obj.data:
                        override['active_object'] = obj

            bpy.ops.view3d.snap_cursor_to_active(
                override,
                'INVOKE_REGION_WIN',
                False
            )
        elif mode == 'GREEN':
            active_obj_loc = context.active_object.location
            context.scene.cursor.location = mathutils.Vector(active_obj_loc)

        return {'FINISHED'}


class ATB_OT_FastSnap(bpy.types.Operator):
    """Wrapper for various transforms, which toggles snapping and pivot setting"""
    bl_idname = "atb.fast_snap"
    bl_label = "ATB Fast Snap"
    bl_description = "Fast Snapping"

    cursor: BoolProperty(
        name="Move Cursor",
        default=False
    )

    debug: BoolProperty(
        name="Debug Mode",
        default=True
    )

    mode_items = [
        ("INCREMENT", "Increment", "", 1),
        ("VERTEX", "Vertex", "", 2),
        ("EDGE", "Edges", "", 3),
        ("FACE", "Faces", "", 4),
    ]

    snap_mode: EnumProperty(
        items=mode_items,
        name="Mode",
        description="Snap mode",
        default='VERTEX'
    )

    def invoke(self, context, event):

        debug = self.debug
        mode = self.snap_mode
        cursor = self.cursor

        wm = bpy.context.window_manager
        state = wm.snap_state
        state_string = ""

        tool_settings = context.scene.tool_settings

        if mode == "INCREMENT":

            tool_settings.use_snap = False
            tool_settings.snap_elements = {'INCREMENT'}
            tool_settings.snap_target = 'CENTER'

            tool_settings.transform_pivot_point = 'CURSOR'

            bpy.ops.transform.translate(
                'INVOKE_REGION_WIN',
                False,
                cursor_transform=False)

            state.snap_state = 0
            state_string = "No Snapping"

        else:
            elements = {""}
            if mode == "VERTEX":
                elements = {'EDGE_MIDPOINT', 'VERTEX'}
            elif mode == "EDGE":
                elements = {'EDGE_MIDPOINT', 'VERTEX', 'EDGE', 'EDGE_PERPENDICULAR'}
            elif mode == "FACE":
                elements = {'FACE'}

            if state.snap_state == 0:

                tool_settings.use_snap = True
                tool_settings.snap_elements = elements
                tool_settings.snap_target = 'CENTER'

                tool_settings.transform_pivot_point = 'CURSOR'

                bpy.ops.transform.translate(
                    'INVOKE_REGION_WIN',
                    False,
                    cursor_transform=cursor)

                state.snap_state = 1
                state_string = "Step One: Moving Cursor"

            elif state.snap_state == 1:

                tool_settings.use_snap = True
                tool_settings.snap_elements = elements
                tool_settings.snap_target = 'CENTER'

                tool_settings.transform_pivot_point = 'CURSOR'

                bpy.ops.transform.translate(
                    'INVOKE_REGION_WIN',
                    False,
                    cursor_transform=False)

                state.snap_state = 0
                state_string = "Step Two: Moving Object"

        if debug:
            self.report({'INFO'}, state_string)

        return {'FINISHED'}


def operator_value_is_undo(value):
    if value in {None, Ellipsis}:
        return False

    # typical properties or objects
    id_data = getattr(value, "id_data", Ellipsis)

    if id_data is None:
        return False
    elif id_data is Ellipsis:
        # handle mathutils types
        id_data = getattr(getattr(value, "owner", None), "id_data", None)

        if id_data is None:
            return False

    # return True if its a non window ID type
    return (isinstance(id_data, bpy.types.ID) and
            (not isinstance(id_data, (bpy.types.WindowManager,
                                      bpy.types.Screen,
                                      bpy.types.Brush,
                                      ))))


def operator_value_undo_return(value):
    return {'FINISHED'} if operator_value_is_undo(value) else {'CANCELLED'}


def scale_round(x, base=5):
    return base * round(x/base)


# Stolen from someone smarter than me
class ATB_OT_context_modal_mouse(bpy.types.Operator):
    """Adjust arbitrary values with mouse input, but not shitty"""
    bl_idname = "atb.context_modal_mouse"
    bl_label = "ATB Context Modal Mouse"
    bl_options = {'GRAB_CURSOR', 'BLOCKING', 'UNDO', 'INTERNAL'}

    initial_zoom: FloatProperty(
        description="Fuck off",
        default=0.0,
        options={'HIDDEN'}
    )

    zoom_delta: FloatProperty(
        description="FUCK FUCK FUCK",
        default=0.0,
    )

    input_scale: FloatProperty(
        description="Scale the mouse movement by this value before applying the delta",
        default=0.1,
    )

    snap: BoolProperty(
        default=False
    )

    initial_x: IntProperty(options={'HIDDEN'})

    def execute(self, context):
        space_data = context.space_data
        space_data.lens = self.zoom_delta

    def modal(self, context, event):
        inital_zoom = self.initial_zoom

        lens = context.space_data.lens

        context.area.header_text_set("Zoom: %.2fmm" % lens)

        if event.type == 'MOUSEMOVE':
            mouse_x = event.mouse_x - self.initial_x
            threshold = 5
            # print(str(mouse_x))

            if event.shift:
                m_input = mouse_x * 0.01
            else:
                m_input = mouse_x * 0.1

            if event.ctrl:
                if event.shift:
                    threshold = 1
                if abs(mouse_x) > threshold:
                    self.zoom_delta = scale_round(m_input + inital_zoom, threshold)
                    self.execute(context)
            else:
                self.zoom_delta = m_input + inital_zoom
                self.execute(context)

            context.area.header_text_set("Zoom: %.2fmm" % lens)

        elif event.type == 'LEFTMOUSE':
            self.execute(context)
            context.area.header_text_set(None)
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.area.header_text_set(None)
            context.space_data.lens = self.initial_zoom
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.initial_x = event.mouse_x
        self.initial_zoom = context.space_data.lens

        self.zoom_delta = 0

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

# TODO: There are still a few edge cases for this one that I need to solve
class ATB_OT_drop_tool(bpy.types.Operator):
    """Changes the active tool to a contextually-appropriate 'default tool'"""
    bl_idname = "atb.drop_tool"
    bl_label = "ATB Drop Tool"
    # bl_options = {'GRAB_CURSOR', 'BLOCKING', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        debug = False
        mode = context.mode

        base_modes = ["OBJECT", "EDIT_MESH", "EDIT_CURVE", "EDIT_SURFACE", "EDIT_METABALL", "EDIT_GPENCIL", "EDIT_LATTICE"]

        other_modes = [
                        "EDIT_TEXT",
                        "SCULPT",
                        "SCULPT_GPENCIL",
                        "PAINT_VERTEX",
                        "PAINT_WEIGHT",
                        "PAINT_TEXTURE",
                        "PAINT_GPENCIL",
                        "VERTEX_GPENCIL",
                        "WEIGHT_GPENCIL"
                        ]

        if debug:
            print(str(mode))

        if mode in base_modes:
            bpy.ops.wm.tool_set_by_id(
                'INVOKE_DEFAULT',
                False,
                name="builtin.select_box"
            )
        elif mode in other_modes:

            if mode == 'EDIT_TEXT':
                bpy.ops.object.editmode_toggle()
            elif mode == 'SCULPT':
                bpy.ops.sculpt.sculptmode_toggle()
            else:
                self.report({'INFO'}, "Unsupported Mode")
        else:
            self.report({'WARNING'}, "Something Broke")

        return{'FINISHED'}


class ATB_OT_Set_Custom_Popover(bpy.types.Operator):
    """Let's the user set which panel will be displayed by the associated popover button"""
    bl_idname = "atb.set_custom_pop"
    bl_label = "ATB Set Custom Popover"
    bl_options = {'BLOCKING', 'UNDO', 'INTERNAL', 'REGISTER'}

    panel_name: StringProperty(
        name="Panel",
        description="The panel to display",
        default="BruceWayne",
    )

    button: IntProperty(
        name="Button",
        description="Which button the panel is linked to",
        default=1,
        min=1,
        max=3,
    )

    def execute(self, context):
        button = self.button

        is_valid = False

        for panel in bpy.types.Panel.__subclasses__():
            if self.panel_name == panel.__name__:
                is_valid = True
                break

        if is_valid:
            bacon = "bacon"
            # continue
        else:
            self.report({'WARNING'}, self.panel_name + " is bullshit")
            return {'CANCELLED'}

        if button == 1:
            context.workspace.customPops.popover_1 = self.panel_name
        elif button == 2:
            context.workspace.customPops.popover_2 = self.panel_name
        elif button == 3:
            context.workspace.customPops.popover_3 = self.panel_name

        return {'FINISHED'}

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


class ATB_OT_Clear_Custom_Popover(bpy.types.Operator):
    """Let's the user clear the panel of the associated popover button"""
    bl_idname = "atb.clear_custom_pop"
    bl_label = "ATB Clear Custom Popover"
    bl_options = {'BLOCKING', 'UNDO', 'INTERNAL', 'REGISTER'}

    button: IntProperty(
        name="Button",
        description="Which button the panel is linked to",
        default=1,
        min=1,
        max=3
    )

    def execute(self, context):
        button = self.button

        if button == 1:
            context.workspace.customPops.popover_1 = "BATMAN"
        elif button == 2:
            context.workspace.customPops.popover_2 = "BATMAN"
        elif button == 3:
            context.workspace.customPops.popover_3 = "BATMAN"

        return {'FINISHED'}

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


class ATB_OT_Frame_Object(bpy.types.Operator):
    """Forces the Frame Selected operator to frame the object in edit mode"""
    bl_idname = "atb.frame_object"
    bl_label = "ATB Frame Object"
    bl_options = {'BLOCKING', 'UNDO', 'REGISTER'}

    def invoke(self, context, event):

        override = bpy.context.copy()
        override['edit_object'] = None

        bpy.ops.view3d.view_selected(
                override,
                'INVOKE_DEFAULT',
                False,
        )

        return {'FINISHED'}

# TODO: Add a poll function that'll keep me from calling it where I shouldn't
class ATB_OT_Select_Object(bpy.types.Operator):
    """A UI-Only Operator for setting the active object selection"""
    bl_idname = "atb.object_select"
    bl_label = "ATB Frame Object"
    bl_options = {'BLOCKING', 'UNDO', 'REGISTER'}

    target_object: StringProperty(
                        name="Target Object",
                        description="The object to select.",
    )

    def invoke(self, context, event):

        for obj in bpy.context.view_layer.objects.selected:
            obj.select_set(False)

        obj = bpy.data.objects.get(self.target_object)

        obj.select_set(True)

        bpy.context.view_layer.objects.active = obj

        return {'FINISHED'}


def nuke(cls, context):
    return False

class ATB_OT_Nuke_Panel(bpy.types.Operator):
    """A UI-Only Operator for setting the active object selection"""
    bl_idname = "atb.nuke_panel"
    bl_label = "ATB Nuke Panel"

    show: BoolProperty(
        name="Show Panel",
        default=False
    )

    def invoke(self, context, event):

        panel = bpy.types.VIEW3D_PT_meta_panel

        if event.ctrl:
            panel.poll = panel.poll
        else:
            panel.poll = types.MethodType(nuke, panel)

        return {'FINISHED'}


class ATB_OT_Set_Object_Display(bpy.types.Operator):
    """A Macro that selects an object, sets its display mode, then deselects it"""
    bl_idname = "atb.obj_display"
    bl_label = "ATB Set Object Display Mode"
    bl_description = "Takes a BoolVector and an Enum, makes them play nice"

    location: IntVectorProperty(
        name="Show Panel",
        size=2,
        default=(0, 0),
    )

    mode_items = [
        ("BOUNDS", "Bounds", "", 1),
        ("WIRE", "Wire", "", 2),
        ("SOLID", "Solid", "", 3),
        ("TEXTURED", "Textured", "", 4),
    ]

    mode: EnumProperty(
        name="Display Mode",
        items=mode_items,
        description="The display mode to set",
        default='BOUNDS',
    )

    do_toggle: BoolProperty(
        name="Toggle",
        default= False,
    )

    def invoke(self, context, event):

        stored_selection = context.selected_objects

        bpy.ops.view3d.select('EXEC_DEFAULT', False, location=self.location)

        obj = context.active_object

        if self.do_toggle:
            if not obj.display_type == 'TEXTURED':
                obj.display_type = 'TEXTURED'
            else:
                obj.display_type = self.mode
        else:
            obj.display_type = self.mode

        obj.select_set(False)

        for thing in stored_selection:
            thing.select_set(True)

        return {'FINISHED'}
