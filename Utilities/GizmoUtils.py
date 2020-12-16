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


class ATBPrintVerts(bpy.types.Operator):
    bl_idname = "atb.print_verts"
    bl_label = "Print Vertex Coordinates"
    bl_description = "Creates a list of vertex coordinates that can be used for gizmos"
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        obj = bpy.context.active_object
        me = obj.data
        # bm = bmesh.from_edit_mesh(me)

        me.calc_loop_triangles()

        tris = me.loop_triangles
        verts = me.vertices

        tri_list = []
        for i, elem in enumerate(tris):
            vert_list = []
            for j, vert in enumerate(tris[i].vertices):
                vv = verts[vert].co
                vv = vv.to_tuple(2)
                vert_list.append(vv)
            tri_list.append(vert_list)
            print(vert_list)

        # print(str(tri_list))

        # for vert in vert_tup:
        #     print(str(vert))
        return {'FINISHED'}
