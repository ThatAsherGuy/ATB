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
from bpy.types import PropertyGroup
from mathutils import Matrix
from bpy.props import (
    EnumProperty,
    FloatVectorProperty,
    BoolProperty,
    BoolVectorProperty,
    IntProperty,
    StringProperty,
    PointerProperty
)
# import math

# Root Properties


class ModalProps(PropertyGroup):
    tablet_modal: BoolProperty(
                                name="Layout Toggle",
                                default=False
                             )

    edit_modal: BoolProperty(
                                name="Pivot Toggle",
                                default=False
                            )

    transform_modal: BoolProperty(
                                name="Snapping Toggle",
                                default=False
                           )

    mirror_modal: BoolProperty(
                                name="Mirror Modal",
                                default=False
                           )

    mm_use_cursor: BoolProperty(
                                name="Mirror Modal",
                                default=False
                           )

    mm_use_cursor_location: BoolProperty(
                                name="Mirror Modal",
                                default=False
                           )


# Fast Panel Stuff

class FastPanelProps(PropertyGroup):
    layout_bool: BoolProperty(
                                name="Layout Toggle",
                                default=False
                             )

    pivot_bool: BoolProperty(
                                name="Pivot Toggle",
                                default=False
                            )

    snap_bool: BoolProperty(
                                name="Snapping Toggle",
                                default=False
                           )

    snap_cycle_items = [
                    ('MIN', "Minimal", "Minimal", 'NONE', 1),
                    ('COMPACT', "Compact", "Compact", 'NONE', 2),
                    ('FULL', "Full", "Full", 'NONE', 3)
                 ]

    snap_cycle: EnumProperty(
        name=' ',
        description='Snap Section Layout',
        items=snap_cycle_items
    )

    fast_panel_tab_items = [
                ('MEASURES', "Measures", "Measurement Tools and Overlays", 'DESKTOP', 1),
                ('OVERLAYS', "Overlays", "Viewport Overlays", 'SEQ_STRIP_DUPLICATE', 2),
                ('NORMALS', "Normals", "Mesh Normal Overlays", 'SNAP_FACE_CENTER', 3),
                ('GIZMOS', "Gizmos", "Gizmo Options", 'CON_OBJECTSOLVER', 4),
                ('DISPLAY', "Display", "Object Display Options", 'RIGID_BODY_CONSTRAINT', 5)
                           ]

    fast_panel_tabs: EnumProperty(
        name=' ',
        description='Fast Panel Tab',
        items=fast_panel_tab_items
    )

# TODO: The hell is this formatting?

# Quick Transforms Stuff
bpy.types.Scene.snap_cycle = bpy.props.IntProperty(
                                                   name="Snapping Toggle",
                                                   default=0,
                                                   min=0,
                                                   max=2)

# Context Gizmo Stuff
bpy.types.Scene.cp_mode_enum = bpy.props.EnumProperty(
                                                   items=[
                                                        (
                                                            '0',
                                                            "Vertex Operators",
                                                            "First Mode",
                                                            'VERTEXSEL',
                                                            1
                                                        ),
                                                        (
                                                            '1',
                                                            "Edge Operators",
                                                            "Second Mode",
                                                            'EDITMODE_HLT',
                                                            2
                                                        ),
                                                        (
                                                            '2',
                                                            "Select",
                                                            "Third Mode",
                                                            'EDITMODE_HLT',
                                                            3
                                                        ),
                                                        (
                                                            '3',
                                                            "Transform",
                                                            "Fourth Mode",
                                                            'OBJECT_ORIGIN',
                                                            4
                                                        )],
                                                   name="Context Pie Mode",
                                                   default='0',
                                                   )
bpy.types.Scene.gz_piv_enum = bpy.props.EnumProperty(
                                                   items=[
                                                        (
                                                            '0',
                                                            "Active",
                                                            "First Mode",
                                                            'PIVOT_ACTIVE',
                                                            1
                                                        ),
                                                        (
                                                            '1',
                                                            "Origin",
                                                            "Second Mode",
                                                            'OBJECT_ORIGIN',
                                                            2
                                                        ),
                                                        (
                                                            '2',
                                                            "Cursor",
                                                            "Third Mode",
                                                            'PIVOT_CURSOR',
                                                            3
                                                        )],
                                                   name="Gizmo Pivot Mode",
                                                   default='0',
                                                   )


bpy.types.Scene.gz_piv_disp_bool = bpy.props.BoolProperty(
                                                  name="pgz_disp_bool",
                                                  default=False)
bpy.types.Scene.gz_scale = bpy.props.FloatProperty(
                                                  name="Gizmo Scale",
                                                  min=1.0,
                                                  max=4.0,
                                                  step=0.1,
                                                  default=1,
                                                  )

# Offset Gizmo Stuff
bpy.types.Scene.piv_gz_radius = bpy.props.FloatProperty(
                                                  name="Pivot Radius",
                                                  min=0.5,
                                                  max=10.0,
                                                  step=1,
                                                  )
bpy.types.Scene.piv_gz_offset = bpy.props.FloatVectorProperty(
                                                  name="Gizmo Offset",
                                                  description="Off the set",
                                                  default=(0.0, 0.0, 0.0),
                                                  unit='LENGTH',
                                                  subtype='TRANSLATION'
                                                  )
bpy.types.Scene.piv_gz_twist = bpy.props.FloatProperty(
                                                  name="Gizmo twist",
                                                  description="Off the set",
                                                  default=90.0,
                                                  step=0.01,
                                                  min=-360.0,
                                                  max=360.0,
                                                  )
bpy.types.Scene.act_gizmo_pick = bpy.props.BoolVectorProperty(
                                        name="ATB Gizmos",
                                        description="ATB Gizmo Toolbox",
                                        default=(False, False, False, False),
                                        size=4
                                        )
bpy.types.Scene.piv_gz_x = bpy.props.FloatProperty(
                                                  name="X",
                                                  step=0.01,
                                                  )
bpy.types.Scene.piv_gz_y = bpy.props.FloatProperty(
                                                  name="Y",
                                                  step=0.01,
                                                  )
bpy.types.Scene.piv_gz_z = bpy.props.FloatProperty(
                                                  name="Z",
                                                  step=0.01,
                                                  )

# This layout-switcher setup is based on HopsButtonOptions from  HardOps

# METAPANEL


class ObjectMatrixConversions(PropertyGroup):

    def set_float(self, value):
        import mathutils
        obj = bpy.context.view_layer.objects.active
        if obj:
            rot_in = mathutils.Euler(value)

            debug = False

            if debug:
                print(str(value))
                print(str(rot_in) + "\n")

            src_loc, _src_rot, _src_scale = obj.matrix_world.decompose()

            loc_mat = mathutils.Matrix.Translation(src_loc)
            rot_mat = rot_in.to_matrix()

            full_mat = loc_mat @ rot_mat.to_4x4()

            obj.matrix_world = full_mat
        else:
            self["prop"] = value

    # Local Space Getters
    def get_local_translation(self):
        obj = bpy.context.view_layer.objects.active
        if obj:
            loc, _rot, _scale = obj.matrix_local.decompose()
            return loc.to_tuple()
        else:
            return (0, 0, 0)

    def get_local_rotation(self):
        obj = bpy.context.view_layer.objects.active
        if obj:
            _loc, rot, _scale = obj.matrix_local.decompose()
            eul_rot = rot.to_euler()
            rot_tup = (eul_rot.x, eul_rot.y, eul_rot.z)
            return rot_tup
        else:
            return (0, 0, 0)

    def get_local_scale(self, context):
        obj = context.view_layer.objects.active
        if obj:
            _loc, _rot, scale = obj.matrix_local.decompose()
            return scale.to_tuple()
        else:
            return (0, 0, 0)

    # World Space Getters
    def get_world_translation(self):
        obj = bpy.context.view_layer.objects.active
        if obj:
            loc, _rot, _scale = obj.matrix_world.decompose()
            return loc.to_tuple()
        else:
            return (0, 0, 0)

    def get_world_rotation(self):
        obj = bpy.context.view_layer.objects.active
        if obj:
            eul_rot = obj.rotation_euler
            rot = obj.matrix_world.to_euler('XYZ', eul_rot)

            debug = False

            if debug:
                print(str(rot))

            return rot
        else:
            return (0, 0, 0)

    def get_world_scale(self, context):
        obj = context.view_layer.objects.active
        if obj:
            _loc, _rot, scale = obj.matrix_world.decompose()
            return scale.to_tuple()
        else:
            return (0, 0, 0)

    local_loc: FloatVectorProperty(
                                name="Object Local Location",
                                description="Object Local Location",
                                default=(0.0, 0.0, 0.0),
                                subtype='TRANSLATION',
                                get=get_local_translation
                                )

    local_rot: FloatVectorProperty(
                                name="Object Local Rotation",
                                description="Object Local Rotation",
                                default=(0.0, 0.0, 0.0),
                                subtype='EULER',
                                get=get_local_rotation
                                )

    world_loc: FloatVectorProperty(
                                name="Object World Location",
                                description="Object World Location",
                                default=(0.0, 0.0, 0.0),
                                subtype='TRANSLATION',
                                get=get_world_translation
                                )

    world_rot: FloatVectorProperty(
                                name="Object World Rotation",
                                description="Object World Rotation",
                                default=(0.0, 0.0, 0.0),
                                subtype='EULER',
                                get=get_world_rotation,
                                set=set_float
                                )


def metapanel_layout_items():
    items = [
        ('0', "Move", "Transformation Tab", 'OBJECT_ORIGIN', 1),
        ('1', "Tools", "Camera Manager Tab", 'OUTLINER_DATA_CAMERA', 2),
        ('2', "Draw", "Viewport Overlays", 'SHADING_RENDERED', 3),
        ('3', "Active", "Active Object Properties", 'OVERLAY', 4)
            ]

    return items


class MetaPanelTabs(PropertyGroup):
    stuff = metapanel_layout_items()

    tab: EnumProperty(
        name='',
        description='Current Tab',
        items=stuff
    )

    debug: BoolVectorProperty(
                            name="Debug Switches",
                            description="ATB Gizmo Toolbox",
                            default=(False, False, False, False),
                            size=4,
                            options={'SKIP_SAVE'}
                             )

    cavity_toggle: BoolVectorProperty(
                                    name="Cavity Shading",
                                    description="ATB Cavity Toggles",
                                    default=(False, False),
                                    size=2,
                                    options={'SKIP_SAVE'}
                                     )

    activeObjectPanel_Toggles: BoolVectorProperty(
                            name="Active Object Panel Sub-Section Toggles",
                            description="ATB Gizmo Toolbox",
                            default=(False, False, False, False),
                            size=4,
                            options={'SKIP_SAVE'}
                             )

    exp_objpointer: PointerProperty(
        type=bpy.types.Object,
        name="Reference Object",
        description="MAGIC",
    )

    cam_index: IntProperty(
        name="Camera Index",
        default=0
    )

# QUICK OPERATOR (MENU PANEL) PANEL


def quick_ops_items():
    items = [
        ('EDIT', "Edit Menu", "Edit Mesh", 'NONE', 1),
        ('ADD', "Add Menu", "Add Mesh", 'NONE', 2),
        ('UV', 'UV Map Menu', "UV Map Options", 'NONE', 3),
        ('CONTEXT', "Context Menu", "Right-Click Menu", 'NONE', 4),
        ('VERTEX', "Vertex Menu", "Vertex Operators", 'NONE', 5),
        ('EDGE', "Edge Menu", "Edge Operators", 'NONE', 6),
        ('FACE', "Face Menu", "FAce Operators", 'NONE', 7)
            ]

    return items


class QuickOpMenus(PropertyGroup):
    stuff = quick_ops_items()

    menus: EnumProperty(
        name='',
        description='Current Menu',
        items=stuff
    )


class CustomTransforms(PropertyGroup):

    def get_matrix(self, value):
        return 0

    transformA: FloatVectorProperty(
        name='',
        description='A persistent custom transform orientation',
        subtype='MATRIX',
        size=9,
        default=[b for a in Matrix.Identity(4).to_3x3() for b in a]
    )

    transformB: FloatVectorProperty(
        name='',
        description='A persistent custom transform orientation',
        subtype='MATRIX',
        size=9,
        default=[b for a in Matrix.Identity(4).to_3x3() for b in a]
    )

    transformC: FloatVectorProperty(
        name='',
        description='A persistent custom transform orientation',
        subtype='MATRIX',
        size=9,
        default=[b for a in Matrix.Identity(4).to_3x3() for b in a]
    )

    transformD: FloatVectorProperty(
        name='',
        description='A persistent custom transform orientation',
        subtype='MATRIX',
        size=9,
        default=[b for a in Matrix.Identity(4).to_3x3() for b in a]
    )

    transformE: FloatVectorProperty(
        name='',
        description='A persistent custom transform orientation',
        subtype='MATRIX',
  
        size=9,
        default=[b for a in Matrix.Identity(4).to_3x3() for b in a]
    )

    transformF: FloatVectorProperty(
        name='',
        description='A persistent custom transform orientation',
        subtype='MATRIX',
        size=9,
        default=[b for a in Matrix.Identity(4).to_3x3() for b in a]
    )

# WIRE COLORS


class ATBWireColors(PropertyGroup):

    default_obj_wire: FloatVectorProperty(
                                        name="Object Wireframe Color",
                                        description="Default Object Mode Wire Color",
                                        default=(0.0, 0.0, 0.0),
                                        subtype='COLOR_GAMMA',
                                        min=0.0,
                                        max=1.0,
                                        )

    default_edit_wire: FloatVectorProperty(
                                        name="Edit Mode Wireframe Color",
                                        description="Default Edit Mode Wire Color",
                                        default=(0.0, 0.0, 0.0),
                                        subtype='COLOR_GAMMA',
                                        min=0.0,
                                        max=1.0,
                                        )

    temp_obj_wire: FloatVectorProperty(
                                        name="Object Wireframe Color",
                                        description="Temporary Object Mode Wire Color",
                                        default=(0.0, 0.0, 0.0),
                                        subtype='COLOR_GAMMA',
                                        min=0.0,
                                        max=1.0,
                                        )

    temp_edit_wire: FloatVectorProperty(
                                        name="Edit Mode Wireframe Color",
                                        description="Temporary Edit Mode Wire Color",
                                        default=(0.0, 0.0, 0.0),
                                        subtype='COLOR_GAMMA',
                                        min=0.0,
                                        max=1.0,
                                        )


def fast_snap_prev_modes(get):
    if get == 'PIVOT':
        items = [
            ('BOUNDING_BOX_CENTER', "Bounding Box Center", "", 'NONE', 1),
            ('CURSOR', "3D Cursor", "", 'NONE', 2),
            ('INDIVIDUAL_ORIGINS', "Individual Origins", "", 'NONE', 3),
            ('MEDIAN_POINT', "Median Point", "", 'NONE', 4),
            ('ACTIVE_ELEMENT', "Active Element", "", 'NONE', 5),
                ]
    elif get == 'TARGET':
        items = [
            ('CLOSEST', "Closest", "", 'NONE', 1),
            ('CENTER', "Center", "", 'NONE', 2),
            ('MEDIAN', "Median", "", 'NONE', 3),
            ('ACTIVE', "Active", "", 'NONE', 4),
                ]

    return items


class FastSnapProps(PropertyGroup):
    pivot_items = fast_snap_prev_modes(get='PIVOT')
    prev_pivot: EnumProperty(
        name='',
        description='Prior Pivot Mode',
        items=pivot_items
    )

    target_items = fast_snap_prev_modes(get='TARGET')
    prev_pivot: EnumProperty(
        name='',
        description='Prior Snap Target',
        items=target_items
    )

    snap_state: IntProperty(
                                name="Snap State",
                                min=0,
                                max=5,
                                default=0
                             )


class CustomPopoverProps(PropertyGroup):

    popover_1: StringProperty(
        name="Custom Popover 1",
        description="Stores the name of a panel",
        default="BATMAN",
    )

    popover_2: StringProperty(
        name="Custom Popover 2",
        description="Stores the name of a panel",
        default="BATMAN",
    )

    popover_3: StringProperty(
        name="Custom Popover 3",
        description="Stores the name of a panel",
        default="BATMAN",
    )

