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
import bgl
import blf
import gpu
import bmesh
import numpy
from gpu_extras.batch import batch_for_shader

def draw_modal_text_px(self, context, text):
    font_id = 0

    loc = self.loc
    offset = self.offset

    blf.position(font_id, loc[0] + offset[0], loc[1] + offset[1], 0)
    blf.size(font_id, 20, 72)
    blf.draw(font_id, text)


def make_batch_edges(self, context):

    mesh = self.obj.data

    vertices = numpy.empty((len(mesh.vertices), 3), 'f')
    indices = numpy.empty((len(mesh.edges), 2), 'i')

    mesh.vertices.foreach_get(
        "co", numpy.reshape(vertices, len(mesh.vertices) * 3))
    mesh.edges.foreach_get(
        "vertices", numpy.reshape(indices, len(mesh.edges) * 2))

    mat = self.obj.matrix_world

    shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINES', {"pos": vertices}, indices=indices)
    return (batch, shader)

def draw_batch(self, context, shader, batch):
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glEnable(bgl.GL_LINE_SMOOTH)
    bgl.glLineWidth(3)

    shader.bind()
    shader.uniform_float("color", (1,1,1, 0.75))

    gpu.matrix.multiply_matrix(self.obj.matrix_world)

    batch.draw(shader)

    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glDisable(bgl.GL_LINE_SMOOTH)