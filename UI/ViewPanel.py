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
from ..Utilities.WidthFunc import (
    get_breakpoints,
    # get_width_factor,
    check_width,
    get_break_full
)


class View3DPanel_hidden:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'

    @classmethod
    def poll(cls, context):
        if context.view_layer.objects.active:
            return True


class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ATB"

    @classmethod
    def poll(cls, context):
        if context.view_layer.objects.active:
            return True


class ATB_MT_MeshShadingMenu(bpy.types.Menu):
    bl_idname = "ATB_MT_MeshShadingMenu"
    bl_label = "Shading"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.shade_smooth")
        layout.operator("object.shade_flat")


class ATB_MT_MiscOverlaysMenu(bpy.types.Menu):
    bl_idname = "ATB_MT_MiscOverlaysMenu"
    bl_label = "Miscellaneous"

    def draw(self, context):
        layout = self.layout
        overlay = context.space_data.overlay

        layout.prop(overlay, "show_text")
        layout.prop(overlay, "show_annotation")
        layout.prop(overlay, "show_cursor")
        layout.prop(overlay, "show_extras", text="Show Extras")
        layout.prop(overlay, "show_relationship_lines")
        layout.prop(overlay, "show_outline_selected")
        layout.prop(overlay, "show_motion_paths")
        layout.prop(overlay, "show_object_origins")
        layout.prop(overlay, "show_object_origins_all")
        layout.prop(overlay, "show_face_orientation")
        layout.prop(overlay, "show_extra_indices")
        layout.prop(overlay, "show_occlude_wire")


class ATB_PT_MiscOverlaysPanel(View3DPanel_hidden, bpy.types.Panel):
    bl_idname = "ATB_PT_MiscOverlaysPanel"
    bl_label = "Miscellaneous Overlays"
    bl_ui_units_x = 8

    def draw(self, context):
        layout = self.layout
        layout.emboss = 'PULLDOWN_MENU'
        overlay = context.space_data.overlay

        col = layout.column_flow(align=True)
        col.alignment = 'LEFT'

        # TODO: Turn these toggle-icons into functions so I can use them anywhere

        ico = ("CHECKBOX_HLT" if overlay.show_text else "CHECKBOX_DEHLT")
        col.prop(overlay, "show_text", icon=ico)

        ico = ("CHECKBOX_HLT" if overlay.show_annotation else "CHECKBOX_DEHLT")
        col.prop(overlay, "show_annotation", icon=ico)

        ico = ("CHECKBOX_HLT" if overlay.show_cursor else "CHECKBOX_DEHLT")
        col.prop(overlay, "show_cursor", icon=ico)

        ico = ("CHECKBOX_HLT" if overlay.show_extras else "CHECKBOX_DEHLT")
        col.prop(overlay, "show_extras", text="Show Extras", icon=ico)

        ico = ("CHECKBOX_HLT" if overlay.show_relationship_lines else "CHECKBOX_DEHLT")
        col.prop(overlay, "show_relationship_lines", icon=ico)

        ico = ("CHECKBOX_HLT" if overlay.show_outline_selected else "CHECKBOX_DEHLT")
        col.prop(overlay, "show_outline_selected", icon=ico)

        ico = ("CHECKBOX_HLT" if overlay.show_motion_paths else "CHECKBOX_DEHLT")
        col.prop(overlay, "show_motion_paths", icon=ico)

        ico = ("CHECKBOX_HLT" if overlay.show_object_origins else "CHECKBOX_DEHLT")
        col.prop(overlay, "show_object_origins", icon=ico)

        ico = ("CHECKBOX_HLT" if overlay.show_object_origins_all else "CHECKBOX_DEHLT")
        col.prop(overlay, "show_object_origins_all", icon=ico)

        ico = ("CHECKBOX_HLT" if overlay.show_face_orientation else "CHECKBOX_DEHLT")
        col.prop(overlay, "show_face_orientation", icon=ico)

        ico = ("CHECKBOX_HLT" if overlay.show_extra_indices else "CHECKBOX_DEHLT")
        col.prop(overlay, "show_extra_indices", icon=ico)

        ico = ("CHECKBOX_HLT" if overlay.show_occlude_wire else "CHECKBOX_DEHLT")
        col.prop(overlay, "show_occlude_wire", icon=ico)


class ATB_PT_ViewOverlaysPanel(View3DPanel, bpy.types.Panel):
    bl_idname = "ATB_PT_ViewOverlaysPanel"
    bl_label = "Overlays"
    bl_options = {'DEFAULT_CLOSED', 'DRAW_BOX'}

    @classmethod
    def get_shading(cls, context):
        view = context.space_data
        if view.type == 'VIEW_3D':
            return view.shading
        else:
            return context.scene.display.shading

    def draw(self, context):
        scene = context.scene
        units = scene.unit_settings

        overlay = context.space_data.overlay
        shading = ATB_PT_ViewOverlaysPanel.get_shading(context)

        active_obj = context.view_layer.objects.active

        if active_obj:
            if active_obj.type == 'MESH':
                active_mat = active_obj.active_material
                active_mesh = active_obj.data

        mesh_anal = context.scene.tool_settings.statvis
        tool_settings = context.scene.tool_settings
        motion_tracking = context.space_data.show_reconstruction
        space_data = context.space_data
        v3dtheme = context.preferences.themes[0].view_3d

        y_scale = 0.85

        layout = self.layout
        root = layout.column(align=True)

        # Shading Type
        # row = layout.row(align=True)
        col = root.column(align=True)
        # col.scale_y = y_scale

        check = check_width('UI', 5, 1)

        # if check[0]:
        #     row = col.row(align=True)
        # else:
        #     row = col.column(align=True)

        if shading.type == 'SOLID':

            if check[0]:
                # row = col.row(align=True)
                row = col.column(align=True)
            else:
                row = col.column(align=True)

            # row.column(align=True).prop(shading, "light", expand=True)

            row.prop(shading, "light", expand=False, text="")

            if shading.light == 'STUDIO':
                prefs = context.preferences
                system = prefs.system
                subrow = col.row(align=True)
                subrow.prop(
                    shading,
                    "use_world_space_lighting",
                    text="",
                    icon='WORLD'
                )
                subrow.prop(shading, "studiolight_rotate_z", text="Rotation")

                if not system.use_studio_light_edit:
                    row.template_icon_view(
                        shading,
                        "studio_light",
                        scale=3,
                        scale_popup=3.0
                    )
                else:
                    row.prop(
                        system,
                        "use_studio_light_edit",
                        text="Disable Studio Light Edit",
                        icon='NONE',
                        toggle=True,
                    )
            elif shading.light == 'MATCAP':

                row.template_icon_view(
                    shading,
                    "studio_light",
                    scale=3,
                    scale_popup=3.0
                )

        # Object Color

        check = check_width('UI', 5, 1, 20)
        col_count = 2
        col = col.column(align=False)
        col.scale_y = y_scale
        row = col.row(align=True)

        box = col.column(align=True)
        if check[0]:
            split = box.split(factor=0.78, align=True)
            col_count = 2
        else:
            split = box.column(align=True)
            col_count = 1
        subcol_0 = split.column(align=True)

        # subcol_1.grid_flow(columns=-2, align=True)
        if shading.type == 'SOLID':
            subcol_1 = subcol_0.grid_flow(columns=col_count, align=True)
            subcol_1.scale_x = 0.33333
            # subcol_1.prop(
            #     shading, "color_type", expand=True
            # )
            subcol_1.prop_enum(
                shading,
                "color_type",
                'MATERIAL'
            )
            subcol_1.prop_enum(
                shading,
                "color_type",
                'VERTEX'
            )
            subcol_1.prop_enum(
                shading,
                "color_type",
                'SINGLE'
            )
            subcol_1.prop_enum(
                shading,
                "color_type",
                'TEXTURE'
            )
            subcol_1.prop_enum(
                shading,
                "color_type",
                'OBJECT'
            )
            subcol_1.prop_enum(
                shading,
                "color_type",
                'RANDOM'
            )
        elif shading.type == 'WIREFRAME':
            subcol_1 = subcol_0.grid_flow(columns=1, align=True)
            subcol_1.prop(
                shading, "wireframe_color_type", expand=True
            )

        sub = split.column(align=True)
        sub.scale_y = 3.2
        if shading.type == 'WIREFRAME':
            if shading.wireframe_color_type == 'SINGLE':
                sub.prop(shading, "single_color", text="")
            elif (shading.wireframe_color_type == 'OBJECT'
                    and active_obj.type == 'MESH'):
                sub.prop(active_obj, "color", text="")

        if (shading.type == 'SOLID' and active_obj):
            if shading.color_type == 'SINGLE':
                sub.prop(shading, "single_color", text="")
            elif (shading.color_type == 'OBJECT'
                    and active_obj.type == 'MESH'):
                sub.prop(active_obj, "color", text="")
            elif (shading.color_type == 'MATERIAL'
                    and active_obj.type == 'MESH'):
                if active_obj.active_material:
                    sub.prop(active_mat, "diffuse_color", text="")
                    if shading.light == 'STUDIO':
                        col.prop(active_mat, "metallic", text="Metalic")
                        col.prop(active_mat, "roughness", text="Rougness")

        # Shading Options
        # col.separator()
        col = col.column(align=False)
        col = col.column(align=True)
        col.label(text="Viewport:")
        # col.scale_y = y_scale

        row = col.row(align=True)
        if not shading.show_xray:
            row.prop(shading, "show_xray", text="X-Ray", toggle=True)
        if shading.show_xray:
            box = row.box()

            bcol = box.column(align=True)

            brow = bcol.row(align=True)
            brow.label(text="X-Ray:")
            brow.prop(
                    shading,
                    "show_xray",
                    text="",
                    icon='X',
                    toggle=True,
                    invert_checkbox=False
            )

            row = bcol.column(align=True)
            row.prop(shading, "xray_alpha", text="Opacity")
            row.prop(overlay, "backwire_opacity", text="Backwires")
            # row.prop(
            #         shading,
            #         "show_xray",
            #         text="",
            #         icon='X',
            #         toggle=True,
            #         invert_checkbox=False
            # )

        row = col.row(align=True)
        if not shading.show_shadows:
            row.prop(shading, "show_shadows", text="Shadows", toggle=True)
        if shading.show_shadows:
            box = row.box()

            bcol = box.column(align=True)

            brow = bcol.row(align=True)
            brow.label(text="Shadows:")
            brow.prop(
                    shading,
                    "show_shadows",
                    text="",
                    icon='X',
                    toggle=True,
                    invert_checkbox=False
            )

            row = bcol.row(align=True)
            row.prop(shading, "shadow_intensity", text="Intensity")
            # row = bcol.row(align=True)
            row.popover(
                panel="VIEW3D_PT_shading_options_shadow",
                icon='TOOL_SETTINGS',
                text="",
            )

        row = col.row(align=True)

        if not shading.show_cavity:
            row.prop(shading, "show_cavity", text="Cavity", toggle=True)

        if shading.show_cavity:

            # row.prop(shading, "cavity_type", text="")
            box = col.box()

            sub = box.column(align=True)

            row_split = sub.split(factor=0.35, align=True)
            row_split_1 = row_split.row(align=True)
            row_split_1.label(text="Cavity:")
            row_split_2 = row_split.row(align=True)
            row_split_2.prop(shading, "cavity_type", text="")
            row_split_2.prop(
                shading,
                "show_cavity",
                text="",
                icon='X',
                toggle=True
            )

            subcol = sub.split(factor=0.5)

            subcol_1 = subcol.column(align=True)
            subcol_1.active = False
            subcol_1.active = (True if shading.cavity_type
                               in {'WORLD', 'BOTH'}
                               and shading.show_cavity else False)
            subcol_1.label(text="World:")
            subcol_1.prop(shading, "cavity_ridge_factor", text="Ridge")
            subcol_1.prop(shading, "cavity_valley_factor", text="Valley")

            subcol_2 = subcol.column(align=True)
            subcol_2.active = False
            subcol_2.active = (True if shading.cavity_type
                               in {'SCREEN', 'BOTH'}
                               and shading.show_cavity else False)
            subcol_2.label(text="Screen:")
            subcol_2.prop(shading, "curvature_ridge_factor", text="Ridge")
            subcol_2.prop(shading, "curvature_valley_factor", text="Valley")

        if not overlay.show_statvis:
            row = col.row(align=True)
            row.prop(
                    overlay,
                    "show_statvis",
                    text="Mesh Analysis",
                    toggle=True
            )
        elif overlay.show_statvis:
            row = col.row(align=False)

            box = row.box()
            bcol = box.column(align=True)

            brow = bcol.row(align=True)
            brow.label(text="Mesh Analysis:")
            brow.prop(
                overlay,
                "show_statvis",
                text="",
                icon='X',
                toggle=True
            )

            # bcol.label(text="Mesh Analysis:")

            brow = bcol.row(align=True)

            brow.prop(mesh_anal, "type", text="")

            OHang_F1_T = (2, 3, 6, 8)
            OHang_F1_V = (1, 2, 3, 6)
            OHang_F1 = get_breakpoints('UI', OHang_F1_T, OHang_F1_V)

            if mesh_anal.type == 'OVERHANG':
                # box = col.box()
                subcol = bcol.column(align=True)
                sub = subcol.row(align=True)
                subcol = sub.column(align=True)

                subrow = subcol.grid_flow(columns=OHang_F1[0] - 1, align=True)
                subrow.prop(mesh_anal, "overhang_min")
                subrow.prop(mesh_anal, "overhang_max")

                subrow = subcol.grid_flow(columns=OHang_F1[0], align=True)
                subrow.scale_y = y_scale
                subrow.prop(mesh_anal, "overhang_axis", text="", expand=False)

            if mesh_anal.type == 'THICKNESS':
                # box = col.box()
                subcol = bcol.column(align=True)
                sub = subcol.row(align=True)
                subrow = subcol.grid_flow(columns=OHang_F1[0] - 2, align=True)
                subrow.prop(mesh_anal, "thickness_min")
                subrow.prop(mesh_anal, "thickness_max")
                subrow.prop(mesh_anal, "thickness_samples")

            if mesh_anal.type == 'DISTORT':
                # box = col.box()
                subcol = bcol.column(align=True)
                sub = subcol.row(align=True)
                subrow = subcol.grid_flow(columns=OHang_F1[0] - 2, align=True)
                subrow.prop(mesh_anal, "distort_min")
                subrow.prop(mesh_anal, "distort_max")

            if mesh_anal.type == 'SHARP':
                # box = col.box()
                subcol = bcol.column(align=True)
                sub = subcol.row(align=True)
                subrow = subcol.grid_flow(columns=OHang_F1[0] - 2, align=True)
                subrow.prop(mesh_anal, "sharp_min", text="Shap Min")
                subrow.prop(mesh_anal, "sharp_max", text="Shap Max")

        row = col.row(align=True)
        show_weight_check = check_width('UI', 10, 1, 20)

        if not overlay.show_weight:
            row.prop(overlay, "show_weight", toggle=True)
        if overlay.show_weight:
            if show_weight_check[0]:
                row.prop(tool_settings, "vertex_group_user", expand=True)
                row.prop(overlay, "show_weight", text="", icon='X')
            else:
                row.prop_menu_enum(
                                tool_settings,
                                "vertex_group_user",
                                text="Weights"
                )
                row.prop(overlay, "show_weight", text="", icon='X')

        row = col.row(align=True)

        MoTr_F1_T = (2, 7)
        MoTr_F1_V = (1, 2)
        MoTr_F1_V_Full = (
                ((" ", " "), ('CURVE_PATH', 'PMARKER_ACT')),
                (("Camera Path", "Marker Names"), ('NONE', 'NONE'))
            )
        MoTr_F1_full = get_breakpoints('UI', MoTr_F1_T, MoTr_F1_V_Full)
        MoTr_F1 = get_breakpoints('UI', MoTr_F1_T, MoTr_F1_V)

        if not motion_tracking:
            row.prop(
                space_data,
                "show_reconstruction",
                text="Motion Tracking",
                toggle=True
            )
        if motion_tracking:
            row.prop(
                space_data,
                "show_camera_path",
                text=MoTr_F1_full[0][0][0],
                icon=MoTr_F1_full[0][1][0],
                toggle=True
            )
            row.prop(
                space_data,
                "show_bundle_names",
                text=MoTr_F1_full[0][0][1],
                icon=MoTr_F1_full[0][1][1],
                toggle=True
            )
            row.prop(
                space_data,
                "show_reconstruction",
                text="",
                icon='X',
                toggle=True
            )
            sub = col.box()
            subrow = sub.grid_flow(columns=MoTr_F1[0], align=True)
            subrow.prop(space_data, "tracks_display_type", text="")
            subrow.prop(space_data, "tracks_display_size", text="Size")

        row = col.row(align=True)
        op = row.operator("wm.call_panel", text="Extras")
        op.name = "ATB_PT_MiscOverlaysPanel"

        # $$Edge_Overlays

        thresholds = (4, 6, 10, 14)
        values = (1, 2, 4, 4)

        EO_Col = get_breakpoints('UI', thresholds, values)

        col = root.column(align=True)
        col.scale_y = y_scale

        col.label(text="Edges:")

        row = col.grid_flow(
                            columns=EO_Col[0],
                            align=True
        )
        row.scale_x = 0.465
        row.prop(overlay, "show_edges", text="Wire", toggle=True)
        row.prop(
            overlay,
            "show_extra_edge_length",
            text="Length",
            toggle=True
        )
        row.prop(
            overlay,
            "show_extra_edge_angle",
            text="Angle",
            toggle=True
        )
        row.prop(
            overlay,
            "show_freestyle_edge_marks",
            text="Freestyle",
            toggle=True
        )
        row.prop(overlay, "show_edge_crease", text="Creases", toggle=True)
        row.prop(overlay, "show_edge_sharp", text="Sharps", toggle=True)
        row.prop(overlay, "show_edge_bevel_weight", text="Bevels", toggle=True)
        row.prop(overlay, "show_edge_seams", text="Seams", toggle=True)

        # Face Overlays
        full_breaks = get_break_full(
                                    'UI',
                                    (2, 5, 10, 14),
                                    (2, 4, 6, 8),
                                    '>',
                                    True,
                                    True
        )

        col = root.column(align=True)
        col.scale_y = y_scale

        col.label(text="Faces:")

        ##
        row = col.grid_flow(
                            columns=full_breaks[1],
                            even_columns=True,
                            even_rows=True,
                            align=True
        )
        row.scale_x = 0.465
        row.prop(overlay, "show_faces", text="Selected", toggle=True)
        row.prop(overlay, "show_face_center", text="Centers", toggle=True)
        row.prop(
            overlay,
            "show_extra_face_area",
            text="Area",
            toggle=True
        )
        row.prop(
            overlay,
            "show_extra_face_angle",
            text="Angle",
            toggle=True
        )

        row = col.row(align=True)
        row.prop(
            overlay,
            "show_freestyle_face_marks",
            text="Freestyle",
            toggle=True
        )

        # Geometry

        # TODO: What the hell is up with this naming?

        # Flow_1
        GeC_F1_T = (2, 8)
        GeC_F1_V = (1, 2)
        GeC_F1 = get_breakpoints('UI', GeC_F1_T, GeC_F1_V)

        # Flow_1_Sub
        GeC_F1S_T = (2, 6)
        GeC_F1S_V = (1, 2)
        GeC_F1S = get_breakpoints('UI', GeC_F1S_T, GeC_F1S_V)

        # Flow_2
        GeC_F2_T = (2, 6)
        GeC_F2_V = (1, 3,)
        GeC_F2 = get_breakpoints('UI', GeC_F2_T, GeC_F2_V)

        # Flow_3
        GeC_F3_T = (2, 6)
        GeC_F3_V = (1, 2)
        GeC_F3 = get_breakpoints('UI', GeC_F3_T, GeC_F3_V)

        # Flow_3_Sub
        GeC_F3S_T = (1, 3)
        GeC_F3S_V = (1, 3)
        GeC_F3S = get_breakpoints('UI', GeC_F3S_T, GeC_F3S_V)

        col = root.column(align=True)
        col.scale_y = y_scale
        col.label(text="Normals:")

        row = col.row(align=True)

        if active_obj and active_obj.type == 'MESH':
            if not active_mesh.use_auto_smooth:
                row.prop(active_mesh, "use_auto_smooth", toggle=True)
            if active_mesh.use_auto_smooth:
                box = row.box()

                bcol = box.column(align=True)

                row = bcol.row(align=True)
                row.label(text="Auto-Smooth:")
                row.prop(
                    active_mesh,
                    "use_auto_smooth",
                    text="",
                    icon="X",
                    toggle=True
                )
                row = bcol.row(align=True)
                # row.scale_x = 0.85

                row.prop(active_mesh, "auto_smooth_angle", text="")
                row.menu("ATB_MT_MeshShadingMenu")

        flow_3 = col.grid_flow(columns=GeC_F3[0], align=True, row_major=True)
        # flow_3 = col.row(align=True)

        row = flow_3.split(factor=0.5, align=True)
        row.prop(overlay, "normals_length", text="Normals")

        flow_3_sub = row.grid_flow(
                                        columns=GeC_F3S[0],
                                        align=True,
                                        row_major=True
        )
        flow_3_sub.prop(
            overlay,
            "show_vertex_normals",
            text="",
            icon='NORMALS_VERTEX'
        )
        flow_3_sub.prop(
            overlay,
            "show_split_normals",
            text="",
            icon='NORMALS_VERTEX_FACE'
        )
        flow_3_sub.prop(
                    overlay,
                    "show_face_normals",
                    text="",
                    icon='NORMALS_FACE'
        )

        col = root.column(align=True)
        col.scale_y = y_scale
        col.label(text="Geo:")

        flow_1 = col.grid_flow(columns=GeC_F1[0], align=True, row_major=True)

        flow_1.prop(v3dtheme, "vertex_size", text="Verts")
        flow_1.prop(v3dtheme, "facedot_size", text="Dots")

        flow_1_sub = col.grid_flow(
                                    columns=GeC_F1S[0],
                                    align=True,
                                    row_major=True
        )
        flow_1_sub.prop(
            overlay,
            "show_wireframes",
            text="Wire All",
            toggle=True
        )
        flow_1_sub.prop(
                active_obj,
                "show_wire",
                text="Wire Object",
                icon='NONE',
                toggle=True
        )

        flow_2 = col.grid_flow(columns=GeC_F2[0], align=True, row_major=True)
        flow_2.prop(overlay, "show_edges", text="Edges", toggle=True)
        flow_2.prop(overlay, "show_faces", text="Faces", toggle=True)
        flow_2.prop(overlay, "show_face_center", text="Centers", toggle=True)

        # Grid

        # Flow_1
        GC_F1_T = (2, 5)
        GC_F1_V = (1, 2)
        GC_F1 = get_breakpoints('UI', GC_F1_T, GC_F1_V)

        # Flow_2
        GC_F2_T = (2, 9)
        GC_F2_V = (1, 3,)
        GC_F2 = get_breakpoints('UI', GC_F2_T, GC_F2_V)

        # Flow_3
        GC_F3_T = (2, 5)
        GC_F3_V = (1, 2)
        GC_F3 = get_breakpoints('UI', GC_F3_T, GC_F3_V)

        col = root.column(align=True)
        col.scale_y = y_scale

        col.label(text="Grid:")

        ##
        flow_1 = col.grid_flow(
            columns=GC_F1[0],
            align=True
        )

        row = flow_1.row(align=True)
        row.prop(overlay, "show_floor", text="Floor", toggle=True)
        row.prop(overlay, "show_ortho_grid", text="Ortho", toggle=True)
        sub = flow_1.row(align=True)
        sub.prop(overlay, "show_axis_x", text="X", toggle=True)
        sub.prop(overlay, "show_axis_y", text="Y", toggle=True)
        sub.prop(overlay, "show_axis_z", text="Z", toggle=True)
        ##

        ##
        flow_2 = col.grid_flow(
            columns=GC_F2[0],
            align=True
        )

        flow_2.prop(overlay, "grid_scale", text="Scale")
        flow_2.prop(overlay, "grid_subdivisions", text="Subdivisions")
        flow_2.prop(units, "scale_length", text="Units")
        ##

        ##
        flow_3 = col.grid_flow(
            columns=GC_F3[0],
            align=True
        )

        flow_3.prop(units, "system", text="")
        flow_3.prop(units, "length_unit", text="")


# TODO: MIGRATE

class ATB_PT_viewport_transform_settings(View3DPanel_hidden, bpy.types.Panel):
    bl_idname = "ATB_PT_viewport_transform_settings"
    bl_label = "Quick Transforms"

    def draw(self, context):
        scene = context.scene
        tool_settings = context.scene.tool_settings

        y_scale = 0.85
        x_scale = 0.75

        layout = self.layout

        col = layout.column(align=True)

        subrow = col.row(align=True)
        # subrow.label(text="Orientation:")
        subrow.prop(scene.transform_orientation_slots[0], "type", text="")
        subrow.operator(
            "transform.create_orientation",
            text="",
            icon="ADD"
        ).use = True
        subrow.operator(
            "transform.delete_orientation",
            text="",
            icon="REMOVE"
        )
        subrow.operator(
            "transform.transform",
            text="",
            icon="ORIENTATION_VIEW"
        ).mode = 'ALIGN'

        col.separator()

        subrow = col.row(align=True)
        # subrow.label(text="Pivot:")
        subrow.prop(
            tool_settings,
            "transform_pivot_point",
            text="",
            expand=False
        )
        subrow.prop(
            tool_settings,
            "use_transform_data_origin",
            text="",
            icon='MESH_DATA',
            toggle=True
        )
        subrow.prop(
            tool_settings,
            "use_transform_pivot_point_align",
            text="",
            icon='CON_PIVOT',
            toggle=True
        )
        subrow.prop(
            tool_settings,
            "use_transform_skip_children",
            text="",
            icon='CON_CHILDOF',
            toggle=True
        )

        col.separator()

        subrow = col.row(align=True)
        # subrow.label(text="Snap:")

        # Yoinked from space_view3d.py 478-489
        snap_items = bpy.types.ToolSettings.bl_rna.properties["snap_elements"].enum_items
        snap_elements = tool_settings.snap_elements
        if len(snap_elements) == 1:
            text = ""
            for elem in snap_elements:
                text = str(snap_items[elem].name)
                icon = snap_items[elem].icon
                break
        else:
            text = "Mix"
            icon = 'NONE'
        del snap_items, snap_elements

        if scene.snap_cycle == 0:

            subrow.prop_menu_enum(tool_settings, "snap_elements", text=text, icon=icon)
            # subrow.prop_tabs_enum(tool_settings, "snap_elements")
            subrow.prop(
                tool_settings,
                "use_snap",
                text="",
                toggle=True
            )
            subrow.prop(
                tool_settings,
                "use_snap_align_rotation",
                text="",
                toggle=True,
                icon="SNAP_NORMAL"
            )
            props = subrow.operator(
                                "wm.context_cycle_int",
                                text="",
                                icon="TRIA_DOWN"
            )
            props.data_path = "scene.snap_cycle"
            props.wrap = True

        if scene.snap_cycle >= 1:
            subrow.alignment = 'RIGHT'
            subrow.prop(tool_settings, "snap_elements", text="", expand=True)
            subrow.separator()
            subrow.prop(
                tool_settings,
                "use_snap",
                text="",
                expand=True,
                toggle=True
            )
            subrow.prop(
                tool_settings,
                "use_snap_align_rotation",
                text="",
                toggle=True,
                icon="SNAP_NORMAL"
            )
            props = subrow.operator(
                                "wm.context_cycle_int",
                                text="",
                                icon="TRIA_DOWN"
            )
            props.data_path = "scene.snap_cycle"
            props.wrap = True

        # if scene.snap_cycle >= 1:

        if scene.snap_cycle == 2:
            # subrow.prop(
            #     tool_settings,
            #     "use_snap",
            #     text="",
            #     expand=True,
            #     toggle=True
            # )
            # props = subrow.operator(
            #                     "wm.context_cycle_int",
            #                     text="",
            #                     icon="TRIA_DOWN"
            # )
            # props.data_path = "scene.snap_cycle"
            # props.wrap = True
            # subrow.label(text="Snapping")
            box = col.box()
            subcol = box.column(align=True)
            subcol.scale_y = y_scale

            subrow = subcol.grid_flow(align=True)
            subrow.scale_x = 0.5
            subrow.prop(tool_settings, "snap_target", expand=True)

            # subcol.separator(factor=2)

            # subflow = subcol.grid_flow(
            #                     columns=-1,
            #                     align=True,
            #                     even_columns=True,
            #                     even_rows=True,
            #                     row_major=True
            # )
            # subflow.scale_x = x_scale
            # subflow.prop_enum(
            #     tool_settings,
            #     "snap_elements",
            #     'VERTEX'
            # )
            # subflow.prop_enum(
            #     tool_settings,
            #     "snap_elements",
            #     'EDGE'
            # )
            # subflow.prop_enum(
            #     tool_settings,
            #     "snap_elements",
            #     'FACE'
            # )
            # subflow.prop_enum(
            #     tool_settings,
            #     "snap_elements",
            #     'VOLUME'
            # )
            # subflow.prop_enum(
            #     tool_settings,
            #     "snap_elements",
            #     'EDGE_MIDPOINT'
            # )
            # subflow.prop_enum(
            #     tool_settings,
            #     "snap_elements",
            #     'EDGE_PERPENDICULAR'
            # )

            # subflow = subcol.grid_flow(columns=1, align=True)
            # subflow.prop_enum(tool_settings, "snap_elements", 'INCREMENT')

            # subcol.separator(factor=1.5)
            subcol = box.column(align=True)

            subflow = subcol.grid_flow(columns=-1, align=True)
            subflow.scale_x = x_scale
            subflow.prop(
                tool_settings,
                "use_snap_align_rotation",
                text="Align to Normal",
                toggle=True
            )
            subflow.prop(
                tool_settings,
                "use_snap_peel_object",
                text="Snap Peel",
                toggle=True
            )
            subflow.prop(
                tool_settings,
                "use_snap_project",
                text="Snap Project",
                toggle=True
            )
            subflow.prop(
                tool_settings,
                "use_snap_grid_absolute",
                text="Absolute Grid Snap",
                toggle=True
            )

            # subcol.separator(factor=2)

            subcol = box.column(align=True)

            subflow = subcol.grid_flow(
                columns=-1,
                align=True,
                even_columns=True,
                even_rows=True,
                row_major=True
            )
            subflow.scale_x = x_scale
            subflow.prop(
                tool_settings,
                "use_snap_translate",
                text="Affect Translation",
                toggle=True
            )
            subflow.prop(
                tool_settings,
                "use_snap_rotate",
                text="Affect Rotation",
                toggle=True
            )

            subflow = subcol.grid_flow(columns=-1, align=True)
            subflow.scale_x = x_scale
            subflow.prop(
                tool_settings,
                "use_snap_scale",
                text="Affect Scale",
                toggle=True
            )

# TODO: Migrate these to somewhere logical

class ATB_PT_quick_operators(View3DPanel, bpy.types.Panel):
    bl_idname = "ATB_PT_quick_operators"
    bl_label = "Menu Panel"

    def draw(self, context):
        layout = self.layout
        wm = bpy.context.window_manager
        qm_props = context.workspace.ATB

        tb_root = layout.column(align=True)
        # tb_root.label(text="Operator Toolbox:")

        menu = "VIEW3D_MT_select_edit_mesh"

        if qm_props.qm_menus == 'EDIT':
            menu = "VIEW3D_MT_edit_mesh"
        if qm_props.qm_menus == "ADD":
            menu = "VIEW3D_MT_mesh_add"
        if qm_props.qm_menus == "UV":
            menu = "VIEW3D_MT_uv_map"
        if qm_props.qm_menus == "CONTEXT":
            menu = "VIEW3D_MT_edit_mesh_context_menu"
        if qm_props.qm_menus == "VERTEX":
            menu = "VIEW3D_MT_edit_mesh_vertices"
        if qm_props.qm_menus == "EDGE":
            menu = "VIEW3D_MT_edit_mesh_edges"
        if qm_props.qm_menus == "FACE":
            menu = "VIEW3D_MT_edit_mesh_faces"

        tb_root.prop(qm_props, "qm_menus", text="")

        box = tb_root.box()

        b_col = box.column(align=True)
        b_col.menu_contents(menu)
