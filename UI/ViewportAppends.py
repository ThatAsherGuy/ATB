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
import math


def popover(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.popover(
        "VIEW3D_PT_meta_panel",
        text="",
        icon='OPTIONS'
    )


def custom_popovers(self, context):

    panel_1 = context.workspace.customPops.popover_1
    panel_2 = context.workspace.customPops.popover_2
    panel_3 = context.workspace.customPops.popover_3

    layout = self.layout
    root = layout.row(align=True)

    if panel_1 == "BATMAN":
        root.operator("atb.set_custom_pop", text="", icon='ADD').button = 1
    else:
        root.popover(
            panel_1,
            text="",
            icon='REC'
        )

    if panel_2 == "BATMAN":
        root.operator("atb.set_custom_pop", text="", icon='ADD').button = 2
    else:
        root.popover(
            panel_2,
            text="",
            icon='KEYFRAME_HLT'
        )

    if panel_3 == "BATMAN":
        root.operator("atb.set_custom_pop", text="", icon='ADD').button = 3
    else:
        root.popover(
            panel_3,
            text="",
            icon='OUTLINER_OB_POINTCLOUD'
        )
    root.operator("atb.clear_custom_pop", text="", icon='REMOVE')


def transform_pop(self, context):

    area = bpy.context.area
    resolution = bpy.context.preferences.system.ui_scale

    for reg in area.regions:
        if reg.type == 'HEADER':
            region_width_raw = reg.width

    region_width = region_width_raw - 40
    region_width_int = round(region_width / (20 * resolution))
    region_width_factor = round((region_width_int / 80), 3)

    if region_width_factor > 2:
        region_width_factor = 2

    region_width_factor_quad = round(
                                (1
                                    * math.pow(region_width_factor, 2)
                                    + 1
                                    * region_width_factor),
                                2)

    layout = self.layout
    row = layout.row(align=True)
    row.scale_x = region_width_factor_quad

    row.operator("wm.search_menu", text=str(region_width_factor_quad))


def snap_pop(self, context):
    tool_settings = context.scene.tool_settings

    layout = self.layout
    layout.ui_units_x = 11

    # Snapping Stuff
    root = layout.column(align=True)
    root.scale_y = 1

    snap_box = root.box()

    snap_box_inner_col = snap_box.column(align=True)

    snap_box_inner_row = snap_box_inner_col.column(align=True)

    first_row = snap_box_inner_row.row(align=True)
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
        text=" "
    )
    first_row.prop_enum(
        tool_settings,
        "snap_elements",
        'VERTEX',
        text=" "
    )
    first_row.prop_enum(
        tool_settings,
        "snap_elements",
        'FACE',
        text=" "
    )
    first_row.prop_enum(
        tool_settings,
        "snap_elements",
        'VOLUME',
        text=" "
    )
    first_row.prop_enum(
        tool_settings,
        "snap_elements",
        'EDGE',
        text=" "
    )
    first_row.prop_enum(
        tool_settings,
        "snap_elements",
        'EDGE_MIDPOINT',
        text=" "
    )
    first_row.prop_enum(
        tool_settings,
        "snap_elements",
        'EDGE_PERPENDICULAR',
        text=" "
    )
    first_row.prop(
        tool_settings,
        "snap_target",
        expand=False,
        text="",
        icon='LAYER_ACTIVE'
    )

    second_row = snap_box_inner_row.row(align=True)

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

    third_row = snap_box_inner_row.row(align=True)

    third_row.prop(
        tool_settings,
        "use_snap_rotate",
        text="Affect Rotate",
        toggle=True
    )
    third_row.prop(
        tool_settings,
        "use_snap_translate",
        text="Affect Translate",
        toggle=True
    )
    third_row.prop(
        tool_settings,
        "use_snap_scale",
        text="Affect Scale",
        toggle=True
    )


def context_buttons(self, context):

    layout = self.layout
    main_row = layout.row(align=True)

    area = bpy.context.area
    resolution = bpy.context.preferences.system.ui_scale

    for reg in area.regions:
        if reg.type == 'HEADER':
            region_width_raw = reg.width

    region_width = region_width_raw - 40
    region_width_int = round(region_width / (20 * resolution))
    region_width_factor = round((region_width_int / 80), 3)

    if region_width_factor > 1:
        region_width_factor = 1

    fish = True
    icon_bool = False
    threshold = 40
    if (region_width_int <= threshold) or context.scene.gz_piv_disp_bool:
        fish = False
        if (region_width_int <= (threshold * 0.75)):
            icon_bool = True
        main_row.prop(
            context.scene,
            "gz_piv_enum",
            text="",
            expand=fish,
            icon_only=icon_bool
        )
        if context.scene.gz_piv_disp_bool:
            main_row.prop(
                context.scene,
                "gz_piv_disp_bool",
                text="",
                icon='FULLSCREEN_EXIT'
            )
    else:
        main_row.prop(context.scene, "gz_piv_enum", expand=fish)
        main_row.prop(
            context.scene,
            "gz_piv_disp_bool",
            text="",
            icon='FULLSCREEN_EXIT',
            icon_only=True
        )


def info_space_buttons(self, context):
    area = bpy.context.area
    resolution = bpy.context.preferences.system.ui_scale
    tool_settings = context.scene.tool_settings

    for reg in area.regions:
        if reg.type == 'WINDOW':
            region_height_raw = reg.height

    region_height_int = round(region_height_raw / (20 * resolution))

    layout = self.layout

    if region_height_int < 1:
        row = layout.row(align=True)
        row.prop(
            tool_settings,
            "snap_target",
            expand=False,
            text="",
        )

        first_row = layout.row(align=True)
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


def navbar_extras(self, context):
    layout = self.layout

    wm = bpy.context.window_manager
    metapanel = wm.ATB

    layout.prop_tabs_enum(metapanel, "tab", icon_only=True)
