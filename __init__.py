# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.types import (
    WindowManager,
    WorkSpace
    )

from bpy.props import (
    PointerProperty
)
# import math

# from .Icons.__init__ import *
# from . Icons import initialize_icons_collection, unload_icons

from . properties import FastPanelProps
from . properties import ObjectMatrixConversions
from . properties import MetaPanelTabs
from . properties import QuickOpMenus
from . properties import ACTWireColors
from . properties import FastSnapProps
from . properties import CustomPopoverProps

from . preferences import ACTAddonPreferences
from . preferences import register_keymaps, unregister_keymaps
from . preferences import get_keys

from .Operators.wrappers import ACT_OT_SetEnum
from .Operators.wrappers import ACT_OT_CycleEnum
from .Operators.wrappers import ACT_OT_ContextOp
from .Operators.wrappers import ACT_OT_MouseContextOp
from .Operators.wrappers import ACT_OT_BoolToEnum
from .Operators.wrappers import ACT_OT_EnhancedSelect
from .Operators.wrappers import ACT_OT_EnhancedTag
from .Operators.wrappers import ACT_OT_GroupSelect
from .Operators.wrappers import ACT_OT_AddToMode
from .Operators.wrappers import ACT_OT_MoveCursor
from .Operators.wrappers import ACT_OT_FastSnap
from .Operators.wrappers import ACT_OT_context_modal_mouse
from .Operators.wrappers import ACT_OT_drop_tool
from .Operators.wrappers import ACT_OT_Set_Custom_Popover
from .Operators.wrappers import ACT_OT_Clear_Custom_Popover

from .Operators.ViewportOps import ACT_OT_ViewAxis
from .Operators.ViewportOps import ACT_OT_set_axis

from .Operators.TransformOperators import ACT_OT_RotateAroundPivot

from .Operators.ThemeOps import ACT_OT_set_color
from .Operators.ThemeOps import ACT_OT_store_wire_color

from .Operators.SelectOps import ACT_OT_SuperContextMenu
from .Operators.SelectOps import ACT_OT_SelectThrough

from .Utilities.GizmoUtils import ACTPrintVerts

from .Gizmos.VertPieGizmo import ATVertexGizmoGroup
from .Gizmos.PivotGizmo import ATPivotGizmoGroup
from .Gizmos.AxisGizmo import AxisGizmo
from .Gizmos.VPCursorGizmo import ATVPCursorGizmo
from .Gizmos.VPCursorGizmo import ATCursorTool

from .UI.MetaPanel import VIEW3D_PT_meta_panel

from .UI.ViewportAppends import popover
# from .UI.ViewportAppends import info_space_buttons
# from .UI.ViewportAppends import custom_popovers

from .UI.ContextPies import VIEW3D_MT_PIE_orbit_lock
from .UI.ContextPies import VIEW3D_MT_PIE_expand_mode
from .UI.ContextPies import VIEW3D_MT_PIE_quick_snap
from .UI.ContextPies import VIEW3D_MT_PIE_quick_orientation

from .UI.ViewPanel import ACT_PT_ViewOverlaysPanel
from .UI.ViewPanel import ACT_MT_MeshShadingMenu
from .UI.ViewPanel import ACT_MT_MiscOverlaysMenu
from .UI.ViewPanel import ACT_PT_viewport_transform_settings
# from .UI.ViewPanel import ACT_PT_quick_operators
from .UI.ViewPanel import ACT_PT_MiscOverlaysPanel

from .UI.FastPanel import VIEW3D_PT_view3d_fast_panel
from .UI.FastPanel import VIEW3D_PT_grid_ribbon
from .UI.FastPanel import VIEW3D_PT_snap_ribbon
from .UI.FastPanel import VIEW3D_PT_draw_ribbon

from .UI.ViewPie import VIEW3D_MT_ACT_view_pie
from .UI.ViewPie import VIEW3D_MT_ACT_cursor_pie
from .UI.ViewPie import VIEW3D_MT_PIE_view_utilities
from .UI.ViewPie import VIEW3D_PT_viewport_rotation_panel

from .UI.EditMenu import VIEW3D_MT_actc_root
from .UI.EditMenu import VIEW3D_MT_actc_sub_edges
from .UI.EditMenu import VIEW3D_MT_actc_sub_operators
from .UI.EditMenu import VIEW3D_MT_actc_sub_select
from .UI.EditMenu import VIEW3D_MT_actc_sub_add
from .UI.EditMenu import VIEW3D_MT_actc_sub_shading

from .UI.ExamplePanel import VIEW3D_PT_view3d_example_panel

bl_info = {
    "name": "ACT",
    "author": "Asher",
    "description": "Asher's Creative Toolset",
    "blender": (2, 83, 0),
    "version": (0, 0, 95),
    "location": "View3D",
    "warning": "Alpha of all Alphas",
    "category": "Modeling"
}


panels = (
        ACT_PT_ViewOverlaysPanel,
        )


def update_panel(self, context):
    message = "Asher's Custom Tools: Panel update has failed"
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        for panel in panels:
            panel.bl_category = context.preferences.addons[__name__].preferences.category
            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass


# class ACTAddonPreferences(bpy.types.AddonPreferences):
#     # this must match the addon name, use '__package__'
#     # when defining this in a submodule of a python package.
#     bl_idname = __name__

#     category: bpy.props.StringProperty(
#             name="Tab Category",
#             description="Choose a name for the category of the panel",
#             default="Dev",
#             update=update_panel
#             )

#     def draw(self, context):
#         layout = self.layout

#         row = layout.row()
#         col = row.column()
#         col.label(text="Tab Category:")
#         col.prop(self, "category", text="")

def debug_keymap():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    print(str(kc.preferences))

    for item in kc.keymaps:
        # print(str(item.name))
        if len(str(item.bl_owner_id)) > 2:
            print(str(item.bl_owner_id)
                  + ": "
                  + str(item.name))
            for entry in item.keymap_items:
                print("      " + str(entry.name))


classes = (
    # ACTAddonPreferences,
    ACTAddonPreferences,
    # wrappers.py
    ACT_OT_SetEnum,
    ACT_OT_CycleEnum,
    ACT_OT_ContextOp,
    ACT_OT_MouseContextOp,
    ACT_OT_BoolToEnum,
    ACT_OT_EnhancedSelect,
    ACT_OT_EnhancedTag,
    ACT_OT_GroupSelect,
    ACT_OT_AddToMode,
    ACT_OT_MoveCursor,
    ACT_OT_FastSnap,
    ACT_OT_context_modal_mouse,
    ACT_OT_drop_tool,
    VIEW3D_MT_PIE_orbit_lock,
    VIEW3D_MT_PIE_expand_mode,
    ACT_OT_Set_Custom_Popover,
    ACT_OT_Clear_Custom_Popover,
    # TransformOperators.py
    ACT_OT_RotateAroundPivot,
    ACT_PT_ViewOverlaysPanel,
    ACT_PT_viewport_transform_settings,
    ACT_MT_MeshShadingMenu,
    ACT_MT_MiscOverlaysMenu,
    # ACT_PT_quick_operators,
    ACT_PT_MiscOverlaysPanel,
    # ThemeOps.py
    ACT_OT_set_color,
    ACT_OT_store_wire_color,
    VIEW3D_PT_view3d_fast_panel,
    VIEW3D_PT_grid_ribbon,
    VIEW3D_PT_snap_ribbon,
    VIEW3D_PT_draw_ribbon,
    ATVertexGizmoGroup,
    ATPivotGizmoGroup,
    VIEW3D_PT_meta_panel,
    ATVPCursorGizmo,
    AxisGizmo,
    # ViewportOps.py
    ACT_OT_ViewAxis,
    ACT_OT_set_axis,
    # SelectOps.py
    ACT_OT_SuperContextMenu,
    ACT_OT_SelectThrough,
    # GizmoUtils.py
    ACTPrintVerts,
    # Pies
    VIEW3D_MT_ACT_view_pie,
    VIEW3D_MT_ACT_cursor_pie,
    VIEW3D_MT_PIE_view_utilities,
    VIEW3D_MT_PIE_quick_snap,
    VIEW3D_MT_PIE_quick_orientation,
    VIEW3D_PT_viewport_rotation_panel,
    # Property Groups
    MetaPanelTabs,
    QuickOpMenus,
    ACTWireColors,
    FastPanelProps,
    ObjectMatrixConversions,
    FastSnapProps,
    CustomPopoverProps,
    # Quick FavoritesMenu
    VIEW3D_MT_actc_root,
    VIEW3D_MT_actc_sub_edges,
    VIEW3D_MT_actc_sub_operators,
    VIEW3D_MT_actc_sub_select,
    VIEW3D_MT_actc_sub_add,
    VIEW3D_MT_actc_sub_shading,
    # Layout Example from ExamplePanel.py,
    VIEW3D_PT_view3d_example_panel
    )


def register():
    prefs = bpy.context.preferences
    for cls in classes:
        bpy.utils.register_class(cls)

    WindowManager.metapanel_tabs = PointerProperty(type=MetaPanelTabs)
    WindowManager.quick_op_menus = PointerProperty(type=QuickOpMenus)
    WindowManager.fp_props = PointerProperty(type=FastPanelProps)
    WindowManager.mat_convert = PointerProperty(type=ObjectMatrixConversions)
    WorkSpace.temp_wires = PointerProperty(type=ACTWireColors)
    WorkSpace.customPops = PointerProperty(type=CustomPopoverProps)

    WindowManager.snap_state = PointerProperty(type=FastSnapProps)

    bpy.types.VIEW3D_HT_header.append(popover)
    # bpy.types.VIEW3D_MT_editor_menus.append(custom_popovers)
    # bpy.types.INFO_HT_header.append(info_space_buttons)
    # bpy.types.PROPERTIES_PT_navigation_bar.append(navbar_extras)

    bpy.utils.register_tool(ATCursorTool)

    global keymaps

    if prefs.addons[__name__].preferences.baseKeymap == 'ASHER':
        keylist = get_keys(dictname="keysdict")
        print("Loading Asher's Keymap")
    elif prefs.addons[__name__].preferences.baseKeymap == 'HUMANS':
        keylist = get_keys(dictname="humankeysdict")
        print("Loading Human Keymap")

    # keylist = get_keys()
    keymaps = register_keymaps(keylist)

    # debug_keymap()


def unregister():
    global keymaps

    unregister_keymaps(keymaps)

    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_HT_header.remove(popover)
    # bpy.types.INFO_HT_header.remove(info_space_buttons)
    # bpy.types.VIEW3D_MT_editor_menus.remove(custom_popovers)
    # bpy.types.PROPERTIES_PT_navigation_bar.remove(navbar_extras)

    bpy.utils.unregister_tool(ATCursorTool)

    del bpy.types.WindowManager.metapanel_tabs
    del bpy.types.WindowManager.quick_op_menus
    del bpy.types.WindowManager.mat_convert
    del bpy.types.WorkSpace.customPops
