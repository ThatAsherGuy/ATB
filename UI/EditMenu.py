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
    # Panel,
    Menu
)


class VIEW3D_MT_actc_root(Menu):
    bl_label = ""

    def draw(self, context):
        layout = self.layout
        # view = context.space_data
        layout.label(text="Favorites:")
        layout.operator("mesh.bridge_edge_loops", text="(A) Bridge")
        layout.operator("mesh.subdivide", text="(S) Subdivide")
        layout.operator("mesh.separate", text="(D) Separate")
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("mesh.rip_move", text="(F) Rip Fill")
        layout.operator("mesh.merge", text="(G) Merge")

        layout.separator()
        # layout.label(text="Tasks:")
        layout.menu(
            "VIEW3D_MT_actc_sub_edges",
            text="(Q) Mark",
            icon='MOD_EDGESPLIT')
        layout.menu(
            "VIEW3D_MT_actc_sub_operators",
            text="(W) Model",
            icon='MOD_MESHDEFORM')
        layout.menu(
            "VIEW3D_MT_actc_sub_select",
            text="(E) Select",
            icon='RESTRICT_SELECT_OFF')
        layout.menu(
            "VIEW3D_MT_actc_sub_add",
            text="(R) Add",
            icon='MESH_MONKEY')
        layout.menu(
            "VIEW3D_MT_actc_sub_shading",
            text="(T) Shade",
            icon='MOD_SMOOTH')

        layout.separator()

        layout.operator(
            "mesh.select_mode",
            text="(Z) Vertex Select",
            icon='VERTEXSEL').type = 'VERT'
        layout.operator(
            "mesh.select_mode",
            text="(X) Edge Select",
            icon='EDGESEL').type = 'EDGE'
        layout.operator(
            "mesh.select_mode",
            text="(C) Face Select",
            icon='FACESEL').type = 'FACE'


class VIEW3D_MT_actc_sub_edges(Menu):
    bl_label = "Context Menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("mesh.mark_sharp", text="(A) Mark Sharp").clear = False
        layout.operator("mesh.mark_seam", text="(S) Mark Seam").clear = False
        layout.operator("transform.edge_crease", text="(D) Mark Crease").value = 1
        layout.operator("transform.edge_bevelweight", text="(F) Mark Bevel").value = 1
        layout.operator("mesh.mark_freestyle_edge", text="(G) Mark Freestyle").clear = False

        layout.separator()

        layout.operator("mesh.mark_sharp", text="(Z) Clear Sharp").clear = True
        layout.operator("mesh.mark_seam", text="(X) Clear Seam").clear = True
        layout.operator("transform.edge_crease", text="(C) Clear Crease").value = -1
        layout.operator("transform.edge_bevelweight", text="(V) Clear Bevel").value = -1
        layout.operator("mesh.mark_freestyle_edge", text="(B) Clear Freestyle").clear = True


class VIEW3D_MT_actc_sub_operators(Menu):
    bl_label = "Context Menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("mesh.extrude_region_move", text="(A) Extrude")
        layout.operator("mesh.bevel", text="(S) Bevel")
        layout.operator("mesh.inset", text="(D) Inset")
        layout.operator("transform.edge_bevelweight", text="(F) Mark Bevel")
        layout.operator("mesh.mark_freestyle_edge", text="(G) Mark Freestyle")


class VIEW3D_MT_actc_sub_select(Menu):
    bl_label = "Context Menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("mesh.loop_to_region", text="(A) Inner")
        layout.operator("mesh.region_to_loop", text="(S) Outer")
        layout.operator("mesh.faces_select_linked_flat", text="(D) Surface")
        layout.operator("mesh.loop_multi_select", text="(F) Loops")
        layout.operator("mesh.edges_select_sharp", text="(G) Sharp")

        layout.separator()

        layout.operator("mesh.select_more", text="(Z) More")
        layout.operator("mesh.select_less", text="(X) Less")
        layout.operator("mesh.select_all", text="(C) Toggle")
        layout.operator("mesh.select_similar", text="(V) Similar")
        layout.operator("mesh.select_mirror", text="(B) Mirror").extend = True


class VIEW3D_MT_actc_sub_add(Menu):
    bl_label = "Context Menu"

    def draw(self, context):
        layout = self.layout

        layout.operator(
            "mesh.primitive_cube_add",
            text="(A) Cube",
            icon='MESH_CUBE')
        layout.operator(
            "mesh.primitive_plane_add",
            text="(S) Plane",
            icon='MESH_PLANE')
        layout.operator(
            "mesh.primitive_cylinder_add",
            text="(D) Cylinder",
            icon='MESH_CYLINDER')
        layout.operator(
            "mesh.primitive_torus_add",
            text="(F) Torus",
            icon='MESH_TORUS')
        layout.operator(
            "mesh.primitive_cone_add",
            text="(G) Cone",
            icon='MESH_CONE')

        layout.separator()

        layout.operator(
            "mesh.primitive_uv_sphere_add",
            text="(Z) UV Sphere",
            icon='MESH_UVSPHERE')
        layout.operator(
            "mesh.primitive_ico_sphere_add",
            text="(X) Ico Sphere",
            icon='MESH_ICOSPHERE')
        layout.operator(
            "mesh.primitive_circle_add",
            text="(C) Circle",
            icon='MESH_CIRCLE')
        layout.operator(
            "mesh.primitive_cube_add_gizmo",
            text="(V) Fancy Cube",
            icon='LIGHTPROBE_CUBEMAP')


class VIEW3D_MT_actc_sub_shading(Menu):
    bl_label = "Context Menu"

    def draw(self, context):
        active_mesh = context.active_object.data
        layout = self.layout
        layout.alignment = 'RIGHT'

        layout.operator("mesh.faces_shade_smooth", text="(A) Shade Smooth")
        layout.operator("mesh.faces_shade_flat", text="(S) Shade Flat")
        layout.operator("mesh.normals_make_consistent", text="(D) Recalculate Normals")
        layout.operator("mesh.flip_normals", text="(F) Flip Normals")

        layout.separator()
        layout.prop(
            active_mesh,
            "use_auto_smooth",
            text="Auto Smooth",
            toggle=True
        )
        layout.prop(
            active_mesh,
            "auto_smooth_angle",
            text="       Angle",
        )


class VIEW3D_MT_actc_sub_mesh(Menu):
    bl_label = "Context Menu"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_REGION_WIN'
        op = layout.operator("mesh.vertices_smooth", text="Smooth Vertices — Invoke Region")
        op.wait_for_input = False
        op.factor = 0
