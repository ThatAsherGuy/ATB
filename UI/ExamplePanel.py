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


class VIEW3D_PT_view3d_example_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    # bl_category = "Dev"
    bl_label = "Example Panel"

    def draw(self, context):

        layout = self.layout
        overlay = context.space_data.overlay

        # Directly in layout:

        layout.prop(overlay, "show_axis_x", text="X", toggle=True)
        layout.prop(overlay, "show_axis_y", text="Y", toggle=True)
        layout.prop(overlay, "show_axis_z", text="Z", toggle=True)

        # In an unaligned column:

        col = layout.column(align=False)

        col.prop(overlay, "show_axis_x", text="X", toggle=True)
        col.prop(overlay, "show_axis_y", text="Y", toggle=True)
        col.prop(overlay, "show_axis_z", text="Z", toggle=True)

        # In an aligned column:

        col = layout.column(align=True)

        col.prop(overlay, "show_axis_x", text="X", toggle=True)
        col.prop(overlay, "show_axis_y", text="Y", toggle=True)
        col.prop(overlay, "show_axis_z", text="Z", toggle=True)
