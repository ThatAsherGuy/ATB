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
from bpy.props import (
    FloatVectorProperty,
    EnumProperty
)
from mathutils import Matrix, Vector, Quaternion
import bmesh
from random import random
# from math import degrees


class ATB_OT_RotateAroundPivot(bpy.types.Operator):
    """Wrapper for transform.rotate"""
    bl_idname = "atb.rotate_around_pivot"
    bl_label = "ATB Rotate Around Pivot"
    bl_description = "Wrapper for transform.rotate"
    bl_options = {'REGISTER', 'UNDO'}

    offset: FloatVectorProperty(
        name="Pivot Offset",
        description="Pivot offset vector",
        default=(0.0, 0.0, 0.0)
    )

    def invoke(self, context, event):
        bpy.ops.transform.rotate(
            'INVOKE_DEFAULT',
            orient_axis='Z',
            orient_type='GLOBAL',
            center_override=self.offset,
            constraint_axis=(True, True, True)
        )
        bpy.context.area.tag_redraw()
        return {'FINISHED'}


# Experimental stuff. Won't add this to the front end for a while yet.
class ATB_OT_SnapAndAlignCursor(bpy.types.Operator):
    """Wrapper for transform.rotate"""
    bl_idname = "atb.snap_align_cursor"
    bl_label = "ATB Snap and Align Cursor"
    bl_description = "Wrapper for transform.rotate"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object or context.selected_objects

    mode_items = [
        ("SNAP_ONLY", "Red", "", 1),
        ("ALIGN_ONLY", "Green", "", 2),
        ("SNAP_ALIGN", "Blue", "", 3),
        ("TWIST", "Yellow", "", 4),
    ]

    move_mode: EnumProperty(
        items=mode_items,
        name="Mode",
        description="Cursor manipulation mode",
        default='SNAP_ALIGN'
    )

    # Internal flag
    internal_mode = "NOPE"

    def align_cursor(self, context, active):

        if self.internal_mode == 'EDIT_MESH':

            bm = bmesh.from_edit_mesh(active.data)
            bm.normal_update()
            bm.verts.ensure_lookup_table()

            if context.scene.tool_settings.mesh_select_mode[0]:
                elements = [v for v in bm.verts if v.select]

            elif context.scene.tool_settings.mesh_select_mode[1]:
                elements = [e for e in bm.edges if e.select]

            elif context.scene.tool_settings.mesh_select_mode[2]:
                elements = [f for f in bm.faces if f.select]

            if len(elements) == 1:

                element = elements[0]
                mx = active.matrix_world

                if isinstance(element, bmesh.types.BMVert):
                    origin = mx @ element.co
                    normal = mx.to_3x3() @ element.normal
                    rmx = create_rotation_matrix_from_normal(active, normal)

                elif isinstance(element, bmesh.types.BMEdge):
                    origin = mx @ get_center_between_verts(*element.verts)
                    rmx = create_rotation_matrix_from_edge(active, element)

                elif isinstance(element, bmesh.types.BMFace):
                    origin = mx @ element.calc_center_median()
                    normal = mx.to_3x3() @ element.normal
                    rmx = create_rotation_matrix_from_normal(active, normal)

                # create quat from rmx
                quat = rmx.to_quaternion()

                set_cursor(origin, quat)

                return True

            else:
                return False
        if not active:
            print("FUCK")

    def invoke(self, context, event):

        active = context.active_object
        sel = [obj for obj in context.selected_objects if obj != active]

        # make sure the is an active
        if sel and not active:
            context.view_layer.objects.active = sel[0]
            sel.remove(active)

        if context.mode == 'OBJECT' and active and not sel:
            self.internal_mode = 'OBJECT'
        elif context.mode == 'EDIT_MESH':
            self.internal_mode = 'EDIT_MESH'

        self.execute(context)
        return {'FINISHED'}

    def execute(self, context):
        active = context.active_object

        if self.move_mode == 'SNAP_ONLY':
            bpy.ops.view3d.snap_cursor_to_selected()
        elif self.move_mode == 'ALIGN_ONLY':
            self.align_cursor(context, active)
        elif self.move_mode == 'SNAP_ALIGN':
            bpy.ops.view3d.snap_cursor_to_selected()
            self.align_cursor(context, active)
        elif self.move_mode == 'TWIST':
            print("I didn't expect to get this far")


# Bunch of stuff yoinked from Machin3Tools for reference. Buy his add-ons. They're better than mine.
# Seriously.
# Not Lying Here.


def set_cursor(location=Vector(), rotation=Quaternion()):
    """
    set cursor location (Vector), and rotation (Quaternion)
    note, that setting cursor.matrix has no effect unfortunately
    """

    cursor = bpy.context.scene.cursor

    # set location
    if location:
        cursor.location = location

    # set rotation
    if rotation:
        if cursor.rotation_mode == 'QUATERNION':
            cursor.rotation_quaternion = rotation

        elif cursor.rotation_mode == 'AXIS_ANGLE':
            cursor.rotation_axis_angle = rotation.to_axis_angle()

        else:
            cursor.rotation_euler = rotation.to_euler(cursor.rotation_mode)


def get_center_between_points(point1, point2, center=0.5):
    return point1 + (point2 - point1) * center


def get_center_between_verts(vert1, vert2, center=0.5):
    return get_center_between_points(vert1.co, vert2.co, center=center)


def get_edge_normal(edge):
    return average_normals([f.normal for f in edge.link_faces])


def average_normals(normalslist):
    avg = Vector()

    for n in normalslist:
        avg += n

    return avg.normalized()


def create_rotation_matrix_from_normal(obj, normal):
    mx = obj.matrix_world

    objup = mx.to_3x3() @ Vector((0, 0, 1))

    dot = normal.dot(objup)
    if abs(round(dot, 6)) == 1:
        # use x instead of z as the up axis
        objup = mx.to_3x3() @ Vector((1, 0, 0))

    tangent = objup.cross(normal)
    binormal = tangent.cross(-normal)

    # create rotation matrix from coordnate vectors, see http://renderdan.blogspot.com/2006/05/rotation-matrix-from-axis-vectors.html
    rotmx = Matrix()
    rotmx[0].xyz = tangent.normalized()
    rotmx[1].xyz = binormal.normalized()
    rotmx[2].xyz = normal.normalized()

    # transpose, because blender is column major?
    return rotmx.transposed()


def create_rotation_matrix_from_edge(obj, edge):
    mx = obj.matrix_world

    # call the direction, the binormal, we want this to be the y axis at the end
    binormal = mx.to_3x3() @ (edge.verts[1].co - edge.verts[0].co)

    # get a normal from the linked faces
    if edge.link_faces:
        normal = mx.to_3x3() @ get_edge_normal(edge)

    # without linked faces get a normal from the objects up vector
    else:
        objup = mx.to_3x3() @ Vector((0, 0, 1))

        # use the x axis if the edge is already pointing in z
        dot = binormal.dot(objup)
        if abs(round(dot, 6)) == 1:
            objup = mx.to_3x3() @ Vector((1, 0, 0))

        normal = objup.cross(binormal)

    # get the tangent
    tangent = normal.cross(-binormal)

    # create rotation matrix from coordnate vectors, see http://renderdan.blogspot.com/2006/05/rotation-matrix-from-axis-vectors.html
    rotmx = Matrix()
    rotmx[0].xyz = tangent.normalized()
    rotmx[1].xyz = binormal.normalized()
    rotmx[2].xyz = normal.normalized()

    # transpose, because blender is column major?
    return rotmx.transposed()


def create_rotation_difference_matrix_from_quat(v1, v2):
    q = v1.rotation_difference(v2)
    return q.to_matrix().to_4x4()


class CursorToSelected(bpy.types.Operator):
    bl_idname = "machin3.cursor_to_selected"
    bl_label = "MACHIN3: Cursor to Selected"
    bl_description = "Set Cursor location and rotation to selected object or mesh element"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object or context.selected_objects

    def execute(self, context):
        active = context.active_object
        sel = [obj for obj in context.selected_objects if obj != active]

        # make sure the is an active
        if sel and not active:
            context.view_layer.objects.active = sel[0]
            sel.remove(active)

        # initiate bool used for using Blender's op as a fallback
        is_cursor_set = False

        # if in object mode with multiple selected ojects, pass it on to Blender's op
        if context.mode == 'OBJECT' and active and not sel:
            self.cursor_to_active_object(active)
            is_cursor_set = True

        elif context.mode == 'EDIT_MESH':
            is_cursor_set = self.cursor_to_mesh_element(context, active)

        # finish if the cursor has been set
        if is_cursor_set:
            return {'FINISHED'}

        # fall back for cases not covered above
        bpy.ops.view3d.snap_cursor_to_selected()

        return {'FINISHED'}

    def cursor_to_mesh_element(self, context, active):
        bm = bmesh.from_edit_mesh(active.data)
        bm.normal_update()
        bm.verts.ensure_lookup_table()

        if context.scene.tool_settings.mesh_select_mode[0]:
            elements = [v for v in bm.verts if v.select]

        elif context.scene.tool_settings.mesh_select_mode[1]:
            elements = [e for e in bm.edges if e.select]

        elif context.scene.tool_settings.mesh_select_mode[2]:
            elements = [f for f in bm.faces if f.select]

        if len(elements) == 1:

            element = elements[0]
            mx = active.matrix_world

            if isinstance(element, bmesh.types.BMVert):
                origin = mx @ element.co
                normal = mx.to_3x3() @ element.normal
                rmx = create_rotation_matrix_from_normal(active, normal)

            elif isinstance(element, bmesh.types.BMEdge):
                origin = mx @ get_center_between_verts(*element.verts)
                rmx = create_rotation_matrix_from_edge(active, element)

            elif isinstance(element, bmesh.types.BMFace):
                origin = mx @ element.calc_center_median()
                normal = mx.to_3x3() @ element.normal
                rmx = create_rotation_matrix_from_normal(active, normal)

            # create quat from rmx
            quat = rmx.to_quaternion()

            set_cursor(origin, quat)

            return True

        else:
            return False

    def cursor_to_active_object(self, active):
        mx = active.matrix_world
        origin, quat, _ = mx.decompose()

        set_cursor(origin, quat)

class ATB_OT_CreateNamedOrientation(bpy.types.Operator):
    """Wrapper for custom orientations"""
    bl_idname = "atb.make_named_orientation"
    bl_label = "ATB Custom Orientation"
    bl_description = "Set/Update Orientation Quick Slot"
    bl_options = {'REGISTER', 'UNDO'}

    slot_enum = [
        ("SLOT_A", "Red", "", 1),
        ("SLOT_B", "Green", "", 2),
        ("SLOT_C", "Blue", "", 3),
        ("SLOT_D", "Yellow", "", 4),
        ("SLOT_E", "Cyan", "", 5),
        ("SLOT_F", "Fuchsia", "", 6),
    ]

    transform_slot: EnumProperty(
        items=slot_enum,
        name="Slot",
        description="Which transform slot to set/get/update",
        default='SLOT_A'
    )

    def invoke(self, context, event):
        debug = False
        # slots = context.workspace.custom_transforms

        if self.transform_slot == 'SLOT_A':
            slot = context.workspace.custom_transforms.transformA
        elif self.transform_slot == 'SLOT_B':
            slot = context.workspace.custom_transforms.transformB
        elif self.transform_slot == 'SLOT_C':
            slot = context.workspace.custom_transforms.transformC
        elif self.transform_slot == 'SLOT_D':
            slot = context.workspace.custom_transforms.transformD
        elif self.transform_slot == 'SLOT_E':
            slot = context.workspace.custom_transforms.transformE
        elif self.transform_slot == 'SLOT_F':
            slot = context.workspace.custom_transforms.transformF

        modifiers = [False, False, False]

        if event.shift:
            print("SHIFT")
            modifiers[0] = True
        if event.ctrl:
            print("CTRL")
            modifiers[1] = True
        if event.alt:
            print("ALT")
            modifiers[2] = True

        blank = Matrix.Identity(4).to_3x3()

        atb_slot = True

        if not bpy.context.scene.transform_orientation_slots[0].type == 'ATB':
            try:
                bpy.ops.transform.select_orientation(
                                    'EXEC_DEFAULT',
                                    False,
                                    orientation='ATB'
                )
            except Exception as inst:
                if debug:
                    print(str(inst))
                atb_slot = False

        if slot == blank:

            if not atb_slot:
                bpy.ops.transform.create_orientation(
                                'EXEC_DEFAULT',
                                False,
                                name="ATB",
                                use=True,
                                use_view=False)

            obj_mat = bpy.context.active_object.matrix_world.to_3x3()
            new = bpy.context.scene.transform_orientation_slots[0].custom_orientation.matrix = obj_mat
            slot = new
        else:
            obj_mat = bpy.context.active_object.matrix_world.to_3x3()

            if modifiers[0]:
                new = bpy.context.scene.transform_orientation_slots[0].custom_orientation.matrix = obj_mat
                slot = new

            if not atb_slot:
                bpy.ops.transform.create_orientation(
                                'EXEC_DEFAULT',
                                False,
                                name="ATB",
                                use=True,
                                use_view=False)

            bpy.context.scene.transform_orientation_slots[0].custom_orientation.matrix = slot.to_3x3()
            print(str(slot))

        slot = slot.inverted_safe()

        if self.transform_slot == 'SLOT_A':
            context.workspace.custom_transforms.transformA = [b for a in slot.to_3x3() for b in a]
        elif self.transform_slot == 'SLOT_B':
            context.workspace.custom_transforms.transformB = [b for a in slot.to_3x3() for b in a]
        elif self.transform_slot == 'SLOT_C':
            context.workspace.custom_transforms.transformC = [b for a in slot.to_3x3() for b in a]
        elif self.transform_slot == 'SLOT_D':
            context.workspace.custom_transforms.transformD = [b for a in slot.to_3x3() for b in a]
        elif self.transform_slot == 'SLOT_E':
            context.workspace.custom_transforms.transformE = [b for a in slot.to_3x3() for b in a]
        elif self.transform_slot == 'SLOT_F':
            context.workspace.custom_transforms.transformF = [b for a in slot.to_3x3() for b in a]

        bpy.ops.transform.select_orientation(
                            'EXEC_DEFAULT',
                            False,
                            orientation='ATB'
        )

        return {'FINISHED'}

class ATB_OT_CursorToOrientation(bpy.types.Operator):
    """Aligns the 3D Cursor to the active orientation. Doesn't fuck with mesh data"""
    bl_idname = "atb.align_cursor_to_orientation"
    bl_label = "ATB Align Cursor to Orientation"
    bl_description = "Aligns the 3d cursor to the active transform orientation"
    bl_options = {'REGISTER', 'UNDO'}

    custom = False

    @classmethod
    def poll(cls, context):
        return context.active_object or context.selected_objects


    def execute(self, context):
        cursor = bpy.context.scene.cursor

        if self.custom:
            cursor.matrix = cursor.matrix @ bpy.context.scene.transform_orientation_slots[0].custom_orientation.matrix.to_4x4()
        else:
            orient_type = bpy.context.scene.transform_orientation_slots[0].type

            if orient_type == 'GLOBAL':
                loc = cursor.matrix.to_translation()
                cursor.matrix = Matrix.Translation(loc)
                # Pass
            elif orient_type == 'LOCAL' or orient_type == 'NORMAL':
                rot = context.active_object.matrix_world.to_quaternion().to_matrix().to_4x4().inverted_safe()
                loc = Matrix.Translation(cursor.matrix.to_translation())
                mat = loc @ rot 
                cursor.matrix = mat
            elif orient_type == 'VIEW':
                rot = bpy.context.region_data.view_matrix.to_quaternion().to_matrix().to_4x4().inverted_safe()
                loc = Matrix.Translation(cursor.matrix.to_translation())
                mat = loc @ rot 
                cursor.matrix = mat

        bpy.context.scene.frame_current = bpy.context.scene.frame_current

        return {'FINISHED'}


    def invoke(self, context, event):
        if bpy.context.scene.transform_orientation_slots[0].custom_orientation:
            self.custom = True

        self.execute(context)
        return {'FINISHED'}


class ATB_OT_SetOrigin(bpy.types.Operator):
    bl_idname = "atb.set_origin"
    bl_label = "ATB Set Origin"
    bl_description = "Moves the object origin to your selection. Works in edit mode"
    bl_options = {'REGISTER', 'UNDO'}

    mode_enum = [
        ("SELECTION", "Snap To Selection", "", 1),
        ("CURSOR", "Snap To 3D Cursor", "", 2),
    ]

    snap_mode: EnumProperty(
        items=mode_enum,
        name="Snap Mode",
        description="Which transform slot to set/get/update",
        default='SELECTION'
    )

    def invoke(self, context, event):
        CursorMatrix = bpy.context.scene.cursor.matrix.copy()

        modifiers = [False, False, False]

        if event.shift:
            modifiers[0] = True
        if event.ctrl:
            modifiers[1] = True
        if event.alt:
            modifiers[2] = True
        
        if bpy.context.mode == 'EDIT_MESH':
            if self.snap_mode == 'SELECTION':
                bpy.ops.view3d.snap_cursor_to_selected()

            bpy.ops.object.editmode_toggle()

            if len(context.selected_editable_objects) > 1:
                for obj in context.selected_editable_objects:
                    if not obj == bpy.context.active_object:
                        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            else:
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

            bpy.ops.object.editmode_toggle()
        else:
            if self.snap_mode == 'SELECTION':
                bpy.ops.view3d.snap_cursor_to_active()
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

        bpy.context.scene.cursor.matrix = CursorMatrix
        bpy.context.scene.frame_current = bpy.context.scene.frame_current
        return {'FINISHED'}


class ATB_OT_SetOriginToBBox(bpy.types.Operator):
    bl_idname = "atb.origin_to_bbox"
    bl_label = "ATB Set Origin To Bounding Box"
    bl_description = "Moves the object origin to a point on its bounding box"
    bl_options = {'REGISTER', 'UNDO'}

    mode_enum = [
        ("POINT", "Snap To Box Corner", "", 1),
        ("FACE", "Snap To Box Face", "", 2),
    ]

    box_mode: EnumProperty(
        items=mode_enum,
        name="Snap Mode",
        description="Which transform slot to set/get/update",
        default='POINT'
    )

    point_enum = [
        ("XNEG_YNEG_ZNEG", "-X -Y -Z Corner", "", 1),
        ("XNEG_YNEG_ZPOS", "-X -Y +Z Corner", "", 2),
        ("XNEG_YPOS_ZPOS", "-X +Y +Z Corner", "", 3),
        ("XNEG_YPOS_ZNEG", "-X +Y -Z Corner", "", 4),
        ("XPOS_YNEG_ZNEG", "+X -Y -Z Corner", "", 5),
        ("XPOS_YNEG_ZPOS", "+X -Y +Z Corner", "", 6),
        ("XPOS_YPOS_ZPOS", "+X +Y +Z Corner", "", 7),
        ("XPOS_YPOS_ZNEG", "+X +Y -Z Corner", "", 8),
    ]

    box_point: EnumProperty(
        items=point_enum,
        name="Box Point",
        description="Which transform slot to set/get/update",
        default='XNEG_YNEG_ZNEG'
    )

    face_enum = [
        ("XPOS", "+X Face", "", 1),
        ("XNEG", "-X Face", "", 2),
        ("YPOS", "+Y Face", "", 3),
        ("YNEG", "-Y Face", "", 4),
        ("ZPOS", "+Z Face", "", 5),
        ("ZNEG", "-Z Face", "", 6),
        ("CENTER", "Bounding Box Center", "", 7),
    ]

    box_face: EnumProperty(
        items=face_enum,
        name="Box Face",
        description="Which transform slot to set/get/update",
        default='ZNEG'
    )


    @classmethod
    def poll(cls, context):
        return context.active_object or context.selected_objects

    def invoke(self, context, event):
        cursor = bpy.context.scene.cursor
        CursorMatrix = bpy.context.scene.cursor.matrix.copy()

        obj = context.active_object
        obj_rot = obj.matrix_world.to_quaternion()
        obj_loc = obj.location.copy()
        raw_bounds = obj.bound_box

        bounds = []
        for point in raw_bounds:
            bounds.append(Vector(point))

        snap_point = Vector((0,0,0))
        snap_type = 'ORIGIN_CURSOR'

        modifiers = [False, False, False]

        if event.shift:
            modifiers[0] = True
        if event.ctrl:
            modifiers[1] = True
        if event.alt:
            modifiers[2] = True

        if self.box_mode == 'POINT':
            if self.box_point == "XNEG_YNEG_ZNEG":
                snap_point = bounds[0]
            elif self.box_point == "XNEG_YNEG_ZPOS":
                snap_point = bounds[1]
            elif self.box_point == "XNEG_YPOS_ZPOS":
                snap_point = bounds[2]
            elif self.box_point == "XNEG_YPOS_ZNEG":
                snap_point = bounds[3]
            elif self.box_point == "XPOS_YNEG_ZNEG":
                snap_point = bounds[4]
            elif self.box_point == "XPOS_YNEG_ZPOS":
                snap_point = bounds[5]
            elif self.box_point == "XPOS_YPOS_ZPOS":
                snap_point = bounds[6]
            elif self.box_point == "XPOS_YPOS_ZNEG":
                snap_point = bounds[7]
            else:
                print("SHIT")
        elif self.box_mode == 'FACE':
            if self.box_face == "XPOS":
                snap_point = (bounds[4] + bounds[5] + bounds[6] + bounds[7])/(4.0)
            elif self.box_face == "XNEG":
                snap_point = (bounds[0] + bounds[1] + bounds[2] + bounds[3])/(4.0)
            elif self.box_face == "YPOS":
                snap_point = (bounds[2] + bounds[3] + bounds[6] + bounds[7])/(4.0)
            elif self.box_face == "YNEG":
                snap_point = (bounds[0] + bounds[1] + bounds[4] + bounds[5])/(4.0)
            elif self.box_face == "ZPOS":
                snap_point = (bounds[1] + bounds[2] + bounds[5] + bounds[6])/(4.0)
            elif self.box_face == "ZNEG":
                snap_point = (bounds[0] + bounds[3] + bounds[4] + bounds[7])/(4.0)
            elif self.box_face == "CENTER":
                # snap_point = Vector(snap_point)
                for point in bounds:
                    snap_point += point
                snap_type = 'ORIGIN_GEOMETRY'

        snap_point.rotate(obj_rot)

        cursor.location = snap_point + obj.location

        if bpy.context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type=snap_type, center='MEDIAN')
            bpy.ops.object.editmode_toggle()
        else:
            bpy.ops.object.origin_set(type=snap_type, center='MEDIAN')

        bpy.context.scene.cursor.matrix = CursorMatrix
        bpy.context.scene.frame_current = bpy.context.scene.frame_current

        if modifiers[2]:
            if (self.box_mode == "POINT") or not (self.box_face == "CENTER"):
                obj.location -= snap_point
        return {'FINISHED'}


class ATB_OT_QuickSnapOrigin(bpy.types.Operator):
    bl_idname = "atb.quick_snap_origin"
    bl_label = "ATB Snap Origin"
    bl_description = "Nested Modal Magic"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tool_settings = context.scene.tool_settings
        tool_settings.snap_elements = self.snap_elements
        tool_settings.snap_target = self.snap_target
        tool_settings.use_transform_data_origin = False
        tool_settings.use_snap = False
        print("FIN")
        return {'FINISHED'}

    def modal(self, context, event):

        if not self.inner:
            self.inner = True
            bpy.ops.transform.translate(
                'INVOKE_DEFAULT',
                False,
                cursor_transform=False
            )
            return {'RUNNING_MODAL'}

        if event.type == 'LEFTMOUSE':
            return self.execute(context)

        if event.type == 'RET':
            if event.value == 'RELEASE':
                return self.execute(context)

        if event.type == 'SPACE':
            if event.value == 'RELEASE':
                tool_settings = context.scene.tool_settings
                if tool_settings.snap_elements == {'VERTEX', 'EDGE_MIDPOINT'}:
                    tool_settings.snap_elements = {'EDGE'}
                elif tool_settings.snap_elements == {'EDGE'}:
                    tool_settings.snap_elements = {'FACE'}
                elif tool_settings.snap_elements == {'FACE'}:
                    tool_settings.snap_elements = {'VERTEX', 'EDGE_MIDPOINT'}
                self.inner = False
                return {'RUNNING_MODAL'}

        if event.type == 'ESCAPE':
            if event.value == 'RELEASE':
                return {'CANCELLED'}

        return {'RUNNING_MODAL'}
            

    def invoke(self, context, event):
        tool_settings = context.scene.tool_settings

        self.snap_elements = tool_settings.snap_elements
        self.snap_target = tool_settings.snap_target

        self.inner = False

        tool_settings.use_transform_data_origin = True
        tool_settings.use_snap = True
        tool_settings.snap_elements = {'VERTEX', 'EDGE_MIDPOINT'}

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}