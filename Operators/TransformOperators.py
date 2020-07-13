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
# from math import degrees


class ATB_OT_RotateAroundPivot(bpy.types.Operator):
    """Wrapper for transform.rotate"""
    bl_idname = "act.rotate_around_pivot"
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
