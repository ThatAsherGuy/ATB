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


# import rna_prop_ui
import bpy
from bpy.types import (
    Panel,
    Curve,
    SurfaceCurve
)
from ..Utilities.WidthFunc import (
    get_breakpoints,
    # get_width_factor,
    check_width,
    get_break_full
)
from bl_ui.space_toolsystem_toolbar import (
    VIEW3D_PT_tools_active as view3d_tools
)
from bpy_extras.node_utils import find_node_input

# from .. Icons import get_icon_id, initialize_icons_collection


def active_tool():
    return view3d_tools.tool_active_from_context(bpy.context)


class VIEW3D_PT_meta_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ATB"
    bl_label = "Meta Panel"

    bl_ui_units_x = 12

    @staticmethod
    def _active_context_member(context):
        obj = context.object
        if obj:
            object_mode = obj.mode
            if object_mode == 'POSE':
                return "active_pose_bone"
            elif object_mode == 'EDIT' and obj.type == 'ARMATURE':
                return "active_bone"
            else:
                return "object"

        return ""

    @classmethod
    def transform_poll(cls, context):
        import rna_prop_ui
        member = cls._active_context_member(context)

        if member:
            context_member, member = rna_prop_ui.rna_idprop_context_value(context, member, object)
            return context_member and rna_prop_ui.rna_idprop_has_properties(context_member)

        return False

    @classmethod
    def get_shading(cls, context):
        view = context.space_data
        if view.type == 'VIEW_3D':
            return view.shading
        else:
            return context.scene.display.shading

    def draw(self, context):

        active_obj = context.view_layer.objects.active
        wm = bpy.context.window_manager
        tabs = wm.metapanel_tabs
        metapanel = wm.metapanel_tabs

        if not tabs.tab:
            tabs.tab = '0'

        # Aliased Stuff
        scene = context.scene
        tool_settings = context.scene.tool_settings

        units = scene.unit_settings
        overlay = context.space_data.overlay
        v3dtheme = context.preferences.themes[0].view_3d

        layout = self.layout

        root = layout.column(align=True)

        tb_width_check = check_width('UI', 12, 1, 440)

        tab_labels = [
                    ("Transforms", ""),
                    ("Cameras", ""),
                    ("Shading", ""),
                    ("Active", ""),
        ]

        tb_ico_only = 0
        if not tb_width_check[0]:
            tb_ico_only = 1

        tb_row = root.row(align=True)
        tb_row.alignment = 'RIGHT'
        # tb_row.prop(tabs, 'tab', expand=True, icon_only=tb_ico_only)

        tb_row.prop_enum(
                        tabs,
                        'tab',
                        '0',
                        text=tab_labels[0][tb_ico_only]
        )
        tb_row.prop_enum(
                        tabs,
                        'tab',
                        '1',
                        text=tab_labels[1][tb_ico_only]
        )
        tb_row.prop_enum(
                        tabs,
                        'tab',
                        '2',
                        text=tab_labels[2][tb_ico_only]
        )
        tb_row.prop_enum(
                        tabs,
                        'tab',
                        '3',
                        text=tab_labels[3][tb_ico_only]
        )

        rbox = root.box()
        bcol = rbox.column(align=True)

        # $$Move Tab
        if tabs.tab == '0':

            orient_slot = scene.transform_orientation_slots[0]
            orientation = orient_slot.custom_orientation

            # Group 1 - Transform Orientation and Pivot
            bcol.label(text="Orientation and Pivot")

            g1_r = bcol.row(align=True)
            g1_r.prop_enum(
                        orient_slot,
                        "type",
                        'GLOBAL',
                        text=""
                        )
            g1_r.prop_enum(
                        orient_slot,
                        "type",
                        'LOCAL',
                        text=""
                        )
            g1_r.prop_enum(
                        orient_slot,
                        "type",
                        'NORMAL',
                        text=""
                        )
            g1_r.prop_enum(
                        orient_slot,
                        "type",
                        'CURSOR',
                        text=""
                        )
            g1_r.prop(orient_slot, "type", text="")

            flow = bcol.grid_flow(columns=2, align=True)
            g_1 = flow.column(align=True)

            g_1_r_1 = g_1.row(align=True)
            g_1_r_1.prop(orient_slot, "type", text="")

            if orientation:
                g_1_r_1.prop(orientation, "name", text="")

            g_1_r_1.operator(
                "transform.create_orientation",
                text="",
                icon="ADD"
            ).use = True
            g_1_r_1.operator(
                "transform.delete_orientation",
                text="",
                icon="REMOVE"
            )
            g_1_r_1.operator(
                "transform.transform",
                text="",
                icon="ORIENTATION_VIEW"
            ).mode = 'ALIGN'

            g_1_r_2 = g_1.row(align=True)
            g_1_r_2.prop(
                tool_settings,
                "transform_pivot_point",
                text="",
                expand=False
            )
            g_1_r_2.prop(
                tool_settings,
                "use_transform_data_origin",
                text="",
                icon='MESH_DATA',
                toggle=True
            )
            g_1_r_2.prop(
                tool_settings,
                "use_transform_pivot_point_align",
                text="",
                icon='CON_PIVOT',
                toggle=True
            )
            g_1_r_2.prop(
                tool_settings,
                "use_transform_skip_children",
                text="",
                icon='CON_CHILDOF',
                toggle=True
            )

            # Group 2 - Proportional Editing

            bcol.separator()
            bcol.label(text="Proportional Editing")

            g2 = bcol.grid_flow(columns=1, align=True)
            g2.separator(factor=0.25)
            g2_s1 = g2.row(align=True)
            # g2_s1.alignment = 'CENTER'

            obj = context.active_object
            object_mode = 'OBJECT' if obj is None else obj.mode

            # Copied from space_view3d.py
            if object_mode in {'EDIT', 'PARTICLE_EDIT', 'SCULPT_GPENCIL', 'EDIT_GPENCIL', 'OBJECT'}:
                kw = {}
                if object_mode == 'OBJECT':
                    attr = "use_proportional_edit_objects"
                else:
                    attr = "use_proportional_edit"

                    if tool_settings.use_proportional_edit:
                        if tool_settings.use_proportional_connected:
                            kw["icon"] = 'PROP_CON'
                        elif tool_settings.use_proportional_projected:
                            kw["icon"] = 'PROP_PROJECTED'
                        else:
                            kw["icon"] = 'PROP_ON'
                    else:
                        kw["icon"] = 'PROP_OFF'

                proport_label = "Falloff"
                if tool_settings.proportional_edit_falloff == 'SMOOTH':
                    proport_label = "Smooth"
                elif tool_settings.proportional_edit_falloff == 'SPHERE':
                    proport_label = "Sphere"
                elif tool_settings.proportional_edit_falloff == 'ROOT':
                    proport_label = "Root"
                elif tool_settings.proportional_edit_falloff == 'INVERSE_SQUARE':
                    proport_label = "Inverse Square"
                elif tool_settings.proportional_edit_falloff == 'SHARP':
                    proport_label = "Sharp"
                elif tool_settings.proportional_edit_falloff == 'LINEAR':
                    proport_label = "Linear"
                elif tool_settings.proportional_edit_falloff == 'CONSTANT':
                    proport_label = "Constant"
                elif tool_settings.proportional_edit_falloff == 'RANDOM':
                    proport_label = "Random"

                exp = False
                g2_check = check_width('UI', 11, 1, 440)
                proport_label = ""
                if not g2_check[0]:
                    exp = False
                    proport_label = ""

                g2_s1.prop(tool_settings, attr, text=proport_label, icon_only=True, **kw)
                g2_s1.prop(tool_settings, "proportional_edit_falloff", expand=exp, text="")
                quarg = (True if context.mode != 'OBJECT' else False)

                g2_s2_t = (2, 3, 6)
                g2_s2_v = (1, 1, 2)
                g2_s2_cols = get_breakpoints('UI', g2_s2_t, g2_s2_v)

                g2_s2 = g2.grid_flow(columns=g2_s2_cols[0], align=True)
                g2_s2.active = quarg
                g2_s2.prop(
                    tool_settings,
                    "use_proportional_connected",
                    text="Connected",
                    toggle=True
                )
                g2_s2.prop(
                    tool_settings,
                    "use_proportional_projected",
                    text="Project",
                    toggle=True
                )

            # Group 3 - Snapping
            bcol.separator()
            bcol.label(text="Snapping")

            g3 = bcol.grid_flow(columns=1, align=True)
            g3.separator(factor=0.25)
            rr_1 = g3.row(align=True)

            bcr1_t = (6, 8, 12)
            bcr1_v = (1, 1, 1)
            bcr1_cols = get_breakpoints('UI', bcr1_t, bcr1_v)
            bcol_rg1 = rr_1.grid_flow(columns=bcr1_cols[0], align=True)

            bcol_rg1 = rr_1.row(align=True)

            # Row 1 Sub 1
            bcr1_s1_t = (2, 5, 8)
            bcr1_s1_v = (2, 4, 8)
            bcr1_s1_cols = get_breakpoints('UI', bcr1_s1_t, bcr1_s1_v)
            bcr1_s1_cols = get_break_full('UI', bcr1_s1_t, bcr1_s1_v, '>=', False, True)

            snp_elem = "bcol_row1_sub1.prop(tool_settings, 'snap_elements', text='', expand=False)"
            if bcr1_s1_cols[5] < 20:
                snp_elem = "bcol_row1_sub1.prop_menu_enum(tool_settings, 'snap_elements')"

            bcol_row1_sub1 = bcol_rg1.grid_flow(
                                            columns=bcr1_s1_cols[0],
                                            align=True
            )

            bcol_row1_sub1 = bcol_rg1.grid_flow(columns=8, align=True)
            exec(snp_elem)
            # bcol_row1_sub1.prop(tool_settings, "use_snap", text="")

            bcol_rg2 = rr_1.row(align=True)

            bcol_rg2.prop(
                        tool_settings,
                        "use_snap_project",
                        text="",
                        icon='MOD_SHRINKWRAP',
                        toggle=True
            )
            bcol_rg2.prop(
                        tool_settings,
                        "use_snap_align_rotation",
                        text="",
                        icon='CON_SHRINKWRAP',
                        toggle=True
            )
            bcol_rg2.prop(
                        tool_settings,
                        "use_snap_peel_object",
                        text="",
                        icon='MOD_SOLIDIFY',
                        toggle=True
            )

            rr_2 = g3.row(align=True)
            rr_2L = rr_2.row(align=True)
            rr_2L.prop(tool_settings, "snap_target", text="")

            rr_2R = rr_2.row(align=True)

            rr_2R.prop(
                        tool_settings,
                        "use_snap_rotate",
                        text="",
                        icon='FORCE_CURVE',
                        toggle=True
            )
            rr_2R.prop(
                        tool_settings,
                        "use_snap_translate",
                        text="",
                        icon='CON_LOCLIKE',
                        toggle=True
            )
            rr_2R.prop(
                        tool_settings,
                        "use_snap_grid_absolute",
                        text="",
                        icon='SNAP_GRID',
                        toggle=True
            )

            # Group 4 - Grid

            bcol.separator()
            bcol.label(text="Grid")
            g4 = bcol.grid_flow(columns=1, align=True)
            # g4.separator(factor=0.25)

            row_1 = g4.split(factor=0.5, align=True)

            row_1_l = row_1.row(align=True)
            row_1_l.prop(overlay, "grid_scale")

            row_1_r = row_1.row(align=True)
            # row_1_r.prop(overlay, "show_floor", toggle=True, text="Floor")
            row_1_r.prop(units, "length_unit", text="")

            row_2 = g4.split(factor=0.5, align=True)

            row_2_l = row_2.row(align=True)
            row_2_l.prop(overlay, "show_ortho_grid", toggle=True, text="Ortho Grid")

            row_2_r = row_2.split(factor=0.5, align=True)
            row_2_r.prop(overlay, "show_floor", toggle=True, text="Floor")

            row_2_r.prop(overlay, "show_axis_x", toggle=True, text="X")
            row_2_r.prop(overlay, "show_axis_y", toggle=True, text="Y")
            row_2_r.prop(overlay, "show_axis_z", toggle=True, text="Z")

        # $$CameraManager Tab
        if tabs.tab == '1':

            bcol.label(text="Scene Cameras:")

            subcol = bcol.column(align=True)

            for cam in bpy.data.cameras:
                if cam.users > 0:
                    row = subcol.row(align=True)
                    row.prop(
                        cam,
                        "name",
                        text=""
                        )
                    if bpy.context.view_layer.objects.active and bpy.context.view_layer.objects.active.name == cam.name:
                        sel_icon = 'RESTRICT_SELECT_OFF'
                    else:
                        sel_icon = 'RESTRICT_SELECT_ON'

                    if context.scene.camera and context.scene.camera.name == cam.name:
                        icon = 'RADIOBUT_ON'
                    else:
                        icon = 'RADIOBUT_OFF'

                    op = row.operator(
                        "wm.context_set_id",
                        text="",
                        icon=icon
                    )
                    op.data_path = "scene.camera"
                    op.value = str(cam.name)

                    op = row.operator(
                        "atb.zoop",
                        text="",
                        icon='SNAP_FACE_CENTER'
                    )
                    op.target_camera = str(cam.name)

                    op = row.operator(
                        "atb.object_select",
                        text="",
                        icon=sel_icon
                    )
                    op.target_object = str(cam.name)

            if active_obj and active_obj.type == 'CAMERA':
                camera = active_obj
            elif context.space_data.region_3d.view_perspective == 'CAMERA':
                camera = context.space_data.camera
            else:
                camera = None

            if camera:
                bcol.label(text="Selected Camera:")

                if context.scene.camera and context.scene.camera.name == camera.name:
                    icon = 'RADIOBUT_ON'
                else:
                    icon = 'RADIOBUT_OFF'

                row = bcol.row(align=True)

                # row.template_ID(context.view_layer.objects, "active", filter='AVAILABLE')

                row.prop(
                    camera,
                    "name",
                    text=""
                    )

                op = row.operator(
                    "wm.context_set_id",
                    text="",
                    icon=icon
                )
                op.data_path = "scene.camera"
                op.value = str(camera.name)

                op = row.operator(
                    "atb.zoop",
                    text="",
                    icon='SNAP_FACE_CENTER')

                op.target_camera = str(camera.name)

                # bcol.label(text="Show:")

                row = bcol.row(align=True)

                row.prop(
                    camera.data,
                    'show_limits',
                    text="Limits",
                    toggle=True
                )
                row.prop(
                    camera.data,
                    'show_mist',
                    text="Mist",
                    toggle=True
                )
                row.prop(
                    camera.data,
                    'show_sensor',
                    text="Sensor",
                    toggle=True
                )
                row.prop(
                    camera.data,
                    'show_name',
                    text="Name",
                    toggle=True
                )

                row = bcol.row(align=True)
                row.prop(
                    camera.data,
                    'display_size',
                    text="Display Size",
                )

                sub = bcol.row(align=True)
                sub.prop(
                    camera.data,
                    'show_passepartout',
                    text="Dim Outer",
                    toggle=True
                )
                sub.prop(
                    camera.data,
                    'passepartout_alpha',
                    text="",
                )

                bcol.label(text="Settings:")

                col = bcol.column(align=True)

                sub = col.row(align=True)

                if camera.data.sensor_fit == 'AUTO':
                    sub.prop(
                        camera.data,
                        'sensor_width',
                        text="Sensor Size",
                    )
                elif camera.data.sensor_fit == 'HORIZONTAL':
                    sub.prop(
                        camera.data,
                        'sensor_width',
                        text="Sensor Width",
                    )
                elif camera.data.sensor_fit == 'VERTICAL':
                    sub.prop(
                        camera.data,
                        'sensor_height',
                        text="Sensor Height",
                    )

                op = sub.operator(
                    "wm.context_cycle_enum",
                    text="",
                    icon='CON_SIZELIKE'
                )
                op.data_path = "object.data.sensor_fit"
                op.wrap = True

                sub = col.row(align=True)

                if camera.data.lens_unit == 'MILLIMETERS':
                    sub.prop(
                        camera.data,
                        'lens',
                    )
                else:
                    sub.prop(
                        camera.data,
                        'angle',
                    )

                op = sub.operator(
                    "wm.context_toggle_enum",
                    text="",
                    icon='OUTLINER_OB_CAMERA'
                )
                op.data_path = str(camera.data.lens_unit)
                op.value_1 = 'FOV'
                op.value_2 = 'MILLIMETERS'

                col = bcol.column(align=True)
                sub = col.row(align=True)

                sub.prop(
                    camera.data,
                    'clip_start'
                )

                sub.prop(
                    camera.data,
                    'clip_end'
                )

                bcol.label(text="Actions:")

                col = bcol.column(align=True)
                sub = col.row(align=True)

                if context.scene.keying_sets.active:
                    # sub.prop(
                    #     context.scene.keying_sets.active,
                    #     "bl_label",
                    #     text="",
                    #     expand=True
                    # )
                    sub.prop_search(
                        context.scene.keying_sets,
                        "active",
                        context.scene,
                        "keying_sets",
                        text="",
                        )

                sub.operator(
                    'atb.add_camera_keyset',
                    text='',
                    icon='KEYINGSET'
                )
                sub.operator(
                    'anim.keyframe_insert',
                    text='',
                    icon='KEY_HLT'
                )
                sub.operator(
                    'anim.keyframe_delete',
                    text='',
                    icon='KEY_DEHLT'
                )

                sub = col.row(align=True)

                sub.prop(
                    context.space_data,
                    'lock_camera',
                    text="Track Camera to View",
                    toggle=True
                )

                sub = col.row(align=True)

                sub.operator(
                    "view3d.zoom_camera_1_to_1",
                    text="1:1"
                )
                sub.operator(
                    "view3d.view_center_camera",
                    text="Recenter"
                )

                if False in camera.lock_location or False in camera.lock_rotation:
                    op_text = "Lock"
                    tog = False
                else:
                    op_text = "Unlock"
                    tog = True

                subsub = sub.row(align=True)
                subsub.alert = tog

                op = subsub.operator(
                    "atb.lock_camera",
                    text=op_text,
                    # depress=tog
                )
                op.target_object = str(camera.name)

                sub = col.row(align=True)
                sub.operator(
                    "view3d.view_selected",
                    text="Zoop",
                )
                sub.operator(
                    "view3d.zoom_border",
                    text="Zoom"
                )
                sub.operator(
                    "view3d.walk",
                    text="Walk"
                )

                col = bcol.column(align=True)
                col.scale_y = 0.75
                col.prop(
                    camera,
                    'location',
                )

                col = bcol.column(align=True)
                col.scale_y = 0.75
                col.prop(
                    camera,
                    'rotation_euler',
                )

                bcol.label(text="Overlays:")

                col = bcol.column(align=True)
                sub = col.row(align=True)

                sub.prop(
                    camera.data,
                    'show_composition_thirds',
                    text="Thirds",
                    toggle=True
                )
                sub.prop(
                    camera.data,
                    'show_composition_center',
                    text="Center",
                    toggle=True
                )
                sub.prop(
                    camera.data,
                    'show_composition_golden',
                    text="Phi",
                    toggle=True
                )

        # $$Display Tab
        if tabs.tab == '2':
            # active_obj = context.active_object
            shading = self.get_shading(context)
            overlay = context.space_data.overlay

            if active_obj:
                if active_obj.type == 'MESH':
                    active_mat = active_obj.active_material
                    # active_mesh = context.active_object.data

            g2 = bcol.column(align=True)
            g2.active = (True if shading.type in {'SOLID'} else False)
            g2.scale_y = 1

            g2_r1 = g2.row(align=True)
            g2_r1_c1 = g2_r1.column(align=True)
            g2_r1_c1.ui_units_x = 3.75
            # g2_r1_c1.label(text="Shading")
            g2_r1_c1.prop(shading, "light", expand=True)
            if shading.light == 'MATCAP':
                g2_r1_c1_sub = g2_r1_c1.row(align=True)
                g2_r1_c1_sub.operator(
                                    "view3d.toggle_matcap_flip",
                                    text="Flip",
                                    icon='ARROW_LEFTRIGHT'
                                    )
                g2_r1_c1_sub.operator("preferences.studiolight_show", text="", icon='PREFERENCES')
            if shading.light == 'STUDIO':
                g2_r1_c1_sub = g2_r1_c1.row(align=True)
                g2_r1_c1_sub.prop(
                                shading,
                                "use_world_space_lighting",
                                text="",
                                toggle=True,
                                icon='WORLD'
                                )
                g2_r1_c1_sub.prop(
                                shading,
                                "studiolight_rotate_z",
                                text=""
                                )

            g2_r1_c2 = g2_r1.column(align=True)
            g2_r1_c2.enabled = (True if shading.light in {'MATCAP', 'STUDIO'} else False)
            asdasd_scale = (4 if shading.light in {'MATCAP', 'STUDIO'} else 3)
            g2_r1_c2.template_icon_view(
                shading,
                "studio_light",
                scale=asdasd_scale,
                scale_popup=3
            )
            # g2_r1_c2_sub = g2_r1_c2.row(align=True)
            # g2_r1_c2_sub.scale_y = 1
            # if shading.light == 'MATCAP':
            #     g2_r1_c2_sub.operator(
            #                         "view3d.toggle_matcap_flip",
            #                         text="Flip",
            #                         icon='ARROW_LEFTRIGHT'
            #                         )
            #     g2_r1_c2_sub.operator("preferences.studiolight_show", text="", icon='PREFERENCES')
            # if shading.light == 'STUDIO':
            #     g2_r1_c2_sub.prop(
            #                     shading,
            #                     "use_world_space_lighting",
            #                     text="",
            #                     toggle=True,
            #                     icon='WORLD'
            #                     )
            #     g2_r1_c2_sub.prop(
            #                     shading,
            #                     "studiolight_rotate_z",
            #                     text="Rotation"
            #                     )

            # bcol.separator()
            bcol.label(text="Color")

            g1 = bcol.split(factor=0.75, align=True)

            g1_left = g1.column(align=True)
            g1_left.scale_y = 1

            shade_mode = " "
            shade_submodes = ('SINGLE', 'OBJECT', 'RANDOM', 'MATERIAL', 'VERTEX', 'TEXTURE')
            shade_len = 3

            if shading.type == 'SOLID':
                shade_mode = "color_type"
                g1_left_1 = g1_left.row(align=True)
            elif shading.type == 'WIREFRAME':
                shade_mode = "wireframe_color_type"
                g1_left_1 = g1_left.row(align=True)
                g1_left.scale_y = 2

            if shading.type == 'SOLID' or shading.type == 'WIREFRAME':
                for i in range(0, shade_len):
                    g1_left_1.prop_enum(
                        shading, shade_mode, shade_submodes[i]
                    )

                if shading.type == 'SOLID':
                    g1_left_2 = g1_left.row(align=True)
                    for i in range(0, shade_len):
                        g1_left_2.prop_enum(
                            shading, shade_mode, shade_submodes[i+3]
                        )

            g1_c2 = g1.grid_flow(align=True)
            g1_c2.scale_y = 2

            if shading.type == 'WIREFRAME':
                if shading.wireframe_color_type == 'SINGLE':
                    g1_c2.prop(v3dtheme, "wire", text="")
                    # g1_c2.prop(shading, "single_color", text="")
                elif (shading.wireframe_color_type == 'OBJECT'
                        and active_obj.type == 'MESH'):
                    g1_c2.prop(active_obj, "color", text="")

            if (shading.type == 'SOLID' and active_obj):
                if shading.color_type == 'SINGLE':
                    g1_c2.prop(shading, "single_color", text="")
                elif (shading.color_type == 'OBJECT'
                        and active_obj.type == 'MESH'):
                    g1_c2.prop(active_obj, "color", text="")
                elif (shading.color_type == 'MATERIAL'
                        and active_obj.type == 'MESH'):
                    if active_obj.active_material:
                        g1_c2.prop(active_mat, "diffuse_color", text="")
                        if shading.light == 'STUDIO':
                            col = bcol.row(align=True)
                            col.prop(active_mat, "metallic", text="Metalic")
                            col.prop(active_mat, "roughness", text="Rougness")

            # $$Xray
            bcol.label(text="X-Ray")
            row = bcol.row(align=True)

            row_left = row.column(align=True)
            row_left.scale_y = 2

            ico = ('CUBE' if shading.show_xray else 'MESH_CUBE')
            row_left.prop(shading, "show_xray", text="", toggle=True, icon=ico)

            row_right = row.column(align=True)
            row_right.scale_y = 1
            row_right.active = shading.show_xray

            row_right.prop(shading, "xray_alpha")
            row_right.prop(overlay, "backwire_opacity")

            # $$Cavity
            bcol.label(text="Cavity")
            c_col = bcol.column(align=True)

            row = c_col.row(align=True)

            press1 = (True if shading.cavity_type
                      in {'WORLD', 'BOTH'}
                      and shading.show_cavity else False)

            press2 = (True if shading.cavity_type
                      in {'SCREEN', 'BOTH'}
                      and shading.show_cavity else False)

            ico = ('WORLD_DATA' if metapanel.cavity_toggle[1] else 'WORLD_DATA')
            op = row.operator("act.bool_to_enum", text="", icon=ico, depress=press1)
            op.bool_prop = 'window_manager.metapanel_tabs.cavity_toggle'
            op.enum_prop_path = 'space_data.shading.cavity_type'
            op.bool_index = 1

            sub = row.split(factor=0.45, align=True)
            sub.active = press1

            sub_sub = sub.row(align=True)
            sub_sub.prop(shading, "cavity_ridge_factor", text="Ridge", icon='WORLD')
            sub_sub = sub.row(align=True)
            sub_sub.prop(shading, "cavity_valley_factor", text="Valley", icon='WORLD')
            sub_sub.popover(
                panel="VIEW3D_PT_shading_options_ssao",
                icon='PREFERENCES',
                text="",
            )

            row = c_col.row(align=True)

            ico = ('RESTRICT_VIEW_OFF' if metapanel.cavity_toggle[0] else 'RESTRICT_VIEW_ON')
            op = row.operator("act.bool_to_enum", text="", icon=ico, depress=press2)
            op.bool_prop = 'window_manager.metapanel_tabs.cavity_toggle'
            op.enum_prop_path = 'space_data.shading.cavity_type'
            op.bool_index = 0

            sub = row.row(align=True)
            sub.active = press2

            sub.prop(shading, "curvature_ridge_factor", text="Ridge")
            sub.prop(shading, "curvature_valley_factor", text="Valley")

            # $$Lighting
            bcol.label(text="Shadow")
            row = bcol.row(align=True)
            row.prop(shading, "show_shadows", text="", icon='LIGHT_HEMI')
            sub_row = row.row(align=True)
            sub_row.active = shading.show_shadows
            sub_row.prop(shading, "shadow_intensity", text="Shadow Intensity")
            sub_row.popover(
                panel="VIEW3D_PT_shading_options_shadow",
                icon='PREFERENCES',
                text="",
            )

            # $$Background Color
            bcol.label(text="Background")

            if shading.background_type == 'VIEWPORT':

                bck_row = bcol.split(factor=0.75, align=True)
                bck_row_left = bck_row.row(align=True)
                bck_row_left.prop(shading, "background_type", expand=True)

                bck_row_right = bck_row.row(align=True)

                bck_row_right.prop(shading, "background_color", text="")

            if shading.background_type == 'THEME':

                bck_row = bcol.split(factor=0.75, align=True)
                bck_row_left = bck_row.row(align=True)
                bck_row_left.prop(shading, "background_type", expand=True)

                bck_row_right = bck_row.row(align=True)

                v3dtheme_gradient = context.preferences.themes[0].view_3d.space.gradients
                bck_row_right.prop(v3dtheme_gradient, "high_gradient", text="")

            if shading.background_type == 'WORLD':
                world = context.scene.world

                bck_row = bcol.row(align=True)

                bck_row_left = bck_row.row(align=True)
                bck_row_left.prop(shading, "background_type", expand=True)

                bck_row_right = bck_row.row(align=True)
                wrld_row = bcol.column(align=True)
                wrld_row.prop(world, "use_nodes", text="↓ Use Nodes ↓", toggle=True)
                wrld_row.separator()

                if world.use_nodes:
                    ntree = world.node_tree
                    node = ntree.get_output_node('EEVEE')

                    if node:
                        input = find_node_input(node, 'Surface')
                        if input:
                            node_row = bcol.column(align=True)
                            node_row.template_node_view(ntree, node, input)
                        else:
                            bck_row_right.label(text="Incompatible output node")
                    else:
                        bck_row_right.label(text="No output node")
                else:
                    bck_row_right.prop(world, "color", text="")

            # $$Options
            bcol.label(text="Options")
            # row = bcol.row(align=True)

            split = bcol.split(factor=0.725, align=True)

            split_l = split.row(align=True)
            split_l.alignment = 'LEFT'

            ico = ('CHECKBOX_HLT' if shading.show_object_outline else 'CHECKBOX_DEHLT')
            split_l.prop(
                        shading,
                        "show_object_outline",
                        text="Object Outlines",
                        toggle=True,
                        icon=ico,
                        emboss=False
                        )

            split_r = split.row(align=True)
            split_r.prop(shading, "object_outline_color", text="")

            row = bcol.row(align=True)
            row.alignment = 'LEFT'

            ico = ('CHECKBOX_HLT' if shading.show_backface_culling else 'CHECKBOX_DEHLT')
            row.prop(shading, "show_backface_culling", icon=ico, emboss=False)

            row = bcol.row(align=True)
            row.alignment = 'LEFT'

            ico = ('CHECKBOX_HLT' if shading.use_dof else 'CHECKBOX_DEHLT')
            row.prop(shading, "use_dof", toggle=True, icon=ico, emboss=False)

            row = bcol.row(align=True)
            row.alignment = 'LEFT'

            ico = ('CHECKBOX_HLT' if shading.show_specular_highlight else 'CHECKBOX_DEHLT')
            row.prop(
                        shading,
                        "show_specular_highlight",
                        text="Specular Highlights",
                        icon=ico,
                        toggle=True,
                        emboss=False
                        )

            # ico = ('CHECKBOX_HLT' if shading.show_backface_culling else 'CHECKBOX_DEHLT')
            # split_l.prop(shading, "show_backface_culling", icon=ico, emboss=False)

        # $$Active Object Tab
        if tabs.tab == '3':
            # active_obj = context.active_object
            shading = self.get_shading(context)
            overlay = context.space_data.overlay

            ocol = bcol.column(align=True)
            row = ocol.row(align=True)
            row.template_ID(context.view_layer.objects, "active", filter='AVAILABLE')

            row = ocol.row(align=True)
            # row.prop(tabs, "exp_objpointer")

            if active_obj and (active_obj.type == 'MESH'):

                ocol.label(text="Display As:")

                row_width_check = check_width('UI', 10, 1, 440)

                row_labels = [
                            ("Bounds", " "),
                            ("Wire", " "),
                            ("Solid", " "),
                            ("Textured", " "),
                ]

                row_icons = [
                            ('NONE', 'MESH_CUBE'),
                            ('NONE', 'SHADING_WIRE'),
                            ('NONE', 'SHADING_SOLID'),
                            ('NONE', 'SHADING_TEXTURE'),
                ]

                label_tog = 0
                row_cols = 3
                if not row_width_check[0]:
                    label_tog = 1

                row = ocol.row(align=True)
                # row.prop(context.object, 'display_type', expand=True)
                row.prop_enum(
                            context.object,
                            'display_type',
                            'BOUNDS',
                            text=row_labels[0][label_tog],
                            icon=row_icons[0][label_tog]
                            )
                row.prop_enum(
                            context.object,
                            'display_type',
                            'WIRE',
                            text=row_labels[1][label_tog],
                            icon=row_icons[1][label_tog]
                            )
                row.prop_enum(
                            context.object,
                            'display_type',
                            'SOLID',
                            text=row_labels[2][label_tog],
                            icon=row_icons[2][label_tog]
                            )
                row.prop_enum(
                            context.object,
                            'display_type',
                            'TEXTURED',
                            text=row_labels[3][label_tog],
                            icon=row_icons[3][label_tog]
                            )
                row = ocol.row(align=True)

                shade_mode = "space_data.shading.color_type"

                if shading.type == 'SOLID':
                    shade_mode = "space_data.shading.color_type"
                    if (shading.color_type == 'OBJECT'):
                        label = "Object Color"
                    elif (shading.color_type == 'SINGLE'):
                        label = "Single Color"
                    elif (shading.color_type == 'MATERIAL'):
                        label = "Material Color"
                    elif (shading.color_type == 'VERTEX'):
                        label = "Vertex Color"
                    elif (shading.color_type == 'RANDOM'):
                        label = "Random Color"
                    elif (shading.color_type == 'TEXTURE'):
                        label = "Texture"
                    else:
                        label = "ERROR"
                elif shading.type == 'WIREFRAME':
                    shade_mode = "space_data.shading.wireframe_color_type"
                    if (shading.wireframe_color_type == 'OBJECT'):
                        label = "Object Color"
                    elif (shading.wireframe_color_type == 'SINGLE'):
                        label = "Single Color"
                    else:
                        label = "ERROR"
                else:
                    label = "No."
                # elif shading.type == 'MATERIAL':

                if shading.type == 'SOLID':
                    row.prop(
                        context.space_data.shading,
                        "color_type",
                        text="",
                        expand=False
                    )
                    # op = row.operator("wm.context_cycle_enum", text=label)
                    # op.data_path = shade_mode
                    # op.wrap = True

                    if (shading.color_type == 'OBJECT'):
                        row.prop(
                            context.object,
                            'color',
                            text="",
                        )
                    elif (shading.color_type == 'SINGLE'):
                        row.prop(
                            shading,
                            "single_color",
                            text="")
                    elif (shading.color_type == 'MATERIAL'
                            and active_obj.type == 'MESH'):
                        if active_obj.active_material:
                            row.prop(
                                active_obj.active_material,
                                "diffuse_color",
                                text=""
                            )
                            row.template_search(
                                active_obj, "active_material",
                                context.blend_data, "materials")

                            # row.prop_search(
                            #     active_obj, "active_material",
                            #     context.blend_data, "materials",
                            #     text=" ")
                        else:
                            row.template_ID(
                                active_obj,
                                "active_material",
                                # new="material.new"
                            )
                            row.prop_search(
                                active_obj, "active_material",
                                context.blend_data, "materials",
                                text=" ")

                            # row.operator(
                            #     "material.new",
                            #     text="",
                            #     icon='PLUS'
                            # )

                # if shading.type == ('SOLID' or 'WIREFRAME'):
                #     op = row.operator("wm.context_toggle_enum", text=label)
                #     op.data_path = shade_mode
                #     op.value_1 = 'SINGLE'
                #     op.value_2 = 'OBJECT'

                #     row.prop(
                #         context.object,
                #         'color',
                #         text="",
                #     )

                ocol.label(text="Show:")
                y_scale_1 = 0.8
                row = ocol.row(align=True)
                row.scale_y = y_scale_1
                row.prop(
                    context.object,
                    'show_name',
                    text="Name",
                    toggle=True
                )
                row.prop(
                    context.object,
                    "show_wire",
                    text="Wires",
                    toggle=True
                )
                row.prop(
                    context.object,
                    "show_in_front",
                    text="Clip",
                    toggle=True,
                    invert_checkbox=True
                )
                row.prop(
                    context.object,
                    "show_axis",
                    text="Axis",
                    toggle=True
                )

                row = ocol.row(align=True)
                row.scale_y = y_scale_1
                row.prop(
                    context.object,
                    'show_bounds',
                    text="Bounds",
                    toggle=True,
                )
                row.prop(
                    context.object,
                    'display_bounds_type',
                    text="",
                )

                row = ocol.row(align=True)
                row.scale_y = y_scale_1
                row.prop(
                    context.object,
                    'show_texture_space',
                    text="Texture Space",
                    toggle=True,
                )
                row.prop(
                    context.object.display,
                    'show_shadows',
                    text="Shadows",
                    toggle=True,
                )

                # Measures Row
                # label_row = ocol.row(align=True)
                # label_row.label(text="Measures:")

                # row = ocol.row(align=True)

                # row.prop(
                #     overlay,
                #     "show_extra_edge_length",
                #     text=" ",
                #     icon='EDGESEL',
                #     toggle=True
                # )
                # row.prop(
                #     overlay,
                #     "show_extra_edge_angle",
                #     text=" ",
                #     icon='DRIVER_ROTATIONAL_DIFFERENCE',
                #     toggle=True
                # )
                # row.prop(
                #     overlay,
                #     "show_extra_face_area",
                #     text=" ",
                #     icon='FACESEL',
                #     toggle=True
                # )
                # row.prop(
                #     overlay,
                #     "show_extra_face_angle",
                #     text=" ",
                #     icon='LIGHT_AREA',
                #     toggle=True
                # )

                label_row = ocol.row(align=True)

                label_row.label(text="Vertex Groups")

                # Yoinked from properties_data_mesh.py

                group = active_obj.vertex_groups.active

                rows = 4
                if group:
                    rows = 4

                obj_collection = context.view_layer.objects

                row = ocol.row(align=True)

                row.template_list(
                                "MESH_UL_vgroups",
                                "",
                                active_obj,
                                "vertex_groups",
                                active_obj.vertex_groups,
                                "active_index",
                                rows=rows
                                )

                col = row.column(align=True)
                _row = col.row(align=True)
                _row.menu("MESH_MT_vertex_group_context_menu", icon='PROPERTIES', text="")

                _col = col.column(align=True)

                _col.operator("object.vertex_group_add", icon='ADD', text="")

                _col = col.column(align=True)
                _col.active = (True if group else False)
                querb = False

                props = _col.operator("object.vertex_group_remove", icon='REMOVE', text="")
                props.all_unlocked = props.all = False

                _col.operator(
                    "object.vertex_group_move",
                    icon='TRIA_UP',
                    text=""
                    ).direction = 'UP'
                _col.operator(
                    "object.vertex_group_move",
                    icon='TRIA_DOWN',
                    text=""
                    ).direction = 'DOWN'

                if (
                        active_obj.vertex_groups and
                        (
                            active_obj.mode == 'EDIT' or
                                                         (
                                                             active_obj.mode == 'WEIGHT_PAINT'
                                                             and active_obj.type == 'MESH'
                                                             and active_obj.data.use_paint_mask_vertex
                                                         )
                        )
                ):
                    querb = True

                ocol.separator(factor=0.5)
                row = ocol.row(align=True)
                row.active = querb

                row_width_check = check_width('UI', 9, 1, 440)

                label_tog = 0
                if not row_width_check[0]:
                    label_tog = 1

                row_labels = [
                            ("Assign", " "),
                            ("Remove", " "),
                            ("Select", " "),
                            ("Deselect", " "),
                ]

                row_icons = [
                            ('NONE', 'ADD'),
                            ('NONE', 'REMOVE'),
                            ('NONE', 'RESTRICT_SELECT_OFF'),
                            ('NONE', 'RESTRICT_SELECT_ON'),
                ]

                sub = row.row(align=True)
                sub.operator(
                            "object.vertex_group_assign",
                            text=row_labels[0][label_tog],
                            icon=row_icons[0][label_tog]
                            )
                sub.operator(
                            "object.vertex_group_remove_from",
                            text=row_labels[1][label_tog],
                            icon=row_icons[1][label_tog]
                            )

                sub = row.row(align=True)
                sub.operator(
                            "object.vertex_group_select",
                            text=row_labels[2][label_tog],
                            icon=row_icons[2][label_tog]
                            )
                sub.operator(
                            "object.vertex_group_deselect",
                            text=row_labels[3][label_tog],
                            icon=row_icons[3][label_tog]
                            )

                row = ocol.row(align=True)
                row.active = querb

                row.prop(context.tool_settings, "vertex_group_weight", text="Weight")

                row = ocol.row(align=True)
                row.label(text="Parent")

                # Parenting Info
                row = ocol.split(factor=0.65, align=True)
                # row.use_property_split = True
                row.prop(active_obj, 'parent', text="")
                subrow = row.row(align=True)
                subrow.prop(active_obj, 'parent_type', text="")
                subrow.prop(tabs, 'activeObjectPanel_Toggles', index=1, text="", icon='DOWNARROW_HLT')

                if active_obj and active_obj.parent:
                    if tabs.activeObjectPanel_Toggles[1]:
                        section = ocol.column(align=True)
                        row = section.row(align=True)
                        row.operator("object.select_more", text="Family")
                        row.operator("object.select_grouped", text="Siblings").type = 'SIBLINGS'
                        # row.operator("object.collection_objects_select", text="Collection")
                        row = section.column(align=True)
                        # row.prop(active_obj.parent, 'location', text="")

                ocol.label(text="Data")

                row = ocol.row(align=True)
                if active_obj is not None and active_obj.type == 'MESH':
                    obj_data = active_obj.data
                    row.prop(obj_data, "use_customdata_edge_bevel", text="Store Bevel")
                    row.prop(obj_data, "use_customdata_edge_crease", text="Store Crease")
                # row.prop()

                ocol.label(text="Visibility")

                row_width_check = check_width('UI', 12, 1, 440)

                row_labels = [
                            ("Viewport", ""),
                            ("Render", ""),
                            ("Selection", ""),
                            ("Overlays", ""),
                ]

                label_tog = 0
                row_cols = 3
                if not row_width_check[0]:
                    label_tog = 1

                row = ocol.grid_flow(columns=row_cols, align=True)

                row.prop(
                    context.object,
                    'hide_viewport',
                    text=row_labels[0][label_tog],
                    toggle=True,
                )
                row.prop(
                    context.object,
                    'hide_render',
                    text=row_labels[1][label_tog],
                    toggle=True,
                )
                row.prop(
                    context.object,
                    'hide_select',
                    text=row_labels[2][label_tog],
                    toggle=True,
                )

            elif active_obj and active_obj.type == 'CURVE':
                curve = active_obj.data
                act_spline = curve.splines.active
                # is_surf = type(curve) is SurfaceCurve
                # is_poly = (act_spline.type == 'POLY')

                if act_spline.type == 'BEZIER':

                    active_point = 0

                    for cp in act_spline.bezier_points:
                        if cp.select_control_point:
                            active_point = cp

                    if active_point:
                        ocol.label(text="Active Point:")
                        row = ocol.row(align=True)
                        col = row.column(align=True)
                        col.prop(
                            active_point,
                            'radius')

                    if active_point:
                        col.prop(
                            active_point,
                            'tilt')

                ocol.label(text="Curve Geometry:")

                row = ocol.row(align=True)
                col = row.column(align=True)

                col.prop(
                    context.object.data,
                    'resolution_u',
                    text="U Resolution",
                )
                col.prop(
                    context.object.data,
                    'offset',
                    text="Offset",
                )
                col.prop(
                    context.object.data,
                    'extrude',
                    text="Extrude",
                )

                subrow = col.split(factor=0.65, align=True)
                subrow.prop(
                    context.object.data,
                    'twist_smooth',
                    text="Smooth",
                )
                subrow.prop(
                    context.object.data,
                    'twist_mode',
                    text="",
                )

                subrow = col.split(factor=0.65, align=True)
                subrow.prop(
                    context.object.data,
                    'taper_object',
                    text="",
                )
                subrow.prop(
                    context.object.data,
                    'use_map_taper',
                    text="Map Taper",
                    toggle=True
                )

                ocol.label(text="Bevel")

                row = ocol.row(align=True)
                col = row.column(align=True)

                col.prop(
                    context.object.data,
                    'bevel_depth',
                    text="Bevel Depth",
                )
                col.prop(
                    context.object.data,
                    'bevel_resolution',
                    text="Bevel Segments",
                )

                subrow = col.split(factor=0.65, align=True)
                subrow.prop(
                    context.object.data,
                    'bevel_factor_start',
                    text="Bevel Start",
                )
                subrow.prop(
                    context.object.data,
                    'bevel_factor_mapping_start',
                    text="",
                )

                subrow = col.split(factor=0.65, align=True)
                subrow.prop(
                    context.object.data,
                    'bevel_factor_end',
                    text="Bevel End",
                    expand=True
                )
                subrow.prop(
                    context.object.data,
                    'bevel_factor_mapping_end',
                    text="",
                )

                subrow = col.split(factor=0.65, align=True)
                subrow.prop(
                    context.object.data,
                    'bevel_object',
                    text="",
                )
                subrow.prop(
                    context.object.data,
                    'use_fill_caps',
                    text="Fill Caps",
                    toggle=True
                )

                ocol.label(text="Spline Settings")

                row = ocol.row(align=True)
                # row.alignment='CENTER'
                col = row.column(align=True)
                col.alignment = 'EXPAND'

                subrow = col.row(align=True)
                # subrow.alignment = 'CENTER'
                subrow.prop(
                    context.object.data,
                    'fill_mode',
                    text="Fill",
                )

                col.prop(
                    act_spline,
                    'tilt_interpolation',
                    text="Tilt",
                )
                col.prop(
                    act_spline,
                    'radius_interpolation',
                    text="Radius",
                )

                ocol.separator()

                row = ocol.row(align=True)
                row.scale_y = 0.75
                row.prop(
                    act_spline,
                    'use_cyclic_u',
                    text="Cyclic",
                    toggle=True,
                )
                row.prop(
                    act_spline,
                    'use_smooth',
                    text="Smooth",
                    toggle=True,
                )
                row.prop(
                    context.object.data,
                    'use_radius',
                    text="Radius",
                    toggle=True,
                )
                row.prop(
                    context.object.data,
                    'use_stretch',
                    text="Stretch",
                    toggle=True,
                )

                row = ocol.row(align=True)
                row.scale_y = 0.75
                row.prop(
                    context.object.data,
                    'use_deform_bounds',
                    text="Clamp Bounds",
                    toggle=True,
                )
                row.prop(
                    context.object.data,
                    'use_fill_deform',
                    text="Fill Deformed",
                    toggle=True,
                )

            elif active_obj and active_obj.type == 'LATTICE':
                ocol.label(text="Resolution:")

                row = ocol.row(align=True)
                row.prop(
                    active_obj.data,
                    'points_u')
                row.prop(
                    active_obj.data,
                    'interpolation_type_u',
                    text="")

                row = ocol.row(align=True)
                row.prop(
                    active_obj.data,
                    'points_v')
                row.prop(
                    active_obj.data,
                    'interpolation_type_v',
                    text="")

                row = ocol.row(align=True)
                row.prop(
                    active_obj.data,
                    'points_w')
                row.prop(
                    active_obj.data,
                    'interpolation_type_w',
                    text="")

                ocol.separator()

                label_row = ocol.row(align=True)

                label_row.label(text="Vertex Groups")

                # Yoinked from properties_data_mesh.py

                group = active_obj.vertex_groups.active

                rows = 4
                if group:
                    rows = 4

                obj_collection = context.view_layer.objects

                row = ocol.row(align=True)

                row.template_list(
                                "MESH_UL_vgroups",
                                "",
                                active_obj,
                                "vertex_groups",
                                active_obj.vertex_groups,
                                "active_index",
                                rows=rows
                                )

                col = row.column(align=True)
                _row = col.row(align=True)
                _row.menu("MESH_MT_vertex_group_context_menu", icon='PROPERTIES', text="")

                _col = col.column(align=True)

                _col.operator("object.vertex_group_add", icon='ADD', text="")

                _col = col.column(align=True)
                _col.active = (True if group else False)
                querb = False

                props = _col.operator("object.vertex_group_remove", icon='REMOVE', text="")
                props.all_unlocked = props.all = False

                _col.operator(
                    "object.vertex_group_move",
                    icon='TRIA_UP',
                    text=""
                    ).direction = 'UP'
                _col.operator(
                    "object.vertex_group_move",
                    icon='TRIA_DOWN',
                    text=""
                    ).direction = 'DOWN'

                if (
                        active_obj.vertex_groups and
                        (
                            active_obj.mode == 'EDIT' or
                                                         (
                                                             active_obj.mode == 'WEIGHT_PAINT'
                                                             and active_obj.type == 'MESH'
                                                             and active_obj.data.use_paint_mask_vertex
                                                         )
                        )
                ):
                    querb = True

                ocol.separator(factor=0.5)
                row = ocol.row(align=True)
                row.active = querb

                row_width_check = check_width('UI', 9, 1, 440)

                label_tog = 0
                if not row_width_check[0]:
                    label_tog = 1

                row_labels = [
                            ("Assign", " "),
                            ("Remove", " "),
                            ("Select", " "),
                            ("Deselect", " "),
                ]

                row_icons = [
                            ('NONE', 'ADD'),
                            ('NONE', 'REMOVE'),
                            ('NONE', 'RESTRICT_SELECT_OFF'),
                            ('NONE', 'RESTRICT_SELECT_ON'),
                ]

                sub = row.row(align=True)
                sub.operator(
                            "object.vertex_group_assign",
                            text=row_labels[0][label_tog],
                            icon=row_icons[0][label_tog]
                            )
                sub.operator(
                            "object.vertex_group_remove_from",
                            text=row_labels[1][label_tog],
                            icon=row_icons[1][label_tog]
                            )

                sub = row.row(align=True)
                sub.operator(
                            "object.vertex_group_select",
                            text=row_labels[2][label_tog],
                            icon=row_icons[2][label_tog]
                            )
                sub.operator(
                            "object.vertex_group_deselect",
                            text=row_labels[3][label_tog],
                            icon=row_icons[3][label_tog]
                            )

                row = ocol.row(align=True)
                row.active = querb

                row.prop(context.tool_settings, "vertex_group_weight", text="Weight")

                ocol.separator()
                row = ocol.row(align=True)
                row.prop(active_obj.data, "use_outside")

            elif active_obj and active_obj.type == 'EMPTY':
                ocol.label(text="Show:")
                row = ocol.row(align=True)
                row.prop(
                    context.object,
                    'empty_display_type',
                    text="",
                    expand=False
                )
                row.prop(
                    context.object,
                    'parent',
                    text="",
                )

                row = ocol.split(factor=0.5, align=True)
                row.prop(
                    context.object,
                    'empty_display_size',
                    text="",
                    expand=False
                )

                row_inner = row.row(align=True)

                row_inner.prop(
                    context.object,
                    'show_name',
                    text="Name",
                    toggle=True
                )
                row_inner.prop(
                    context.object,
                    'show_axis',
                    text="Axis",
                    toggle=True
                )

                if active_obj.empty_display_type == 'IMAGE':
                    row = ocol.split(factor=0.5, align=True)
                    row.prop(
                        context.object,
                        'use_empty_image_alpha',
                        text="Use Alpha",
                        toggle=True
                    )
                    row.prop(
                        context.object,
                        'color',
                        text="",
                        index=3,
                        slider=True
                    )

                    col = ocol.column(align=True)
                    col.template_ID_preview(
                                   context.object,
                                   "data",
                                   open="image.open",
                                   unlink="object.unlink_data",
                                   hide_buttons=False
                                   )
                    ocol.separator(factor=2)
                    col = ocol.column(align=True)
                    col.template_image(
                                      context.object,
                                      "data",
                                      context.object.image_user,
                                      compact=True,
                                      )

                    row = ocol.row(align=True)

                    sub = row.column(align=True)
                    sub.label(text="Offset:")
                    sub.prop(context.object, "empty_image_offset", text="X", index=0)
                    sub.prop(context.object, "empty_image_offset", text="Y", index=1)

                    row = ocol.split(factor=0.5, align=True)
                    sub = row.column(align=True)

                    sub.label(text="Depth:")
                    sub.prop(context.object, "empty_image_depth", text="", expand=False)

                    sub = row.column(align=True)
                    sub.label(text="Side:")
                    sub.prop(context.object, "empty_image_side", text="", expand=False)

                    col = ocol.column(align=True)
                    col.label(text="Options")
                    col.prop(
                            context.object,
                            "show_empty_image_orthographic",
                            text="Display Orthographic"
                            )
                    col.prop(
                            context.object,
                            "show_empty_image_perspective",
                            text="Display Perspective"
                            )
                    col.prop(context.object, "show_empty_image_only_axis_aligned")

            elif active_obj and active_obj.type == 'CAMERA':

                ocol.label(text="Show:")

                row = ocol.row(align=True)
                row.prop(
                    context.object.data,
                    'show_limits',
                    text="Limits",
                    toggle=True
                )
                row.prop(
                    context.object.data,
                    'show_mist',
                    text="Mist",
                    toggle=True
                )
                row.prop(
                    context.object.data,
                    'show_sensor',
                    text="Sensor",
                    toggle=True
                )
                row.prop(
                    context.object.data,
                    'show_name',
                    text="Name",
                    toggle=True
                )

                row = ocol.row(align=True)
                row.prop(
                    context.object.data,
                    'display_size',
                    text="Display Size",
                )

                ocol.label(text="Settings:")

                col = ocol.column(align=True)

                sub = col.row(align=True)

                if context.object.data.sensor_fit == 'AUTO':
                    sub.prop(
                        context.object.data,
                        'sensor_width',
                        text="Sensor Size",
                    )
                elif context.object.data.sensor_fit == 'HORIZONTAL':
                    sub.prop(
                        context.object.data,
                        'sensor_width',
                        text="Sensor Width",
                    )
                elif context.object.data.sensor_fit == 'VERTICAL':
                    sub.prop(
                        context.object.data,
                        'sensor_height',
                        text="Sensor Height",
                    )

                op = sub.operator(
                    "wm.context_cycle_enum",
                    text="",
                    icon='CON_SIZELIKE'
                )
                op.data_path = "object.data.sensor_fit"
                op.wrap = True

                sub = col.row(align=True)

                if context.object.data.lens_unit == 'MILLIMETERS':
                    sub.prop(
                        context.object.data,
                        'lens',
                    )
                else:
                    sub.prop(
                        context.object.data,
                        'angle',
                    )

                op = sub.operator(
                    "wm.context_toggle_enum",
                    text="",
                    icon='OUTLINER_OB_CAMERA'
                )
                op.data_path = "object.data.lens_unit"
                op.value_1 = 'FOV'
                op.value_2 = 'MILLIMETERS'

                col = ocol.column(align=True)
                sub = col.row(align=True)

                sub.prop(
                    context.object.data,
                    'clip_start'
                )

                sub.prop(
                    context.object.data,
                    'clip_end'
                )

                ocol.label(text="Stuffs:")

                col = ocol.column(align=True)
                sub = col.row(align=True)

                sub.prop(
                    context.space_data,
                    'lock_camera',
                    toggle=True
                )

                sub = col.row(align=True)
                sub.prop(
                    context.object.data,
                    'show_passepartout',
                    text="Dim Outer",
                    toggle=True
                )
                sub.prop(
                    context.object.data,
                    'passepartout_alpha',
                    text="",
                )

                # ocol.separator()

                col = ocol.column(align=True)
                col.scale_y = 0.75
                col.prop(
                    context.object,
                    'location',
                )

                ocol.label(text="Overlays:")

                col = ocol.column(align=True)
                sub = col.row(align=True)

                sub.prop(
                    context.object.data,
                    'show_composition_thirds',
                    text="Thirds",
                    toggle=True
                )
                sub.prop(
                    context.object.data,
                    'show_composition_center',
                    text="Center",
                    toggle=True
                )
                sub.prop(
                    context.object.data,
                    'show_composition_golden',
                    text="Phi",
                    toggle=True
                )

                # RETURN HERE

                ocol.label(text="Scene Cameras:")

                for cam in bpy.data.cameras:
                    if cam.users > 0:
                        row = ocol.row(align=True)
                        row.prop(
                            cam,
                            "name",
                            text=""
                            )

                        if context.scene.camera and context.scene.camera.name == cam.name:
                            icon = 'OUTLINER_OB_CAMERA'
                        else:
                            icon = 'OUTLINER_DATA_CAMERA'

                        op = row.operator(
                            "wm.context_set_id",
                            text="",
                            icon=icon
                        )
                        op.data_path = "scene.camera"
                        op.value = str(cam.name)

                        op = row.operator(
                            "atb.zoop",
                            text="",
                            icon='LIGHT'
                        )
                        op.target_camera = str(cam.name)

            elif active_obj and active_obj.type == 'LIGHT':
                ocol.label(text="Show:")
                row = ocol.row(align=True)
                row.prop(
                    context.object,
                    'show_name',
                    text="Name",
                    toggle=True
                )
                row.prop(
                    context.object,
                    "show_in_front",
                    text="Clip",
                    toggle=True,
                    invert_checkbox=True
                )
                row.prop(
                    context.object,
                    "show_axis",
                    text="Axis",
                    toggle=True
                )

                ocol.label(text="Settings")
                row = ocol.row(align=True)
                row.prop(context.object.data, "type", expand=True)

                row = ocol.split(factor=0.75, align=True)
                row.prop(context.object.data, "energy", expand=False)
                row.prop(context.object.data, "color", text="", expand=False)

                row = ocol.row(align=True)
                row.prop(context.object.data, "specular_factor", text="Specular", expand=False)

                if context.object.data.type == 'POINT' or context.object.data.type == 'SPOT':
                    row.prop(context.object.data, "shadow_soft_size", text="Radius", expand=False)
                elif context.object.data.type == 'SUN':
                    row.prop(context.object.data, "angle", text="Angle", expand=False)
                elif context.object.data.type == 'AREA':
                    row.prop(context.object.data, "shape", text="", expand=False)

                if context.object.data.type == 'SPOT':
                    ocol.separator()

                    row = ocol.split(align=True)

                    sub = row.row(align=True)
                    sub.prop(context.object.data, "show_cone", text="", icon='LIGHT_SPOT')
                    sub.prop(context.object.data, "spot_size", text="Size", expand=False)

                    sub = row.row(align=True)
                    sub.prop(context.object.data, "spot_blend", text="Blend", expand=False)
                elif context.object.data.type == 'AREA':
                    ocol.separator()
                    row = ocol.row(align=True)
                    row.prop(context.object.data, "size", text="X", expand=False)
                    if not context.object.data.shape == 'DISK':
                        row.prop(context.object.data, "size_y", text="Y", expand=False)

                ocol.label(text="Shadows")

                row = ocol.row(align=True)

                col = row.column(align=True)

                col.scale_y = 2
                col.prop(
                        context.object.data,
                        "use_shadow",
                        text="",
                        icon='OUTLINER_DATA_LIGHTPROBE'
                        )

                col = row.column(align=True)
                col.active = context.object.data.use_shadow
                col.prop(
                        context.object.data,
                        "shadow_buffer_clip_start",
                        text="Clip Start",
                        )
                col.prop(
                        context.object.data,
                        "shadow_buffer_bias",
                        text="Bias",
                        )

                ocol.label(text="Contact Shadows")

                row = ocol.row(align=True)

                col = row.column(align=True)

                col.active = context.object.data.use_shadow

                col.scale_y = 3

                col.prop(
                        context.object.data,
                        "use_contact_shadow",
                        text="",
                        icon='MOD_PHYSICS'
                        )

                col = row.column(align=True)

                col.active = (
                    context.object.data.use_shadow
                    and context.object.data.use_contact_shadow)

                col.prop(
                        context.object.data,
                        "contact_shadow_distance",
                        text="Distance",
                        )

                col.prop(
                        context.object.data,
                        "contact_shadow_bias",
                        text="Bias",
                        )

                col.prop(
                        context.object.data,
                        "contact_shadow_thickness",
                        text="Thickness",
                        )

                ocol.label(text="Custom Distance")

                row = ocol.row(align=True)

                col = row.column(align=True)

                col.prop(
                        context.object.data,
                        "use_custom_distance",
                        text="",
                        icon='DRIVER_DISTANCE'
                        )

                col = row.column(align=True)

                col.active = context.object.data.use_custom_distance

                col.prop(
                        context.object.data,
                        "cutoff_distance",
                        text="Distance",
                        )

            elif active_obj and active_obj.type == 'LIGHT_PROBE':
                probe = context.object.data
                ocol.label(text="Settings")

                if probe.type == 'GRID':
                    row = ocol.row(align=True)
                    row.prop(
                            probe,
                            "intensity",
                            text="Intensity",
                            )
                    row.prop(
                            probe,
                            "falloff",
                            text="Falloff",
                            )

                    row = ocol.row(align=True)

                    row.prop(
                            probe,
                            "influence_distance",
                            text="Distance",
                            )

                    row = ocol.row(align=True)
                    row.prop(
                            probe,
                            "clip_start",
                            text="Clip Start",
                            )

                    row = ocol.row(align=True)
                    row.prop(
                            probe,
                            "clip_end",
                            text="Clip End",
                            )

                    ocol.label(text="Resolution:")

                    row = ocol.row(align=True)

                    row.prop(
                            probe,
                            "grid_resolution_x",
                            text="X:",
                            )
                    row.prop(
                            probe,
                            "grid_resolution_x",
                            text="Y:",
                            )
                    row.prop(
                            probe,
                            "grid_resolution_x",
                            text="Z:",
                            )
                elif probe.type == 'PLANAR':
                    row = ocol.row(align=True)

                    row.prop(
                            probe,
                            "falloff",
                            text="Falloff",
                            )
                    row.prop(
                            probe,
                            "influence_distance",
                            text="Distance",
                            )

                    row = ocol.row(align=True)

                    row.prop(
                            probe,
                            "clip_start",
                            text="Offset",
                            )
                else:
                    row = ocol.row(align=True)

                    row.prop(
                            probe,
                            "intensity",
                            text="Intensity",
                            )
                    row.prop(
                            probe,
                            "falloff",
                            text="Falloff",
                            )
                    row = ocol.row(align=True)
                    row.prop(
                            probe,
                            "influence_distance",
                            text="Distance",
                            )

                    row = ocol.row(align=True)
                    row.prop(
                            probe,
                            "clip_start",
                            text="Clip Start",
                            )

                    row = ocol.row(align=True)
                    row.prop(
                            probe,
                            "clip_end",
                            text="Clip End",
                            )

                    row = ocol.row(align=True)
                    row.label(text="Custom Paralax")

                    row = ocol.row(align=True)
                    col = row.column(align=True)
                    col.scale_y = 2
                    ico = 'OUTLINER_DATA_LIGHTPROBE'
                    if probe.use_custom_parallax:
                        ico = 'OUTLINER_OB_LIGHTPROBE'

                    col.prop(
                            probe,
                            "use_custom_parallax",
                            text="",
                            icon=ico
                            )

                    col = row.column(align=True)
                    col.active = probe.use_custom_parallax
                    col.prop(
                            probe,
                            "parallax_type",
                            text="",
                            )
                    col.prop(
                            probe,
                            "parallax_distance",
                            text="Radius",
                            )
                ocol.label(text="Visibility:")

                row = ocol.row(align=True)
                row.prop(
                        probe,
                        "visibility_collection",
                        text=""
                        )
                row.prop(probe, "invert_visibility_collection", text="", icon='ARROW_LEFTRIGHT')

                if probe.type == 'GRID':
                    row = ocol.row(align=True)

                    row.prop(
                            probe,
                            "visibility_buffer_bias",
                            text="Bias"
                            )
                    row.prop(
                            probe,
                            "visibility_bleed_bias",
                            text="Bleed"
                            )
                    row = ocol.row(align=True)
                    row.prop(
                            probe,
                            "visibility_blur",
                            text="Blur"
                            )

                ocol.label(text="Display:")

                col = ocol.column_flow(columns=1, align=True)
                col.alignment = 'LEFT'
                ico = ('CHECKBOX_HLT' if probe.show_influence else 'CHECKBOX_DEHLT')
                col.prop(
                        probe,
                        "show_influence",
                        text="Influence",
                        toggle=True,
                        emboss=False,
                        icon=ico
                        )
                ico = ('CHECKBOX_HLT' if probe.show_clip else 'CHECKBOX_DEHLT')
                col.prop(
                        probe,
                        "show_clip",
                        text="Clipping",
                        toggle=True,
                        emboss=False,
                        icon=ico
                        )
                if not (probe.type in {'PLANAR', 'GRID'}):
                    ico = ('CHECKBOX_HLT' if probe.show_parallax else 'CHECKBOX_DEHLT')
                    col.prop(
                            probe,
                            "show_parallax",
                            text="Parallax",
                            toggle=True,
                            emboss=False,
                            icon=ico
                            )

            if active_obj and active_obj.field:
                field = active_obj.field

                dep = (True if not active_obj.field.type == 'NONE' else False)

                bcol.label(text="Physics:")

                row = bcol.row(align=True)

                row.operator(
                            "object.forcefield_toggle",
                            text="Force Field",
                            icon='FORCE_FORCE',
                            depress=dep
                            )

                row.prop(field, "type", text="")

                if field.type == 'NONE':
                    return  # nothing to draw.

                elif field.type == 'GUIDE':
                    col = bcol.column(align=True)
                    col.prop(field, "guide_minimum")
                    col.prop(field, "guide_free")
                    col.prop(field, "falloff_power")
                    col.prop(field, "use_guide_path_add")
                    col.prop(field, "use_guide_path_weight")

                    # col.separator()

                    col = bcol.column(align=True)
                    col.prop(field, "guide_clump_amount", text="Clumping amount")
                    col.prop(field, "guide_clump_shape")
                    col.prop(field, "use_max_distance")

                    sub = col.column(align=True)
                    sub.active = field.use_max_distance
                    sub.prop(field, "distance_max")

                elif field.type == 'TEXTURE':
                    col = bcol.column(align=True)
                    col.prop(field, "texture_mode")

                    col.separator()

                    col.prop(field, "strength")

                    col = bcol.column(align=True)
                    col.prop(field, "texture_nabla")
                    col.prop(field, "use_object_coords")
                    col.prop(field, "use_2d_force")

                elif field.type == 'SMOKE_FLOW':
                    col = bcol.column(align=True)
                    col.prop(field, "strength")
                    col.prop(field, "flow")

                    col = bcol.column(align=True)
                    col.prop(field, "source_object")
                    col.prop(field, "use_smoke_density")
                else:
                    col = bcol.column(align=True)
                    if field.type == 'DRAG':
                        col.prop(field, "linear_drag", text="Linear")
                    else:
                        col.prop(field, "strength")

                    if field.type == 'TURBULENCE':
                        col.prop(field, "size")
                        col.prop(field, "flow")

                    elif field.type == 'HARMONIC':
                        col.prop(field, "harmonic_damping", text="Damping")
                        col.prop(field, "rest_length")

                    elif field.type == 'VORTEX' and field.shape != 'POINT':
                        col.prop(field, "inflow")

                    elif field.type == 'DRAG':
                        col.prop(field, "quadratic_drag", text="Quadratic")

                    else:
                        col.prop(field, "flow")

                    col.prop(field, "apply_to_location", text="Affect Location")
                    col.prop(field, "apply_to_rotation", text="Affect Rotation")

                    col = bcol.column(align=True)
                    sub = col.column(align=True)
                    sub.prop(field, "noise", text="Noise Amount")
                    sub.prop(field, "seed", text="Seed")

                    if field.type == 'TURBULENCE':
                        col.prop(field, "use_global_coords", text="Global")

                    elif field.type == 'HARMONIC':
                        col.prop(field, "use_multiple_springs")

                    if field.type == 'FORCE':
                        col.prop(field, "use_gravity_falloff", text="Gravitation")

                    col.prop(field, "use_absorption")

        footer_row = root.row(align=True)

        footer_row.scale_y = 1
        footer_row.prop(
            tabs,
            "debug",
            text="Debug",
            icon='TOOL_SETTINGS',
            index=0,
            toggle=True
            )
        footer_row.prop(
            tabs,
            "debug",
            text="",
            icon='KEYFRAME_HLT',
            index=1,
            toggle=True
            )
        footer_row.prop(
            tabs,
            "debug",
            text="",
            icon='LAYER_USED',
            index=2,
            toggle=True
            )
        footer_row.prop(
            tabs,
            "debug",
            text="",
            icon='DOT',
            index=3,
            toggle=True
            )

        # footer_col = root.column(align=True)

        # footer_col.template_icon(icon_value=T1, scale=8)
        # footer_col.template_icon(icon_value=T2, scale=8)
        # footer_col.template_icon(icon_value=T4, scale=8)
