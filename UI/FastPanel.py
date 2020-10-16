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
    Panel,
)


class VIEW3D_PT_view3d_fast_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    # bl_category = "ATB"
    bl_label = "Fast Panel"
    bl_options = {'DRAW_BOX'}

    @classmethod
    def get_shading(cls, context):
        view = context.space_data
        if view.type == 'VIEW_3D':
            return view.shading
        else:
            return context.scene.display.shading

    def draw(self, context):

        # Aliased Stuff
        scene = context.scene
        units = scene.unit_settings
        overlay = context.space_data.overlay
        view = context.space_data
        shading = VIEW3D_PT_view3d_fast_panel.get_shading(context)
        active_obj = context.active_object

        # use_shrink = False
        # base_scale_y = 0.85

        # Fast Panel Property Group
        wm = bpy.context.window_manager
        fp = wm.fp_props

        if context.active_object:
            if context.active_object.type == 'MESH':
                active_mat = context.active_object.active_material
            # active_mesh = context.active_object.data

        layout = self.layout

        if fp.layout_bool:
            layout.ui_units_x = 60
            root = layout.grid_flow(columns=4, even_columns=True, align=False)
        else:
            root = layout.grid_flow(columns=1, even_columns=True, align=False)
            layout.ui_units_x = 12

        root.scale_y = 1

        # ignoring Blender's variable naming conventions for UI layouts
        # because it's bad and you should feel bad for using it
        col_1 = root.column(align=True)
        tab_row = col_1.row(align=False)
        tab_row.alignment = 'EXPAND'

        tb_l = tab_row.row(align=True)
        tb_l.alignment = 'LEFT'
        tb_l.operator("act.toggle_photo_mode", text="", icon='FULLSCREEN_ENTER')

        tb_r = tab_row.row(align=True)
        tb_r.alignment = 'RIGHT'
        # tab_row.prop(fp, "layout_bool", text="", icon="KEYFRAME_HLT")
        tb_r.prop(fp, "fast_panel_tabs", expand=True, icon_only=True)

        # Measures Row
        if fp.fast_panel_tabs == 'MEASURES':
            but_box = col_1.column()

            but_box_inner_col = but_box.column(align=True)
            but_row = but_box_inner_col.row(align=True)

            if (context.active_object and context.active_object.type == 'MESH'):

                r_row = but_box_inner_col.row(align=True)
                r_col = r_row.column(align=True)
                row = r_col.row(align=True)

                row.prop_enum(
                    context.object,
                    "display_type",
                    'BOUNDS',
                    text="Box",
                )
                row.prop_enum(
                    context.object,
                    "display_type",
                    'WIRE',
                    text="Wire",
                )
                row.prop_enum(
                    context.object,
                    "display_type",
                    'TEXTURED',
                    text="Full",
                )
                row = r_col.row(align=True)

                if context.active_object:

                    if context.active_object.type == 'MESH':
                        active_mesh = context.active_object.data
                        row.prop(
                            active_mesh,
                            "use_auto_smooth",
                            text="Auto Smooth",
                            # icon='MOD_NORMALEDIT',
                            toggle=True
                        )
                        row.prop(
                            active_mesh,
                            "auto_smooth_angle",
                            text="",
                        )

                col = r_row.column(align=True)
                row = col.row(align=True)

                row.prop(
                    overlay,
                    "show_extra_edge_length",
                    text="",
                    toggle=True,
                    icon='EDGESEL'
                )
                row.prop(
                    overlay,
                    "show_extra_edge_angle",
                    text="",
                    toggle=True,
                    icon='DRIVER_ROTATIONAL_DIFFERENCE'
                )
                row.prop(
                    overlay,
                    "show_extra_face_area",
                    text="",
                    toggle=True,
                    icon='CON_SIZELIMIT'
                )
                row.prop(
                    overlay,
                    "show_extra_face_angle",
                    text="",
                    toggle=True,
                    icon='MOD_SOLIDIFY'
                )
                row.prop(
                    context.object,
                    "show_wire",
                    text="",
                    icon='MOD_WIREFRAME',
                    toggle=True
                )

                row = col.row(align=True)

                if context.active_object:
                    if context.mode == 'OBJECT' and context.active_object.type == 'MESH':
                        row.operator(
                            "object.shade_smooth",
                            text="Set Smooth",
                            # icon='NORMALS_VERTEX_FACE'
                        )
                    elif context.mode == 'OBJECT' and context.active_object.type == 'CURVE':
                        row.operator(
                            "curve.shade_smooth"
                        )
                    elif context.mode == 'EDIT_MESH':
                        row.operator(
                            "mesh.faces_shade_smooth",
                        )

            statvis = context.scene.tool_settings.statvis
            statvis_col = but_box.column(align=True)
            subrow = statvis_col.row(align=True)
            subrow.prop(
                    overlay,
                    "show_statvis",
                    text="Mesh Viz",
                    toggle=True
            )
            subrow.prop(statvis, "type", text="")

            subrow = statvis_col.row(align=True)
            subrow.active = (True if overlay.show_statvis else False)

            if statvis.type == 'OVERHANG':
                subrow.prop(statvis, "overhang_min", text="Min")
                subrow.prop(statvis, "overhang_max", text="Max")
                subrow.prop(statvis, "overhang_axis", text="")
            if statvis.type == 'THICKNESS':
                subrow.prop(statvis, "thickness_min", text="Min")
                subrow.prop(statvis, "thickness_max", text="Max")
                subrow.prop(statvis, "thickness_samples", text="")
            if statvis.type == 'DISTORT':
                subrow.prop(statvis, "distort_min", text="Min")
                subrow.prop(statvis, "distort_max", text="Max")
            if statvis.type == 'SHARP':
                subrow.prop(statvis, "sharp_min", text="Min")
                subrow.prop(statvis, "sharp_max", text="Max")
            but_box_inner_col = but_box.split(factor=0.645, align=True)

            col = but_box_inner_col.column(align=True)
            col.prop(overlay, "grid_scale", text="Grid Scale")
            row = col.row(align=True)

            row.prop(overlay, "show_axis_x", text="X", toggle=True)
            row.prop(overlay, "show_axis_y", text="Y", toggle=True)
            row.prop(overlay, "show_axis_z", text="Z", toggle=True)
            row.prop(overlay, "show_floor", text="Floor", toggle=True)
            row.prop(overlay, "show_ortho_grid", text="Ortho", toggle=True)

            col = but_box_inner_col.column(align=True)
            col.prop(units, "system", text="")
            col.prop(units, "length_unit", text="")

            ###

            but_box_inner_col = but_box.column(align=True)

            tog_row = but_box_inner_col.row(align=True)
            if shading.type == 'SOLID':
                tog_row.prop(shading, "xray_alpha", text="X-Ray")
            elif shading.type == 'WIREFRAME':
                tog_row.prop(shading, "xray_alpha_wireframe", text="X-Ray")
            tog_row.prop(overlay, "backwire_opacity", text="Wires")
            tog_row.prop(
                    shading,
                    "show_xray",
                    text="",
                    icon='XRAY',
                    toggle=True,
                    invert_checkbox=False
            )

            shading_root = but_box_inner_col.row(align=True)

            if not shading.type == 'WIREFRAME':
                shading_root.template_icon_view(
                    shading,
                    "studio_light",
                    scale=2,
                    scale_popup=2.0
                )

            if shading.type == 'SOLID':
                shading_row = shading_root.split(factor=0.9, align=True)
                col = shading_row.row(align=True)

                subcol = col.column(align=True)
                subcol.prop_enum(
                    shading,
                    "color_type",
                    'MATERIAL'
                )
                subcol.prop_enum(
                    shading,
                    "color_type",
                    'VERTEX'
                )

                subcol = col.column(align=True)
                subcol.prop_enum(
                    shading,
                    "color_type",
                    'SINGLE'
                )
                subcol.prop_enum(
                    shading,
                    "color_type",
                    'TEXTURE'
                )

                subcol = col.column(align=True)
                subcol.prop_enum(
                    shading,
                    "color_type",
                    'OBJECT'
                )
                subcol.prop_enum(
                    shading,
                    "color_type",
                    'RANDOM'
                )
            elif shading.type == 'WIREFRAME':
                shading_row = shading_root.column(align=True)
                col = shading_row.row(align=True)

                subcol = col.column(align=True)
                subcol.prop_enum(
                    shading,
                    "wireframe_color_type",
                    'SINGLE'
                )

                subcol = col.column(align=True)
                subcol.prop_enum(
                    shading,
                    "wireframe_color_type",
                    'OBJECT'
                )

                subcol = col.column(align=True)
                subcol.prop_enum(
                    shading,
                    "wireframe_color_type",
                    'RANDOM'
                )
            elif shading.type == 'MATERIAL':
                shading_row = shading_root.row(align=True)
                col = shading_row.row(align=True)

                subcol = col.column(align=True)

                subrow = subcol.row(align=True)
                subrow.prop(
                    shading,
                    "studiolight_rotate_z",
                    text="Angle"
                )
                subrow.prop(
                    shading,
                    "studiolight_background_alpha",
                    text="Alpha"
                )
                subcol.prop(
                    shading,
                    "studiolight_intensity",
                )
            else:
                shading_row = shading_root.split(factor=0.9, align=True)

            col = shading_row.column(align=True)
            col.scale_y = 2
            if active_obj:
                if (shading.color_type == 'SINGLE' and (shading.type == 'SOLID'
                                                        or shading.type == 'WIREFRAME')):
                    if shading.type == 'WIREFRAME':
                        col.scale_y = 1
                    col.prop(shading, "single_color", text="")
                elif (shading.color_type == 'OBJECT' and active_obj.type == 'MESH'
                        and (shading.type == 'SOLID' or shading.type == 'WIREFRAME')):
                    if shading.type == 'WIREFRAME':
                        col.scale_y = 1
                    col.prop(active_obj, "color", text="")

        # Overlays Row
        if fp.fast_panel_tabs == 'OVERLAYS':
            but_box = col_1.box()
            # but_box.scale_y = 0.85
            but_box_inner_col = but_box.column(align=True)
            but_row = but_box_inner_col.row(align=True)
            # but_row.scale_x = 0.5

            but_row.prop(
                overlay,
                "show_edge_crease",
                text="Crease",
                toggle=True,
                icon='MOD_SUBSURF'
            )
            but_row.prop(
                overlay,
                "show_edge_sharp",
                text="Sharp",
                toggle=True,
                icon='MOD_EDGESPLIT'
            )
            but_row.prop(
                overlay,
                "show_edge_bevel_weight",
                text="Bevel",
                toggle=True,
                icon='MOD_BEVEL'
            )
            but_row.prop(
                overlay,
                "show_edge_seams",
                text="Seam",
                toggle=True,
                icon='UV_DATA'
            )

            but_row = but_box_inner_col.row(align=True)
            # but_row.scale_x = 0.5

            but_row.prop(
                overlay,
                "show_edges",
                text="Edges",
                toggle=True,
                icon='MOD_WIREFRAME'
            )
            but_row.prop(
                overlay,
                "show_faces",
                text="Faces",
                toggle=True,
                icon='FACE_MAPS'
            )
            but_row.prop(
                overlay,
                "show_face_center",
                text="Face Dots",
                toggle=True,
                icon='SNAP_FACE_CENTER'
            )

        # Normals Row
        if fp.fast_panel_tabs == 'NORMALS':
            but_box = col_1.box()
            # but_box.scale_y = 0.85
            but_box_inner_col = but_box.column(align=True)
            but_row = but_box_inner_col.row(align=True)
            # but_row.scale_x = 0.35

            but_row.prop(overlay, "normals_length", text="Normals")

            # but_row = but_box_inner_col.row(align=True)
            but_row.prop(
                overlay,
                "show_vertex_normals",
                text="",
                icon='NORMALS_VERTEX'
            )
            but_row.prop(
                overlay,
                "show_split_normals",
                text="",
                icon='NORMALS_VERTEX_FACE'
            )
            but_row.prop(
                overlay,
                "show_face_normals",
                text="",
                icon='NORMALS_FACE'
            )
            but_row.prop(
                overlay,
                "show_face_orientation",
                text="",
                toggle=True,
                invert_checkbox=False,
                icon='ORIENTATION_LOCAL'
            )

            but_row = but_box_inner_col.row(align=True)
            # but_row.scale_x = 0.65
            but_row.prop(
                shading,
                "show_backface_culling",
                text="Cull Backfaces",
                toggle=True,
                invert_checkbox=False,
            )
            but_row.prop(
                overlay,
                "show_face_orientation",
                text="Orientation",
                toggle=True,
                invert_checkbox=False,
            )
            if context.active_object:
                if context.mode == 'OBJECT' and context.active_object.type == 'MESH':
                    but_row.operator(
                        "object.shade_smooth"
                    )
                elif context.mode == 'OBJECT' and context.active_object.type == 'CURVE':
                    but_row.operator(
                        "curve.shade_smooth"
                    )
                elif context.mode == 'EDIT_MESH':
                    but_row.operator(
                        "mesh.faces_shade_smooth"
                    )
                if context.active_object.type == 'MESH':
                    active_mesh = context.active_object.data
                    but_row.prop(
                        active_mesh,
                        "use_auto_smooth",
                        text="",
                        icon='MOD_NORMALEDIT',
                        toggle=True
                    )

        # Gizmo Row
        if fp.fast_panel_tabs == 'GIZMOS':
            but_box = col_1.box()
            # but_box.scale_y = 0.85
            but_box_inner_col = but_box.column(align=True)
            but_row = but_box_inner_col.row(align=True)
            # but_row.scale_x = 0.65
            but_row.prop(scene.transform_orientation_slots[1], "type", text="")
            but_row.prop(
                view,
                "show_gizmo_object_translate",
                text="",
                toggle=True,
                icon='ORIENTATION_VIEW'
                )
            but_row.prop(
                view,
                "show_gizmo_object_rotate",
                text="",
                toggle=True,
                icon='DRIVER_ROTATIONAL_DIFFERENCE'
            )
            but_row.prop(
                view,
                "show_gizmo_object_scale",
                text="",
                toggle=True,
                icon='CON_SIZELIMIT'
            )

            but_row = but_box_inner_col.row(align=True)
            # but_row.scale_x = 0.85
            but_row.prop(
                context.preferences.view,
                "gizmo_size",
                text="Gizmo Size"
            )
            but_row.prop(
                view,
                "show_gizmo_empty_image",
                text="",
                toggle=True,
                icon='IMAGE_PLANE',
            )
            but_row.prop(
                view,
                "show_gizmo_empty_force_field",
                text="",
                toggle=True,
                icon='FORCE_VORTEX',
            )
            but_row.prop(
                view,
                "show_gizmo_light_size",
                text="",
                toggle=True,
                icon='OUTLINER_OB_LIGHT',
            )
            but_row.prop(
                view,
                "show_gizmo_light_look_at",
                text="",
                toggle=True,
                icon='LIGHT_SPOT',
            )
            but_row.prop(
                view,
                "show_gizmo_camera_lens",
                text="",
                toggle=True,
                icon='CON_CAMERASOLVER',
            )
            but_row.prop(
                view,
                "show_gizmo_camera_dof_distance",
                text="",
                toggle=True,
                icon='CAMERA_DATA',
            )
            but_row.prop(
                view,
                "show_gizmo",
                text="",
                toggle=True,
                icon='GIZMO',
            )

        # Display Row
        if fp.fast_panel_tabs == 'DISPLAY':
            but_box = col_1.box()
            # but_box.scale_y = 0.85
            but_box_inner_col = but_box.column(align=True)
            but_row = but_box_inner_col.row(align=True)
            # but_row.scale_x = 0.5

            if (context.active_object and context.active_object.type == 'MESH'):
                but_row.prop(context.object, 'display_type', expand=True)

                # if context.object.display_type == 'BOUNDS':
                #     but_row = but_box_inner_col.row(align=True)
                #     but_row.prop(
                #         context.object,
                #         'display_bounds_type',
                #         text="",
                #     )

                but_row = but_box_inner_col.split(factor=0.65, align=True)

                but_row_left = but_row.row(align=True)
                # but_row_left.scale_x = 0.5
                but_row_left.prop(
                    context.object,
                    'show_name',
                    text="Name",
                    toggle=True
                )
                but_row_left.prop(
                    context.object,
                    "show_wire",
                    text="Wires",
                    toggle=True
                )
                but_row_left.prop(
                    context.object,
                    "show_in_front",
                    text="Clip",
                    toggle=True,
                    invert_checkbox=True
                )
                but_row_left.prop(
                    context.object,
                    "show_axis",
                    text="Axis",
                    toggle=True
                )
                but_row_right = but_row.row(align=True)
                # but_row_right.separator(factor=1.5)
                but_row_right_inner = but_row_right.row(align=True)
                but_row_right_inner.scale_x = 1
                but_row_right_inner.prop(
                    context.object,
                    'display_bounds_type',
                    text="",
                )
                but_row_right_inner.prop(
                    context.object,
                    'show_bounds',
                    text="",
                    toggle=True,
                    icon='PIVOT_BOUNDBOX'
                )

            elif (active_obj and active_obj.type == 'EMPTY'):
                but_row.prop(
                    context.object,
                    'empty_display_type',
                    text="",
                    expand=False
                )
                but_row.prop(
                    context.object,
                    'parent',
                    text="",
                )

                but_row_split = but_box_inner_col.split(factor=0.5, align=True)

                but_row_split.prop(
                    context.object,
                    'empty_display_size',
                    text="",
                    expand=False
                )

                but_row_inner = but_row_split.row(align=True)

                but_row_inner.prop(
                    context.object,
                    'show_name',
                    text="Name",
                    toggle=True
                )
                but_row_inner.prop(
                    context.object,
                    'show_axis',
                    text="Axis",
                    toggle=True
                )

            elif (active_obj and active_obj.type == 'CAMERA'):
                but_row.prop(
                    context.object.data,
                    'show_limits',
                    text="Limits",
                    toggle=True
                )
                but_row.prop(
                    context.object.data,
                    'show_mist',
                    text="Mist",
                    toggle=True
                )
                but_row.prop(
                    context.object.data,
                    'show_sensor',
                    text="Sensor",
                    toggle=True
                )
                but_row.prop(
                    context.object.data,
                    'show_name',
                    text="Name",
                    toggle=True
                )

                but_row = but_box_inner_col.row(align=True)
                but_row.prop(
                    context.object.data,
                    'display_size',
                    text="Size",
                )


class VIEW3D_PT_grid_ribbon(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    # bl_category = "Ribbons"
    bl_label = "Grid Ribbon"
    text = "Bacon"

    @classmethod
    def get_shading(cls, context):
        view = context.space_data
        if view.type == 'VIEW_3D':
            return view.shading
        else:
            return context.scene.display.shading

    def draw(self, context):

        area = bpy.context.area
        resolution = bpy.context.preferences.system.ui_scale
        resolution_label = str(resolution)

        for reg in area.regions:
            if reg.type == 'UI':
                region_width_raw = reg.width

        region_width = region_width_raw - 40
        region_width_label = str(region_width)

        region_width_int = round(region_width / (20 * resolution))
        region_width_int_label = str(region_width_int)

        # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

        # region_width_factor = round((region_width / 440), 3)
        # region_width_factor_label = str(region_width_factor)

        layout = self.layout
        # layout.ui_units_x = region_width_int
        layout.scale_y = 0.85

        root = layout.column(align=True)

        break_info = root.row(align=True)

        break_info.label(text=region_width_label)
        break_info.label(text=region_width_int_label)
        break_info.label(text=resolution_label)

        if region_width_int >= 12:
            col_set_1 = 2
            col_set_2 = 4
            col_set_3 = 2
            col_set_4 = 3

        if region_width_int < 12:
            col_set_1 = 1
            col_set_2 = 2
            col_set_3 = 2
            col_set_4 = 3

        if region_width_int <= 8:
            col_set_1 = 1
            col_set_2 = 2
            col_set_3 = 2
            col_set_4 = 3

        if region_width_int <= 6:
            col_set_1 = 1
            col_set_2 = 1
            col_set_3 = 2
            col_set_4 = 3

        if region_width_int < 6:
            col_set_1 = 1
            col_set_2 = 1
            col_set_3 = 1
            col_set_4 = 3

        # Aliased Stuff
        scene = context.scene
        units = scene.unit_settings
        overlay = context.space_data.overlay

        grid_box = root.box()

        grid_box_inner_col = grid_box.column(align=False)

        row_1 = grid_box_inner_col.grid_flow(columns=col_set_1, align=True)

        row_1.prop(overlay, "grid_scale", text="Grid Scale")

        row_1_sub = row_1.grid_flow(columns=col_set_3, align=True)

        row_1_sub_left = row_1_sub.row(align=True)
        row_1_sub_left.prop(overlay, "show_floor", text="Floor", toggle=True)

        row_1_sub_right = row_1_sub.grid_flow(columns=col_set_4, align=True)
        row_1_sub_right.prop(overlay, "show_axis_x", text="X", toggle=True)
        row_1_sub_right.prop(overlay, "show_axis_y", text="Y", toggle=True)
        row_1_sub_right.prop(overlay, "show_axis_z", text="Z", toggle=True)

        row_2 = grid_box_inner_col.grid_flow(columns=col_set_2, align=True)

        row_2.prop(overlay, "grid_subdivisions", text="Subdivisions")
        row_2.prop(units, "scale_length", text="Unit Scale")
        row_2.prop(overlay, "show_ortho_grid", text="Ortho", toggle=True)
        row_2.prop(units, "length_unit", text="")


class VIEW3D_PT_snap_ribbon(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    # bl_category = "Ribbons"
    bl_label = "Snap Ribbon"

    @classmethod
    def get_shading(cls, context):
        view = context.space_data
        if view.type == 'VIEW_3D':
            return view.shading
        else:
            return context.scene.display.shading

    def draw(self, context):

        area = bpy.context.area
        resolution = bpy.context.preferences.system.ui_scale
        # resolution_label = str(resolution)

        for reg in area.regions:
            if reg.type == 'UI':
                region_width_raw = reg.width

        region_width = region_width_raw - 40
        # region_width_label = str(region_width)

        region_width_int = round(region_width / (20 * resolution))
        # region_width_int_label = str(region_width_int)

        layout = self.layout
        # layout.ui_units_x = region_width_int
        layout.scale_y = 0.85

        root = layout.column(align=True)

        # break_info = root.row(align=True)

        # break_info.label(text=region_width_label)
        # break_info.label(text=region_width_int_label)
        # break_info.label(text=resolution_label)

        if region_width_int >= 12:
            col_set_1 = 8
            col_set_2 = 4
            col_set_3 = 4

        if region_width_int < 12:
            col_set_1 = 8
            col_set_2 = 4
            col_set_3 = 4

        if region_width_int <= 8:
            col_set_1 = 8
            col_set_2 = 2
            col_set_3 = 2

        if region_width_int <= 6:
            col_set_1 = 4
            col_set_2 = 2
            col_set_3 = 2

        if region_width_int < 6:
            col_set_1 = 2
            col_set_2 = 1
            col_set_3 = 1
        tool_settings = context.scene.tool_settings

        snap_box = root.box()

        snap_box_inner_col = snap_box.column(align=True)
        snap_box_inner_row = snap_box_inner_col.column(align=False)

        first_row = snap_box_inner_row.grid_flow(columns=col_set_1, align=True)

        first_row.prop(
            tool_settings,
            "use_snap",
            text="",
            expand=True,
            toggle=True
        )
        first_row.prop_enum(
            tool_settings,
            "snap_elements",
            'INCREMENT',
            text=""
        )
        first_row.prop_enum(
            tool_settings,
            "snap_elements",
            'VERTEX',
            text=""
        )
        first_row.prop_enum(
            tool_settings,
            "snap_elements",
            'FACE',
            text=""
        )
        first_row.prop_enum(
            tool_settings,
            "snap_elements",
            'VOLUME',
            text=""
        )
        first_row.prop_enum(
            tool_settings,
            "snap_elements",
            'EDGE',
            text=""
        )
        first_row.prop_enum(
            tool_settings,
            "snap_elements",
            'EDGE_MIDPOINT',
            text=""
        )
        first_row.prop_enum(
            tool_settings,
            "snap_elements",
            'EDGE_PERPENDICULAR',
            text=""
        )

        second_row = snap_box_inner_row.grid_flow(columns=col_set_2, align=True)

        second_row.prop(
            tool_settings,
            "use_snap_align_rotation",
            text="Align",
            toggle=True
        )
        second_row.prop(
            tool_settings,
            "use_snap_peel_object",
            text="Peel",
            toggle=True
        )
        second_row.prop(
            tool_settings,
            "use_snap_project",
            text="Project",
            toggle=True
        )
        second_row.prop(
            tool_settings,
            "use_snap_grid_absolute",
            text="Absolute",
            toggle=True
        )

        third_row = snap_box_inner_row.grid_flow(columns=col_set_3, align=True)

        third_row.prop(
            tool_settings,
            "use_snap_rotate",
            text="Rotate",
            toggle=True
        )
        third_row.prop(
            tool_settings,
            "use_snap_translate",
            text="Move",
            toggle=True
        )
        third_row.prop(
            tool_settings,
            "use_snap_scale",
            text="Scale",
            toggle=True
        )
        third_row.prop(
            tool_settings,
            "snap_target",
            expand=False,
            text="",
        )


class VIEW3D_PT_draw_ribbon(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    # bl_category = "Ribbons"
    bl_label = "Draw Ribbon"

    @classmethod
    def get_shading(cls, context):
        view = context.space_data
        if view.type == 'VIEW_3D':
            return view.shading
        else:
            return context.scene.display.shading

    def draw(self, context):

        area = bpy.context.area
        resolution = bpy.context.preferences.system.ui_scale

        for reg in area.regions:
            if reg.type == 'UI':
                region_width_raw = reg.width

        region_width = region_width_raw - 40
        region_width_int = round(region_width / (20 * resolution))

        layout = self.layout

        root = layout.column(align=True)

        if region_width_int >= 12:
            tog_row_cols = 5
            # tog_row_labels = (
            #     'Measures',
            #     'Overlays',
            #     'Normals',
            #     'Gizmos',
            #     'Display'
            # )
            # tog_row_icons = (
            #     'NONE',
            #     'NONE',
            #     'NONE',
            #     'NONE',
            #     'NONE',
            # )
            cols_8_8_8_4_2 = 8
            cols_4_4_4_2_1 = 4
            cols_4_4_2_2_1 = 4
            cols_2_2_1_1_1 = 2
            cols_3_3_3_1_1 = 3
            giz_row_2_cols = 2

        if region_width_int < 12:
            tog_row_cols = 5
            # _tog_row_labels = (
            #     '',
            #     '',
            #     '',
            #     '',
            #     ''
            # )
            # _tog_row_icons = (
            #     'CON_SIZELIMIT',
            #     'OVERLAY',
            #     'NORMALS_VERTEX_FACE',
            #     'GIZMO',
            #     'OBJECT_DATA',
            # )
            cols_8_8_8_4_2 = 8
            cols_4_4_4_2_1 = 4
            cols_4_4_2_2_1 = 4
            cols_2_2_1_1_1 = 2
            cols_3_3_3_1_1 = 3
            giz_row_2_cols = 2

        if region_width_int <= 8:
            tog_row_cols = 5
            cols_8_8_8_4_2 = 8
            cols_4_4_4_2_1 = 2
            cols_4_4_2_2_1 = 2
            cols_2_2_1_1_1 = 1
            cols_3_3_3_1_1 = 3
            giz_row_2_cols = 2

        if region_width_int <= 6:
            tog_row_cols = 5
            cols_8_8_8_4_2 = 4
            cols_4_4_4_2_1 = 2
            cols_4_4_2_2_1 = 2
            cols_2_2_1_1_1 = 1
            cols_3_3_3_1_1 = 1
            giz_row_2_cols = 1

        if region_width_int < 6:
            tog_row_cols = 5
            cols_8_8_8_4_2 = 2
            cols_4_4_4_2_1 = 1
            cols_4_4_2_2_1 = 1
            cols_2_2_1_1_1 = 1
            cols_3_3_3_1_1 = 1
            giz_row_2_cols = 1

        # Aliased Stuff
        scene = context.scene
        # units = scene.unit_settings
        overlay = context.space_data.overlay
        view = context.space_data
        shading = VIEW3D_PT_view3d_fast_panel.get_shading(context)
        active_obj = context.active_object

        # Fast Panel Property Group
        wm = bpy.context.window_manager
        fp = wm.fp_props

        layout = self.layout
        # layout.ui_units_x = 11

        root = layout.column(align=True)
        root.scale_y = 1

        # ignoring Blender's variable naming conventions for UI layouts
        # because it's bad and you should feel bad for using it
        tab_row = root.grid_flow(columns=tog_row_cols, align=True)
        tab_row.prop(fp, "fast_panel_tabs", expand=True)

        # Measures Row
        if fp.fast_panel_tabs == 'MEASURES':
            but_box = root.box()
            but_box_inner_col = but_box.column(align=False)
            but_row = but_box_inner_col.grid_flow(columns=cols_4_4_4_2_1, align=True)

            but_row.prop(
                overlay,
                "show_extra_edge_length",
                text="Length",
                toggle=True
            )
            but_row.prop(
                overlay,
                "show_extra_edge_angle",
                text="Angle",
                toggle=True
            )
            but_row.prop(
                overlay,
                "show_extra_face_area",
                text="Area",
                toggle=True
            )
            but_row.prop(
                overlay,
                "show_extra_face_angle",
                text="Angle",
                toggle=True
            )

            but_row = but_box_inner_col.grid_flow(columns=cols_4_4_4_2_1, align=True)
            but_row.scale_x = 0.65
            measure_tool = but_row.operator(
                "wm.tool_set_by_id",
                text="Measure Tool"
            )
            measure_tool.name = "builtin.measure"
            measure_tool.space_type = "VIEW_3D"

            annotate_tool = but_row.operator(
                "wm.tool_set_by_id",
                text="Annotate Tool"
            )
            annotate_tool.name = "builtin.annotate"
            annotate_tool.space_type = "VIEW_3D"

        # Overlays Row
        if fp.fast_panel_tabs == 'OVERLAYS':
            but_box = root.box()
            but_box_inner_col = but_box.column(align=False)
            but_row = but_box_inner_col.grid_flow(columns=cols_4_4_4_2_1, align=True)

            but_row.prop(
                overlay,
                "show_edge_crease",
                text="Crease",
                toggle=True,
                icon='MOD_SUBSURF'
            )
            but_row.prop(
                overlay,
                "show_edge_sharp",
                text="Sharp",
                toggle=True,
                icon='MOD_EDGESPLIT'
            )
            but_row.prop(
                overlay,
                "show_edge_bevel_weight",
                text="Bevel",
                toggle=True,
                icon='MOD_BEVEL'
            )
            but_row.prop(
                overlay,
                "show_edge_seams",
                text="Seam",
                toggle=True,
                icon='UV_DATA'
            )

            but_row = but_box_inner_col.grid_flow(columns=cols_4_4_2_2_1, align=True)

            but_row.prop(
                overlay,
                "show_edges",
                text="Edges",
                toggle=True,
                icon='MOD_WIREFRAME'
            )
            but_row.prop(
                overlay,
                "show_faces",
                text="Faces",
                toggle=True,
                icon='FACE_MAPS'
            )
            but_row.prop(
                overlay,
                "show_face_center",
                text="Face Dots",
                toggle=True,
                icon='SNAP_FACE_CENTER'
            )

        # Normals Row
        if fp.fast_panel_tabs == 'NORMALS':
            but_box = root.box()
            but_box_inner_col = but_box.column(align=True)

            but_row = but_box_inner_col.grid_flow(columns=cols_2_2_1_1_1, align=True)

            sub1 = but_row.row(align=True)
            sub1.prop(overlay, "normals_length", text="Normals")

            sub2 = but_row.grid_flow(columns=cols_3_3_3_1_1, align=True)
            sub2.prop(
                overlay,
                "show_vertex_normals",
                text="",
                icon='NORMALS_VERTEX'
            )
            sub2.prop(
                overlay,
                "show_split_normals",
                text="",
                icon='NORMALS_VERTEX_FACE'
            )
            sub2.prop(
                overlay,
                "show_face_normals",
                text="",
                icon='NORMALS_FACE'
            )

            but_row = but_box_inner_col.grid_flow(align=True)
            but_row.scale_x = 0.65
            but_row.prop(
                shading,
                "show_backface_culling",
                text="Cull Backfaces",
                toggle=True,
                invert_checkbox=False,
            )
            but_row.prop(
                overlay,
                "show_face_orientation",
                text="Show Orientation",
                toggle=True,
                invert_checkbox=False,
            )

            if active_obj:
                if active_obj.type == 'MESH':
                    active_mesh = context.active_object.data
                    but_row.prop(
                        active_mesh,
                        "use_auto_smooth",
                        toggle=True
                    )

        # Gizmo Row
        if fp.fast_panel_tabs == 'GIZMOS':
            but_box = root.box()
            but_box_inner_col = but_box.column(align=False)

            row_1 = but_box_inner_col.grid_flow(
                                                columns=cols_2_2_1_1_1,
                                                align=True,
                                                even_columns=True
                                                )

            row_1.prop(
                context.preferences.view,
                "gizmo_size",
                text="Gizmo Size"
            )

            sub_row = row_1.grid_flow(columns=cols_8_8_8_4_2, align=True)
            sub_row.prop(
                view,
                "show_gizmo_empty_image",
                text="",
                toggle=True,
                icon='IMAGE_PLANE',
            )
            sub_row.prop(
                view,
                "show_gizmo_empty_force_field",
                text="",
                toggle=True,
                icon='FORCE_VORTEX',
            )
            sub_row.prop(
                view,
                "show_gizmo_light_size",
                text="",
                toggle=True,
                icon='OUTLINER_OB_LIGHT',
            )
            sub_row.prop(
                view,
                "show_gizmo_light_look_at",
                text="",
                toggle=True,
                icon='LIGHT_SPOT',
            )
            sub_row.prop(
                view,
                "show_gizmo_camera_lens",
                text="",
                toggle=True,
                icon='CON_CAMERASOLVER',
            )
            sub_row.prop(
                view,
                "show_gizmo_camera_dof_distance",
                text="",
                toggle=True,
                icon='CAMERA_DATA',
            )
            # sub_row.prop(
            #     view,
            #     "show_gizmo",
            #     text="",
            #     toggle=True,
            #     icon='GIZMO',
            # )

            row_2 = but_box_inner_col.grid_flow(columns=giz_row_2_cols, align=True)
            sub_row_1 = row_2.grid_flow(columns=3, align=True)
            sub_row_1.prop(
                view,
                "show_gizmo_object_translate",
                text="",
                toggle=True,
                icon='ORIENTATION_VIEW',
                )
            sub_row_1.prop(
                view,
                "show_gizmo_object_rotate",
                text="",
                toggle=True,
                icon='DRIVER_ROTATIONAL_DIFFERENCE'
            )
            sub_row_1.prop(
                view,
                "show_gizmo_object_scale",
                text="",
                toggle=True,
                icon='CON_SIZELIMIT'
            )
            sub_row_2 = row_2.row(align=True)
            sub_row_2.prop(
                scene.transform_orientation_slots[1],
                "type",
                text=""
            )

        # Display Row
        if fp.fast_panel_tabs == 'DISPLAY':
            but_box = root.box()
            # but_box.scale_y = 0.85
            but_box_inner_col = but_box.column(align=False)
            but_row_1 = but_box_inner_col.grid_flow(columns=cols_4_4_4_2_1,  align=True)
            # but_row.scale_x = 0.5

            if context.active_object.type == 'MESH':
                but_row_1.prop_enum(
                    context.object,
                    "display_type",
                    'BOUNDS',
                )
                but_row_1.prop_enum(
                    context.object,
                    "display_type",
                    'WIRE',
                )
                but_row_1.prop_enum(
                    context.object,
                    "display_type",
                    'SOLID',
                )
                but_row_1.prop_enum(
                    context.object,
                    "display_type",
                    'TEXTURED',
                )

                but_row_2 = but_box_inner_col.grid_flow(
                                                        columns=cols_4_4_4_2_1,
                                                        align=True,
                                                        even_columns=True
                                                        )

                but_row_2.prop(
                    context.object,
                    'show_name',
                    text="Name",
                    toggle=True
                )
                but_row_2.prop(
                    context.object,
                    "show_wire",
                    text="Wires",
                    toggle=True
                )
                but_row_2.prop(
                    context.object,
                    "show_in_front",
                    text="Clip",
                    toggle=True,
                    invert_checkbox=True
                )
                but_row_2.prop(
                    context.object,
                    'show_bounds',
                    text="Bounds",
                    toggle=True,
                )
                but_row_2.prop(
                    context.object,
                    "show_axis",
                    text="Axis",
                    toggle=True
                )
                but_row_2.prop(
                    context.object,
                    'display_bounds_type',
                    text="",
                    icon='REC'
                )

            elif context.active_object.type == 'EMPTY':
                but_row.prop(
                    context.object,
                    'empty_display_type',
                    text="",
                    expand=False
                )
                but_row.prop(
                    context.object,
                    'parent',
                    text="",
                )

                but_row_split = but_box_inner_col.split(factor=0.5, align=True)

                but_row_split.prop(
                    context.object,
                    'empty_display_size',
                    text="",
                    expand=False
                )

                but_row_inner = but_row_split.row(align=True)

                but_row_inner.prop(
                    context.object,
                    'show_name',
                    text="Name",
                    toggle=True
                )
                but_row_inner.prop(
                    context.object,
                    'show_axis',
                    text="Axis",
                    toggle=True
                )

            elif context.active_object.type == 'CAMERA':
                but_row.prop(
                    context.object.data,
                    'show_limits',
                    text="Limits",
                    toggle=True
                )
                but_row.prop(
                    context.object.data,
                    'show_mist',
                    text="Mist",
                    toggle=True
                )
                but_row.prop(
                    context.object.data,
                    'show_sensor',
                    text="Sensor",
                    toggle=True
                )
                but_row.prop(
                    context.object.data,
                    'show_name',
                    text="Name",
                    toggle=True
                )

                but_row = but_box_inner_col.row(align=True)
                but_row.prop(
                    context.object.data,
                    'display_size',
                    text="Size",
                )
