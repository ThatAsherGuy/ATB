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
from bpy.types import (
    # Panel,
    Menu
)

def save_pie(self, context):
    pie = self.layout.menu_pie()
    pie.operator_context = 'INVOKE_DEFAULT'

    # LEFT
    pie.operator(
        "wm.save_as_mainfile",
        text="Save As...",
    )

    # RIGHT
    pie.operator(
        "wm.save_mainfile",
        text="Save",
    )

    # BOTTOM
    pie.operator(
        "atb.save_incremental",
        text="Save Incremental",
    )

    # TOP
    pie.operator(
        "wm.open_mainfile",
        text="Open...",
    )

    # TOP LEFT
    pie.separator()

    # TOP RIGHT
    pie.separator()

    # BOTTOM LEFT
    pie.separator()

    # BOTTOM RIGHT
    pie.separator()

class ATB_OT_SavePie(bpy.types.Operator):
    bl_idname = "atb.save_pie"
    bl_label = "ATB Save Pie"
    bl_description = ("A Pie for quick-saving, incremental saving, and other things.")
    bl_options = {'REGISTER'}

    mode_items = [
        ("BRUSH", "Brush", ""),
        ("STROKE", "Stroke", ""),
        ("PLANE", "Plane", ""),
        ("SYMM", "Symmetry", ""),
    ]

    mode: bpy.props.EnumProperty(
        items=mode_items,
        name="Mode",
        description="The invocation mode, used to select which sculpt functions are displayed",
        default='STROKE'
    )

    def invoke(self, context, event):
        self.loc = (event.mouse_region_x, event.mouse_region_y)

        wm = context.window_manager
        wm.popup_menu_pie(event, draw_func=save_pie, title="", icon='NONE')
        return{'FINISHED'}


class ATB_OT_MetaPie(bpy.types.Operator):
    bl_idname = "atb.meta_pie"
    bl_label = "ATB Meta Pie"
    bl_description = ("Launches the mode-appropriate ATB Pie.")
    bl_options = {'REGISTER'}

    mode_items = [
        ("BRUSH", "Brush", ""),
        ("STROKE", "Stroke", ""),
        ("PLANE", "Plane", ""),
        ("SYMM", "Symmetry", ""),
    ]

    mode: bpy.props.EnumProperty(
        items=mode_items,
        name="Mode",
        description="The invocation mode, used to select which sculpt functions are displayed",
        default='STROKE'
    )

    def invoke(self, context, event):
        self.loc = (event.mouse_region_x, event.mouse_region_y)

        if context.mode == 'OBJECT':
            print("OBJECT MODE")
            bpy.ops.atb.super_select('INVOKE_DEFAULT', False)
            return {'FINISHED'}


        elif context.mode == 'SCULPT':
            print("SCULPT MODE")
            bpy.ops.atb.sculpt_pie('INVOKE_DEFAULT', False)
            return {'FINISHED'}

        elif context.mode == 'EDIT_MESH':
            print("MESH EDIT")
            bpy.ops.atb.super_select('INVOKE_DEFAULT', False)
            return {'FINISHED'}

        elif context.mode == 'EDIT_CURVE':
            print("CURVE EDIT")

        elif context.mode == 'EDIT_SURFACE':
            print("SURFACE EDIT")

        elif context.mode == 'EDIT_TEXT':
            print("TEXT EDIT")

        elif context.mode == 'EDIT_ARMATURE':
            print("ARMATURE EDIT")

        elif context.mode == 'EDIT_METABALL':
            print("METABALL EDIT")

        elif context.mode == 'EDIT_LATTICE':
            print("LATTICE EDIT")


        if event.is_tablet:
            self.tablet = True
        else:
            self.tablet = False

        return {'FINISHED'}


class VIEW3D_MT_PIE_orbit_lock(Menu):
    bl_label = "Context Pie"

    def draw(self, context):
        layout = self.layout
        # view = context.space_data
        pie = layout.menu_pie()
        if bpy.context.mode == 'EDIT_MESH':
            if context.scene.cp_mode_enum == '0':
                # LEFT
                pie.operator(
                    "mesh.vertices_smooth"
                )
                # RIGHT
                pie.operator(
                    "mesh.dissolve_verts"
                )
                # BOTTOM
                pie.operator(
                    "transform.vert_slide"
                )

                # TOP
                pie.operator(
                    "mesh.vert_connect_path"
                )

                # TOP LEFT
                # TOP RIGHT
                # BOTTOM LEFT
                # BOTTOM RIGHT

            elif context.scene.cp_mode_enum == '1':

                # LEFT
                context_op = pie.operator(
                    "atb.context_op",
                    text="Clear Seam / Sharp / Bevel / Crease"
                )

                context_op.def_op = "mesh.mark_seam"
                context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                context_op.def_op_props = (
                                            "{"
                                            "'clear': "
                                            "True,"
                                            "}"
                                        )

                context_op.ctrl_op = "mesh.mark_sharp"
                context_op.ctrl_op_args = "'EXEC_DEFAULT', True,"
                context_op.ctrl_op_props = (
                                            "{"
                                            "'clear': "
                                            "True,"
                                            "}"
                                        )

                context_op.alt_op = "transform.edge_bevelweight"
                context_op.alt_op_args = "'EXEC_DEFAULT', True,"
                context_op.alt_op_props = (
                                            "{"
                                            "'value': "
                                            "-1,"
                                            "}"
                                        )

                context_op.shift_op = "transform.edge_crease"
                context_op.shift_op_args = "'EXEC_DEFAULT', True,"
                context_op.shift_op_props = (
                                            "{"
                                            "'value': "
                                            "-1,"
                                            "}"
                                        )

                # RIGHT
                context_op = pie.operator(
                    "atb.context_op",
                    text="Mark Seam / Sharp / Bevel / Crease"
                )

                context_op.def_op = "mesh.mark_seam"
                context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                context_op.def_op_props = (
                                            "{"
                                            "'clear': "
                                            "False,"
                                            "}"
                                        )

                context_op.ctrl_op = "mesh.mark_sharp"
                context_op.ctrl_op_args = "'EXEC_DEFAULT', True,"
                context_op.ctrl_op_props = (
                                            "{"
                                            "'clear': "
                                            "False,"
                                            "}"
                                        )

                context_op.alt_op = "transform.edge_bevelweight"
                context_op.alt_op_args = "'INVOKE_DEFAULT', True,"
                context_op.alt_op_props = (
                                            "{"
                                            "'value': "
                                            "1,"
                                            "}"
                                        )

                context_op.shift_op = "transform.edge_crease"
                context_op.shift_op_args = "'INVOKE_DEFAULT', True,"
                context_op.shift_op_props = (
                                            "{"
                                            "'value': "
                                            "0,"
                                            "}"
                                        )

                # BOTTOM
                pie.operator(
                    "mesh.bevel"
                )

                # TOP
                pie.operator(
                    "mesh.subdivide"
                )

                # TOP LEFT
                pie.operator(
                    "mesh.bridge_edge_loops"
                )

                # TOP RIGHT
                # BOTTOM LEFT
                # BOTTOM RIGHT

            elif context.scene.cp_mode_enum == '2':
                # LEFT
                context_op = pie.operator(
                    "atb.context_op",
                    text="Mark Seam / Sharp / Bevel / Crease"
                )

                context_op.def_op = "mesh.mark_seam"
                context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                context_op.def_op_props = (
                                            "{"
                                            "'clear': "
                                            "False,"
                                            "}"
                                        )

                context_op.ctrl_op = "mesh.mark_sharp"
                context_op.ctrl_op_args = "'EXEC_DEFAULT', True,"
                context_op.ctrl_op_props = (
                                            "{"
                                            "'clear': "
                                            "False,"
                                            "}"
                                        )

                context_op.alt_op = "transform.edge_bevelweight"
                context_op.alt_op_args = "'INVOKE_DEFAULT', True,"
                context_op.alt_op_props = (
                                            "{"
                                            "'value': "
                                            "1,"
                                            "}"
                                        )

                context_op.shift_op = "transform.edge_crease"
                context_op.shift_op_args = "'INVOKE_DEFAULT', True,"
                context_op.shift_op_props = (
                                            "{"
                                            "'value': "
                                            "0,"
                                            "}"
                                        )

                # RIGHT
                context_op = pie.operator(
                    "atb.context_op",
                    text="Clear Seam / Sharp / Bevel / Crease"
                )

                context_op.def_op = "mesh.mark_seam"
                context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                context_op.def_op_props = (
                                            "{"
                                            "'clear': "
                                            "True,"
                                            "}"
                                        )

                context_op.ctrl_op = "mesh.mark_sharp"
                context_op.ctrl_op_args = "'EXEC_DEFAULT', True,"
                context_op.ctrl_op_props = (
                                            "{"
                                            "'clear': "
                                            "True,"
                                            "}"
                                        )

                context_op.alt_op = "transform.edge_bevelweight"
                context_op.alt_op_args = "'EXEC_DEFAULT', True,"
                context_op.alt_op_props = (
                                            "{"
                                            "'value': "
                                            "-1,"
                                            "}"
                                        )

                context_op.shift_op = "transform.edge_crease"
                context_op.shift_op_args = "'EXEC_DEFAULT', True,"
                context_op.shift_op_props = (
                                            "{"
                                            "'value': "
                                            "-1,"
                                            "}"
                                        )

                # BOTTOM
                context_op = pie.operator(
                    "atb.context_op",
                    text="Cursor to Active / Selection"
                )

                context_op.def_op = "mesh.view3d.snap_cursor_to_active"
                context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                context_op.def_op_props = ""

                context_op.ctrl_op = "view3d.snap_cursor_to_selected"
                context_op.ctrl_op_args = "'EXEC_DEFAULT', True,"
                context_op.ctrl_op_props = ""

                # TOP
                context_op = pie.operator(
                    "atb.context_op",
                    text="Merge to: Center | (c) Last | (a) Cursor | (s) First"
                )

                context_op.def_op = "mesh.merge"
                context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                context_op.def_op_props = (
                                            "{"
                                            "'type': "
                                            "'CENTER',"
                                            "}"
                                        )

                context_op.ctrl_op = "mesh.merge"
                context_op.ctrl_op_args = "'EXEC_DEFAULT', True,"
                context_op.ctrl_op_props = (
                                            "{"
                                            "'type': "
                                            "'LAST',"
                                            "}"
                                        )

                context_op.alt_op = "mesh.merge"
                context_op.alt_op_args = "'EXEC_DEFAULT', True,"
                context_op.alt_op_props = (
                                            "{"
                                            "'type': "
                                            "'CURSOR',"
                                            "}"
                                        )

                context_op.shift_op = "mesh.merge"
                context_op.shift_op_args = "'EXEC_DEFAULT', True,"
                context_op.shift_op_props = (
                                            "{"
                                            "'type': "
                                            "'FIRST',"
                                            "}"
                                        )

                # TOP LEFT
                pie.operator(
                    "mesh.loop_multi_select"
                )

                # TOP RIGHT
                context_op = pie.operator(
                    "atb.context_op",
                    text="Select Surface | Region | Inner | Outer"
                )

                context_op.def_op = "mesh.faces_select_linked_flat"
                context_op.def_op_args = "'INVOKE_REGION_WIN', False,"
                context_op.def_op_props = (
                                            "{"
                                            "'sharpness': "
                                            "0.26,"
                                            "}"
                                        )

                context_op.ctrl_op = "mesh.select_linked"
                context_op.ctrl_op_args = "'INVOKE_DEFAULT', True,"
                context_op.ctrl_op_props = ""

                context_op.alt_op = "mesh.loop_to_region"
                context_op.alt_op_args = "'EXEC_DEFAULT', True,"
                context_op.alt_op_props = ""

                context_op.shift_op = "mesh.region_to_loop"
                context_op.shift_op_args = "'EXEC_DEFAULT', True,"
                context_op.shift_op_props = ""

                # BOTTOM LEFT
                context_op = pie.operator(
                    "atb.context_op",
                    text="Select More / Less / Next / Prev"
                )

                context_op.def_op = "mesh.select_more"
                context_op.def_op_args = "'EXEC_DEFAULT', True,"
                context_op.def_op_props = ""

                context_op.ctrl_op = "mesh.select_less"
                context_op.ctrl_op_args = "'EXEC_DEFAULT', True,"
                context_op.ctrl_op_props = ""

                context_op.alt_op = "mesh.select_next_item"
                context_op.alt_op_args = "'EXEC_DEFAULT', True,"
                context_op.alt_op_props = ""

                context_op.shift_op = "mesh.select_prev_item"
                context_op.shift_op_args = "'EXEC_DEFAULT', True,"
                context_op.shift_op_props = ""

                # BOTTOM RIGHT
                context_op = pie.operator(
                    "atb.context_op",
                    text="Snap to Active / Cursor"
                )

                context_op.def_op = "view3d.snap_selected_to_active"
                context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                context_op.def_op_props = ""

                context_op.ctrl_op = "view3d.snap_selected_to_cursor"
                context_op.ctrl_op_args = "'INVOKE_DEFAULT', True,"
                context_op.ctrl_op_props = (
                                                    "{"
                                                    "'use_offset': "
                                                    "'False',"
                                                    "}"
                                            )

                context_op.alt_op = "view3d.snap_selected_to_cursor"
                context_op.alt_op_args = "'INVOKE_DEFAULT', True,"
                context_op.alt_op_props = (
                                                    "{"
                                                    "'use_offset': "
                                                    "'True',"
                                                    "}"
                                            )

            elif context.scene.cp_mode_enum == '3':

                # LEFT
                context_op = pie.operator(
                    "atb.context_op",
                    text="Bevel / Inset"
                )

                context_op.def_op = "mesh.bevel"
                context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                context_op.def_op_props = ""

                context_op.ctrl_op = "mesh.inset"
                context_op.ctrl_op_args = "'INVOKE_DEFAULT', True,"
                context_op.ctrl_op_props = ""

                # RIGHT
                context_op = pie.operator(
                    "atb.context_op",
                    text="Bridge / Merge Edge Loops"
                )

                context_op.def_op = "mesh.bridge_edge_loops"
                context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                context_op.def_op_props = (
                                                    "{"
                                                    "'use_merge': "
                                                    "False,"
                                                    "}"
                )

                context_op.ctrl_op = "mesh.bridge_edge_loops"
                context_op.ctrl_op_args = "'INVOKE_DEFAULT', True,"
                context_op.ctrl_op_props = (
                                                    "{"
                                                    "'use_merge': "
                                                    "True,"
                                                    "}"
                                            )

                # BOTTOM
                context_op = pie.operator(
                    "atb.context_op",
                    text="Transform Selection / Cursor"
                )

                context_op.def_op = "transform.translate"
                context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                context_op.def_op_props = (
                                                    "{"
                                                    "'cursor_transform': "
                                                    "False,"
                                                    "}"
                )

                context_op.ctrl_op = "transform.translate"
                context_op.ctrl_op_args = "'INVOKE_DEFAULT', True,"
                context_op.ctrl_op_props = (
                                                    "{"
                                                    "'cursor_transform': "
                                                    "True,"
                                                    "}"
                                            )

                # TOP
                context_op = pie.operator(
                    "atb.context_op",
                    text="Cycle Pie"
                )

                context_op.def_op = "wm.context_cycle_int"
                context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                context_op.def_op_props = (
                                            "{"
                                            "'wrap': True, "
                                            "'reverse': False, "
                                            "}"
                                            )

                context_op.ctrl_op = "wm.context_cycle_int"
                context_op.ctrl_op_args = "'INVOKE_DEFAULT', True,"
                context_op.ctrl_op_props = (
                                            "{"
                                            "'wrap': True,"
                                            "'reverse': True"
                                            "}"
                                            )

                # TOP LEFT
                context_op = pie.operator(
                    "atb.context_op",
                    text="Extrude and Push / Scale"
                )
                context_op.def_op = "bpy.ops.view3d.edit_mesh_extrude_move_normal('INVOKE_DEFAULT', True)"
                context_op.ctrl_op = "bpy.ops.mesh.extrude_region_shrink_fatten('INVOKE_DEFAULT', True)"

                context_op.def_op = "view3d.edit_mesh_extrude_move_normal"
                context_op.def_op_args = "'INVOKE_DEFAULT', True,"
                context_op.def_op_props = ""

                context_op.ctrl_op = "mesh.extrude_region_shrink_fatten"
                context_op.ctrl_op_args = "'INVOKE_DEFAULT', True,"
                context_op.ctrl_op_props = ""

                # TOP RIGHT
                # BOTTOM LEFT
                # BOTTOM RIGHT
        if bpy.context.mode == 'OBJECT':
            # LEFT
            context_op = pie.operator(
                "atb.context_op",
                text="Cursor to Active / Selection"
            )
            context_op.def_op = """view3d.snap_cursor_to_active"""
            context_op.def_op_args = "'INVOKE_DEFAULT', True,"
            context_op.def_op_props = ""

            context_op.ctrl_op = """view3d.snap_cursor_to_selected"""
            context_op.ctrl_op_args = "'INVOKE_DEFAULT', True,"
            context_op.ctrl_op_props = ""

            # RIGHT
            context_op = pie.operator(
                "atb.context_op",
                text="Snap to Active / Cursor"
            )

            context_op.def_op = "view3d.snap_selected_to_cursor"
            context_op.def_op_args = "'INVOKE_DEFAULT', True,"
            context_op.def_op_props = ""

            context_op.ctrl_op = "view3d.snap_selected_to_active"
            context_op.ctrl_op_args = "'INVOKE_DEFAULT', True,"
            context_op.ctrl_op_props = ""

            context_op.alt_op = "view3d.snap_selected_to_cursor)"
            context_op.alt_op_args = "'INVOKE_DEFAULT', True,"
            context_op.alt_op_props = (
                                                "{"
                                                "'use_offset': "
                                                "'True',"
                                                "}"
                                        )

            # BOTTOM
            context_op = pie.operator(
                "atb.context_op",
                text="Set Origin to Cursor / Geometry"
            )

            context_op.def_op = "object.origin_set"
            context_op.def_op_args = "'INVOKE_DEFAULT', True,"
            context_op.def_op_props = (
                                                "{"
                                                "'type': "
                                                "'ORIGIN_CURSOR',"
                                                "'center': "
                                                "'MEDIAN',"
                                                "}"
                                        )

            context_op.ctrl_op = "object.origin_set"
            context_op.ctrl_op_args = "'INVOKE_DEFAULT', True,"
            context_op.ctrl_op_props = (
                                                "{"
                                                "'type': "
                                                "'ORIGIN_GEOMETRY',"
                                                "'center': "
                                                "'MEDIAN',"
                                                "}"
                                        )

            context_op.alt_op = "object.origin_set"
            context_op.alt_op_args = "'INVOKE_DEFAULT', True,"
            context_op.alt_op_props = (
                                                "{"
                                                "'type': "
                                                "'GEOMETRY_ORIGIN',"
                                                "'center': "
                                                "'MEDIAN',"
                                                "}"
                                        )


class VIEW3D_MT_PIE_expand_mode(Menu):
    bl_label = "ATB Mode Pie"

    def draw(self, context):
        layout = self.layout
        # view = context.space_data
        pie = layout.menu_pie()

        pie.operator(
            "atb.add_to_mode"
        )


class VIEW3D_MT_PIE_quick_snap(Menu):
    bl_label = "ATB Snapping Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        tool_settings = context.scene.tool_settings

        # pie.prop(tool_settings, 'snap_elements')

        # LEFT
        op = pie.operator("wm.context_set_value", text="Snap Cycle")
        op.data_path = "scene.tool_settings.snap_elements"

        if not tool_settings.snap_elements == {'INCREMENT'}:
            if tool_settings.snap_elements == {'VERTEX'}:
                op.value = "{'EDGE'}"
            elif tool_settings.snap_elements == {'EDGE'}:
                op.value = "{'FACE'}"
            elif tool_settings.snap_elements == {'FACE'}:
                op.value = "{'VOLUME'}"
            elif tool_settings.snap_elements == {'VOLUME'}:
                op.value = "{'INCREMENT'}"
            else:
                print("FALLBACK")
                op.value = "{'INCREMENT'}"
        else:
            op.value = "{'VERTEX'}"

        # RIGHT
        op = pie.operator("wm.context_set_value", text="Pivot Cycle")
        op.data_path = "scene.tool_settings.transform_pivot_point"

        if not tool_settings.transform_pivot_point == 'BOUNDING_BOX_CENTER':
            if tool_settings.transform_pivot_point == 'CURSOR':
                op.value = "'INDIVIDUAL_ORIGINS'"
            elif tool_settings.transform_pivot_point == 'INDIVIDUAL_ORIGINS':
                op.value = "'MEDIAN_POINT'"
            elif tool_settings.transform_pivot_point == 'MEDIAN_POINT':
                op.value = "'ACTIVE_ELEMENT'"
            elif tool_settings.transform_pivot_point == 'ACTIVE_ELEMENT':
                op.value = "'BOUNDING_BOX_CENTER'"
        else:
            op.value = "'CURSOR'"

        # BOTTOM
        op = pie.operator("wm.context_set_value", text="Cursor Pivot")
        op.data_path = "scene.tool_settings.transform_pivot_point"

        if not tool_settings.transform_pivot_point == 'CURSOR':
            op.value = "'CURSOR'"
        else:
            op.value = "'BOUNDING_BOX_CENTER'"

        # TOP
        op = pie.operator("wm.context_set_value", text="Grid Snap")
        op.data_path = "scene.tool_settings.snap_elements"

        if not tool_settings.snap_elements == {'INCREMENT'}:
            op.value = "{'INCREMENT'}"
        else:
            op.value = "{'VERTEX'}"


class VIEW3D_MT_PIE_quick_orientation(Menu):
    bl_label = "ATB Orientation Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        scene = context.scene

        orient_slot = scene.transform_orientation_slots[0]
        # orientation = orient_slot.custom_orientation

        # LEFT
        op = pie.operator("wm.context_set_value", text="Global/Local")
        op.data_path = "scene.transform_orientation_slots[0].type"

        if not orient_slot.type == 'GLOBAL':
            op.value = "'GLOBAL'"
        else:
            op.value = "'LOCAL'"

        # RIGHT
        op = pie.operator("wm.context_set_value", text="Cursor/Normal")
        op.data_path = "scene.transform_orientation_slots[0].type"

        if not orient_slot.type == 'CURSOR':
            op.value = "'CURSOR'"
        else:
            op.value = "'NORMAL'"

        # BOTTOM
        op = pie.operator("wm.context_set_value", text="View/Gimbal")
        op.data_path = "scene.transform_orientation_slots[0].type"

        if not orient_slot.type == 'VIEW':
            op.value = "'VIEW'"
        else:
            op.value = "'GIMBAL'"

        # TOP
        op = pie.operator("transform.create_orientation", text="Create")
        op.use = True
        # pie.prop(tool_settings, 'snap_elements', expand=False)
