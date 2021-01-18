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

from .Icons.__init__ import *
from . Icons import initialize_icons_collection, unload_icons

from . properties import FastPanelProps
from . properties import ObjectMatrixConversions
from . properties import MetaPanelTabs
from . properties import QuickOpMenus
from . properties import CustomTransforms
from . properties import ATBWireColors
from . properties import FastSnapProps
from . properties import CustomPopoverProps
from . properties import ModalProps
from . properties import ATB_ObjectProperties
from . properties import ATB_SceneProperties
from . properties import ATB_WorkspaceProperties
from . properties import ATB_WindowProperties

from . preferences import ATBAddonPreferences
from . preferences import register_keymaps, unregister_keymaps
from . preferences import get_keys

from .Operators.wrappers import ATB_OT_SetEnum
from .Operators.wrappers import ATB_OT_CycleEnum
from .Operators.wrappers import ATB_OT_ContextOp
from .Operators.wrappers import ATB_OT_MouseContextOp
from .Operators.wrappers import ATB_OT_BoolToEnum
from .Operators.wrappers import ATB_OT_EnhancedSelect
from .Operators.wrappers import ATB_OT_EnhancedTag
from .Operators.wrappers import ATB_OT_GroupSelect
from .Operators.wrappers import ATB_OT_AddToMode
from .Operators.wrappers import ATB_OT_MoveCursor
from .Operators.wrappers import ATB_OT_FastSnap
from .Operators.wrappers import ATB_OT_context_modal_mouse
from .Operators.wrappers import ATB_OT_drop_tool
from .Operators.wrappers import ATB_OT_Set_Custom_Popover
from .Operators.wrappers import ATB_OT_Clear_Custom_Popover
from .Operators.wrappers import ATB_OT_TogglePhotoMode
from .Operators.wrappers import ATB_OT_Frame_Object
from .Operators.wrappers import ATB_OT_Select_Object
from .Operators.wrappers import ATB_OT_Nuke_Panel
from .Operators.wrappers import ATB_OT_Set_Object_Display
from .Operators.wrappers import ATB_OT_SaveIncremental

from .Operators.CameraOps import ATB_OT_Zoop
from .Operators.CameraOps import ATB_OT_Lock_Camera
from .Operators.CameraOps import ATB_OT_Add_Camera_Keying_Set

from .Operators.ViewportOps import ATB_OT_ViewAxis
from .Operators.ViewportOps import ATB_OT_set_axis

from .Operators.TransformOperators import ATB_OT_RotateAroundPivot
from .Operators.TransformOperators import ATB_OT_CreateNamedOrientation
from .Operators.TransformOperators import ATB_OT_CursorToOrientation
from .Operators.TransformOperators import ATB_OT_SetOrigin
from .Operators.TransformOperators import ATB_OT_SetOriginToBBox
from .Operators.TransformOperators import ATB_OT_QuickSnapOrigin
from .Operators.TransformOperators import ATB_OT_SnapAndAlignCursor

from .Operators.ThemeOps import ATB_OT_set_color
from .Operators.ThemeOps import ATB_OT_store_wire_color

from .Operators.SelectOps import ATB_OT_SuperContextMenu
from .Operators.SelectOps import ATB_OT_SelectThrough
from .Operators.SelectOps import ATB_OT_ProximitySelect

from .Operators.TabletOps import ATB_OT_SuperTabletPie
from .Operators.TabletOps import ATB_OT_RhythmInvoke
from .Operators.TabletOps import ATB_OT_DRAW

from .Operators.MeshOps import ATB_OT_QuickSymmetry

from .Operators.ModifierOps import ATB_OT_AddModifier
from .Operators.ModifierOps import ATB_OT_Modifier_Pie

from .Operators.ObjectOps import ATB_OT_AddBasePlane

from .Operators.SculptOps import ATB_OT_SculptPie

from .Utilities.GizmoUtils import ATBPrintVerts

from .Gizmos.VertPieGizmo import ATVertexGizmoGroup
from .Gizmos.PivotGizmo import ATPivotGizmoGroup
from .Gizmos.AxisGizmo import AxisGizmo
from .Gizmos.VPCursorGizmo import ATVPCursorGizmo
from .Gizmos.VPCursorGizmo import ATCursorTool
from .Gizmos.TabletGizmo import ATB_TabletGizmoGroup
from .Gizmos.MirrorGizmo import ATB_MirrorGizmoGroup
from .Gizmos.PreselectGizmo import ATB_PreselectGizmoGroup

from .UI.MetaPanel import VIEW3D_PT_meta_panel
from .UI.MetaPanel import CUSTOM_UL_camera_list
from .UI.MetaPanel import VIEW3D_MT_set_origin

from .UI.ViewportAppends import popover
# from .UI.ViewportAppends import info_space_buttons
# from .UI.ViewportAppends import custom_popovers

from .UI.ContextPies import VIEW3D_MT_PIE_orbit_lock
from .UI.ContextPies import VIEW3D_MT_PIE_expand_mode
from .UI.ContextPies import VIEW3D_MT_PIE_quick_snap
from .UI.ContextPies import VIEW3D_MT_PIE_quick_orientation
from .UI.ContextPies import ATB_OT_MetaPie
from .UI.ContextPies import ATB_OT_SavePie

from .UI.ViewPanel import ATB_PT_ViewOverlaysPanel
from .UI.ViewPanel import ATB_MT_MeshShadingMenu
from .UI.ViewPanel import ATB_MT_MiscOverlaysMenu
from .UI.ViewPanel import ATB_PT_viewport_transform_settings
# from .UI.ViewPanel import ATB_PT_quick_operators
from .UI.ViewPanel import ATB_PT_MiscOverlaysPanel

from .UI.FastPanel import VIEW3D_PT_view3d_fast_panel

from .UI.ViewPie import VIEW3D_MT_ATB_view_pie
from .UI.ViewPie import VIEW3D_MT_ATB_cursor_pie
from .UI.ViewPie import VIEW3D_MT_PIE_view_utilities
from .UI.ViewPie import VIEW3D_PT_viewport_rotation_panel
from .UI.ViewPie import VIEW3D_PT_viewport_orbit_panel
from .UI.ViewPie import VIEW3D_MT_ATB_tablet_pie
from .UI.ViewPie import VIEW3D_MT_ATB_origin_pie
from .UI.ViewPie import VIEW3D_MT_ATB_camera_pie
from .UI.ViewPie import ATB_OT_EnhancedCameraPie

from .UI.EditMenu import VIEW3D_MT_actc_root
from .UI.EditMenu import VIEW3D_MT_actc_sub_edges
from .UI.EditMenu import VIEW3D_MT_actc_sub_operators
from .UI.EditMenu import VIEW3D_MT_actc_sub_select
from .UI.EditMenu import VIEW3D_MT_actc_sub_add
from .UI.EditMenu import VIEW3D_MT_actc_sub_shading

from .UI.ExamplePanel import VIEW3D_PT_view3d_example_panel

bl_info = {
    "name": "ATB",
    "author": "ThatAsherGuy",
    "description": "Asher's Toolbox",
    "blender": (2, 83, 0),
    "version": (0, 0, 65),
    "location": "View3D",
    "warning": "Alpha of all Alphas",
    "category": "Modeling"
}

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
    # ATBAddonPreferences,
    ATBAddonPreferences,
    # wrappers.py
    ATB_OT_SetEnum,
    ATB_OT_CycleEnum,
    ATB_OT_ContextOp,
    ATB_OT_MouseContextOp,
    ATB_OT_BoolToEnum,
    ATB_OT_EnhancedSelect,
    ATB_OT_EnhancedTag,
    ATB_OT_GroupSelect,
    ATB_OT_AddToMode,
    ATB_OT_MoveCursor,
    ATB_OT_FastSnap,
    ATB_OT_context_modal_mouse,
    ATB_OT_drop_tool,
    VIEW3D_MT_PIE_orbit_lock,
    VIEW3D_MT_PIE_expand_mode,
    ATB_OT_Set_Custom_Popover,
    ATB_OT_Clear_Custom_Popover,
    ATB_OT_TogglePhotoMode,
    ATB_OT_Frame_Object,
    ATB_OT_Select_Object,
    ATB_OT_Nuke_Panel,
    ATB_OT_Set_Object_Display,
    ATB_OT_SaveIncremental,
    # CameraOps.py,
    ATB_OT_Zoop,
    ATB_OT_Lock_Camera,
    ATB_OT_Add_Camera_Keying_Set,
    # TransformOperators.py
    ATB_OT_RotateAroundPivot,
    ATB_OT_CreateNamedOrientation,
    ATB_OT_CursorToOrientation,
    ATB_OT_SetOrigin,
    ATB_OT_SetOriginToBBox,
    ATB_OT_QuickSnapOrigin,
    ATB_OT_SnapAndAlignCursor,
    # Other Stuff
    ATB_PT_ViewOverlaysPanel,
    ATB_PT_viewport_transform_settings,
    ATB_MT_MeshShadingMenu,
    ATB_MT_MiscOverlaysMenu,
    # ATB_PT_quick_operators,
    ATB_PT_MiscOverlaysPanel,
    # ThemeOps.py
    ATB_OT_set_color,
    ATB_OT_store_wire_color,
    VIEW3D_PT_view3d_fast_panel,
    ATVertexGizmoGroup,
    ATPivotGizmoGroup,
    # MetaPanel.py
    VIEW3D_PT_meta_panel,
    VIEW3D_MT_set_origin,
    CUSTOM_UL_camera_list,
    # Gizmos
    ATVPCursorGizmo,
    AxisGizmo,
    ATB_TabletGizmoGroup,
    ATB_MirrorGizmoGroup,
    ATB_PreselectGizmoGroup,
    # ViewportOps.py
    ATB_OT_ViewAxis,
    ATB_OT_set_axis,
    # SelectOps.py
    ATB_OT_SuperContextMenu,
    ATB_OT_SelectThrough,
    ATB_OT_ProximitySelect,
    # TabletOps.py
    ATB_OT_SuperTabletPie,
    ATB_OT_RhythmInvoke,
    ATB_OT_DRAW,
    # Mesh Ops
    ATB_OT_QuickSymmetry,
    # Object Ops
    ATB_OT_AddBasePlane,
    # Modifier Ops
    ATB_OT_AddModifier,
    ATB_OT_Modifier_Pie,
    # Sculpt Ops
    ATB_OT_SculptPie,
    # GizmoUtils.py
    ATBPrintVerts,
    # Pies
    VIEW3D_MT_ATB_view_pie,
    VIEW3D_MT_ATB_cursor_pie,
    VIEW3D_MT_PIE_view_utilities,
    VIEW3D_MT_PIE_quick_snap,
    VIEW3D_MT_PIE_quick_orientation,
    VIEW3D_MT_ATB_tablet_pie,
    VIEW3D_MT_ATB_origin_pie,
    VIEW3D_MT_ATB_camera_pie,
    ATB_OT_EnhancedCameraPie,
    VIEW3D_PT_viewport_rotation_panel,
    VIEW3D_PT_viewport_orbit_panel,
    ATB_OT_MetaPie,
    ATB_OT_SavePie,
    # Property Groups
    MetaPanelTabs,
    QuickOpMenus,
    CustomTransforms,
    ATBWireColors,
    FastPanelProps,
    ObjectMatrixConversions,
    FastSnapProps,
    CustomPopoverProps,
    ModalProps,
    ATB_ObjectProperties,
    ATB_SceneProperties,
    ATB_WorkspaceProperties,
    ATB_WindowProperties,
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


    WorkSpace.custom_transforms = PointerProperty(type=CustomTransforms)
    WorkSpace.temp_wires = PointerProperty(type=ATBWireColors)
    WorkSpace.customPops = PointerProperty(type=CustomPopoverProps)

    # Currently working to unify my properties
    bpy.types.Object.ATB = PointerProperty(type=ATB_ObjectProperties)
    bpy.types.Scene.ATB = PointerProperty(type=ATB_SceneProperties)
    WindowManager.ATB = PointerProperty(type=ATB_WindowProperties)
    WorkSpace.ATB = PointerProperty(type=ATB_WorkspaceProperties)

    WorkSpace.modals = PointerProperty(type=ModalProps)

    WindowManager.snap_state = PointerProperty(type=FastSnapProps)

    bpy.types.VIEW3D_HT_header.append(popover)

    bpy.utils.register_tool(ATCursorTool)

    global keymaps

    if prefs.addons[__name__].preferences.baseKeymap == 'ASHER':
        keylist = get_keys(dictname="keysdict")
        print("Loading Asher's Keymap")
    elif prefs.addons[__name__].preferences.baseKeymap == 'HUMANS':
        keylist = get_keys(dictname="humankeysdict")
        print("Loading Human Keymap")
    else:
        keylist = get_keys(dictname="keysdict")
        print("Loading Backup Keymap")

    keymaps = register_keymaps(keylist)

def unregister():
    global keymaps

    unregister_keymaps(keymaps)

    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_HT_header.remove(popover)

    bpy.utils.unregister_tool(ATCursorTool)

    del bpy.types.WorkSpace.customPops

    # Newer unified properties setup
    del bpy.types.Scene.ATB
    del bpy.types.Object.ATB
    del bpy.types.WorkSpace.ATB
    del bpy.types.WindowManager.ATB