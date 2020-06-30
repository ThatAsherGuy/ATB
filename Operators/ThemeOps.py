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
import mathutils
from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatVectorProperty,
    IntVectorProperty
)


class ACT_OT_set_color(bpy.types.Operator):
    bl_idname = "act.set_color"
    bl_label = "ACT Set Theme Color"
    bl_description = "Currently toggles the viewport wireframe colors"
    bl_options = {'REGISTER', 'UNDO'}

    element: StringProperty(
        name="UI Element",
        description="The Thing You Want to Change the Color Of",
        maxlen=1024,
    )
    rgb: FloatVectorProperty(
        name="Color",
        description="Bitch, do you even color?",
        default=(0.5, 0.5, 0.5),
        size=3,
        min=0.0,
        max=1.0,
        subtype='COLOR'
    )
    sv_only: BoolProperty(
        name="SV Only",
        description="Limits color adjustment to saturation and value",
        default=False
    )
    sv_relative: BoolProperty(
        name="SV Relative",
        description="Add/Subtract SV",
        default=False
    )

    tog_vert_size: BoolProperty(
        name="Toggle Vertex Size",
        description="When enabled, operator toggles the size of vertices in the 3D Viewport"
    )

    vert_sizes: IntVectorProperty(
        name="Vertex Sizes",
        description="Vertex Sizes",
        default=(4, 8),
        size=2,
        soft_min=1,
        soft_max=32
    )

    tog_set: BoolProperty(
        name="Toggle Wireframe Lightness",
        description="When enabled, operator toggles the lightness of the UI element",
        default=False
    )
    sync_wire: BoolProperty(
        name="Sync Modes",
        description="When enabled, operator toggles the size of vertices in the 3D Viewport",
        default=False
    )
    invert_wire: BoolProperty(
        name="Invert Modes",
        description="When enabled, operator toggles the size of vertices in the 3D Viewport",
        default=False
    )

    def execute(self, context):
        input_rgb = mathutils.Color(self.rgb)

        set_to_larger = self.set_to_larger
        sync = self.sync
        invert = self.invert

        if self.tog_set:
            edit_final = self.edit_final
            object_final = self.object_final

            if context.mode == 'EDIT_MESH':
                if sync:
                    if invert:
                        context.preferences.themes[0].view_3d.wire_edit = edit_final
                        context.preferences.themes[0].view_3d.wire = self.wire_edit_color
                    else:
                        context.preferences.themes[0].view_3d.wire_edit = edit_final
                        context.preferences.themes[0].view_3d.wire = object_final
                else:
                    context.preferences.themes[0].view_3d.wire_edit = edit_final
            else:
                if sync:
                    if invert:
                        context.preferences.themes[0].view_3d.wire_edit = self.wire_object_color
                        context.preferences.themes[0].view_3d.wire = object_final
                    else:
                        context.preferences.themes[0].view_3d.wire_edit = edit_final
                        context.preferences.themes[0].view_3d.wire = object_final
                else:
                    context.preferences.themes[0].view_3d.wire = object_final
        elif self.sv_only:
            if self.sv_relative:
                if context.mode == 'EDIT_MESH':
                    context.preferences.themes[0].view_3d.wire_edit = input_rgb
                else:
                    context.preferences.themes[0].view_3d.wire = input_rgb
            else:
                if context.mode == 'EDIT_MESH':
                    context.preferences.themes[0].view_3d.wire_edit = input_rgb
                else:
                    context.preferences.themes[0].view_3d.wire = input_rgb
        else:
            object_final = input_rgb.copy()

        if self.tog_vert_size:
            if set_to_larger:
                context.preferences.themes[0].view_3d.vertex_size = self.vert_sizes[1]
            else:
                context.preferences.themes[0].view_3d.vertex_size = self.vert_sizes[0]

        return {'FINISHED'}

    def invoke(self, context, event):
        self.wire_edit_color = bpy.context.preferences.themes[0].view_3d.wire_edit.copy()
        self.wire_object_color = bpy.context.preferences.themes[0].view_3d.wire.copy()

        self.edit_final = self.wire_edit_color.copy()
        self.edit_final.v = 1 - self.wire_edit_color.v

        self.object_final = self.wire_object_color.copy()
        self.object_final.v = 1 - self.wire_object_color.v

        self.set_to_larger = False
        self.sync = False

        self.invert = False

        if self.tog_set:
            print("Toggle")
        else:
            print("Set")

        if self.tog_vert_size:
            current_size = context.preferences.themes[0].view_3d.vertex_size
            if current_size == self.vert_sizes[0]:
                self.set_to_larger = True

        if self.sync_wire:
            self.sync = True

        if self.invert_wire:
            self.invert = True

        return self.execute(context)


class ACT_OT_store_wire_color(bpy.types.Operator):
    bl_idname = "act.store_wire_color"
    bl_label = "ACT Store Wire Color"
    bl_description = "Currently toggles the viewport wireframe colors"
    bl_options = {'REGISTER', 'UNDO'}

    source: bpy.props.EnumProperty(
                                items=[
                                    (
                                        'CURRENT',
                                        "Current",
                                        "Set Colors",
                                        'COLOR',
                                        1
                                    ),
                                    (
                                        'CUSTOM',
                                        "Custom",
                                        "Use Custom Wire Colors",
                                        'COLOR',
                                        2
                                    ),
                                    (
                                        'INVERSE',
                                        "Invert",
                                        "Invert Colors",
                                        'UV_SYNC_SELECT',
                                        3
                                    ),
                                    (
                                        'SWAP',
                                        "Swap",
                                        "Swap Colors",
                                        'MOD_MIRROR',
                                        4
                                    )],
                                name="Source",
                                default='CURRENT',
                                )

    mode: bpy.props.EnumProperty(
                                items=[
                                    (
                                        'STORE_DEFAULT',
                                        "Store Default Wire Colors",
                                        "First Mode",
                                        'COPYDOWN',
                                        1
                                    ),
                                    (
                                        'STORE_TEMP',
                                        "Store Temporary Wire Colors",
                                        "Second Mode",
                                        'COPYDOWN',
                                        2
                                    ),
                                    (
                                        'RESTORE_DEFAULT',
                                        "Restore Default Wire Colors",
                                        "Third Mode",
                                        'PASTEFLIPDOWN',
                                        3
                                    ),
                                    (
                                        'RESTORE_TEMP',
                                        "Restore Temporary Wire Colors",
                                        "Third Mode",
                                        'PASTEFLIPDOWN',
                                        4
                                    ),
                                    (
                                        'SET_COLOR',
                                        "Set Color",
                                        "Set the wire color to a specific color",
                                        'PIVOT_CURSOR',
                                        5
                                    )],
                                name="Mode",
                                default='STORE_TEMP',
                                )

    obj_wire: FloatVectorProperty(
        name="Object Wire Color",
        description="Bitch, do you even color?",
        default=(0.5, 0.5, 0.5),
        size=3,
        min=0.0,
        max=1.0,
        subtype='COLOR_GAMMA'
    )

    edit_wire: FloatVectorProperty(
        name="Edit Wire Color",
        description="Bitch, do you even color?",
        default=(0.5, 0.5, 0.5),
        size=3,
        min=0.0,
        max=1.0,
        subtype='COLOR_GAMMA'
    )

    def execute(self, context):
        v3d = bpy.context.preferences.themes[0].view_3d
        ws = bpy.context.workspace
        colorz = ws.temp_wires

        if self.source == 'CURRENT':
            if self.mode == 'STORE_DEFAULT':
                colorz.default_obj_wire = v3d.wire
                colorz.default_edit_wire = v3d.wire_edit
            elif self.mode == 'STORE_TEMP':
                colorz.temp_obj_wire = v3d.wire
                colorz.temp_edit_wire = v3d.wire_edit
            elif self.mode == 'RESTORE_DEFAULT':
                v3d.wire = colorz.default_obj_wire
                v3d.wire_edit = colorz.default_edit_wire
            elif self.mode == 'RESTORE_TEMP':
                v3d.wire = colorz.temp_obj_wire
                v3d.wire_edit = colorz.temp_edit_wire
        elif self.source == 'CUSTOM':
            if self.mode == 'STORE_DEFAULT':
                colorz.default_obj_wire = self.obj_wire
                colorz.default_edit_wire = self.edit_wire
            elif self.mode == 'STORE_TEMP':
                colorz.temp_obj_wire = self.obj_wire
                colorz.temp_edit_wire = self.edit_wire
            elif self.mode == 'RESTORE_DEFAULT':
                v3d.wire = self.obj_wire
                v3d.wire_edit = self.edit_wire
            elif self.mode == 'RESTORE_TEMP':
                v3d.wire = self.obj_wire
                v3d.wire_edit = self.edit_wire
        elif self.source == 'INVERSE':
            if self.mode == 'STORE_DEFAULT':
                colorz.default_obj_wire.v = 1 - colorz.default_obj_wire.v
                colorz.default_edit_wire.v = 1 - colorz.default_edit_wire.v
            elif self.mode == 'STORE_TEMP':
                colorz.temp_obj_wire.v = 1 - colorz.temp_obj_wire.v
                colorz.temp_edit_wire.v = 1 - colorz.temp_edit_wire.v
            elif self.mode == 'RESTORE_DEFAULT':
                v3d.wire.v = (1 - v3d.wire.v)
                v3d.wire_edit.v = (1 - v3d.wire_edit.v)
            elif self.mode == 'RESTORE_TEMP':
                v3d.wire.v = (1 - v3d.wire.v)
                v3d.wire_edit.v = (1 - v3d.wire_edit.v)
        elif self.source == 'SWAP':
            if self.mode == 'STORE_DEFAULT':
                self.obj_wire = v3d.wire
                self.edit_wire = v3d.wire_edit

                v3d.wire = colorz.default_obj_wire
                v3d.wire_edit = colorz.default_edit_wire

                colorz.default_obj_wire = self.obj_wire
                colorz.default_edit_wire = self.edit_wire
            elif self.mode == 'STORE_TEMP':
                self.obj_wire = v3d.wire
                self.edit_wire = v3d.wire_edit

                v3d.wire = colorz.temp_obj_wire
                v3d.wire_edit = colorz.temp_edit_wire

                colorz.temp_obj_wire = self.obj_wire
                colorz.temp_edit_wire = self.edit_wire
            elif self.mode == 'RESTORE_DEFAULT':
                self.obj_wire = v3d.wire
                self.edit_wire = v3d.wire_edit

                v3d.wire = colorz.default_obj_wire
                v3d.wire_edit = colorz.default_edit_wire

                colorz.default_obj_wire = self.obj_wire
                colorz.default_edit_wire = self.edit_wire
            elif self.mode == 'RESTORE_TEMP':
                self.obj_wire = colorz.default_obj_wire
                self.edit_wire = colorz.default_edit_wire

                colorz.default_obj_wire = colorz.temp_obj_wire
                colorz.default_edit_wire = colorz.temp_edit_wire

                colorz.temp_obj_wire = self.obj_wire
                colorz.temp_edit_wire = self.edit_wire
        elif self.mode == 'SET_COLOR':
            pass
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col = col.column(align=False)

        row = col.row(align=True)
        row.prop_enum(self, "source", 'CURRENT')
        row.prop_enum(self, "source", 'INVERSE')
        row.prop_enum(self, "source", 'SWAP')
        col.separator()

        ws = bpy.context.workspace
        colorz = ws.temp_wires

        if self.source == 'CURRENT':
            v3d = bpy.context.preferences.themes[0].view_3d
            scene = context.scene

            row = col.row(align=True)
            row.label(text="Current:")
            row.prop(v3d, "wire", text="")
            row.prop(v3d, "wire_edit", text="")

            row = col.row(align=True)
            row.label(text="Default:")
            row.prop(colorz, "default_obj_wire", text="")
            row.prop(colorz, "default_edit_wire", text="")

            row = col.row(align=True)
            row.label(text="Temp:")
            row.prop(colorz, "temp_obj_wire", text="")
            row.prop(colorz, "temp_edit_wire", text="")

            col = col.column(align=True)
            row = col.row(align=True)
            sub = row.column(align=True)
            sub.prop_enum(self, "mode", 'STORE_DEFAULT', text="Save to Default")
            sub.prop_enum(self, "mode", 'STORE_TEMP', text="Save to Temp")
            sub = row.column(align=True)
            sub.prop_enum(self, "mode", 'RESTORE_DEFAULT', text="Set to Default")
            sub.prop_enum(self, "mode", 'RESTORE_TEMP', text="Set to Temp")

            row = col.row(align=False)
            row.prop_enum(self, "mode", 'SET_COLOR', text="Do Nothing")
        elif self.source == 'INVERSE':
            v3d = bpy.context.preferences.themes[0].view_3d
            scene = context.scene

            row = col.row(align=True)
            row.label(text="Current:")
            row.prop(v3d, "wire", text="")
            row.prop(v3d, "wire_edit", text="")

            row = col.row(align=True)
            row.label(text="Default:")
            row.prop(colorz, "default_obj_wire", text="")
            row.prop(colorz, "default_edit_wire", text="")

            row = col.row(align=True)
            row.label(text="Temp:")
            row.prop(colorz, "temp_obj_wire", text="")
            row.prop(colorz, "temp_edit_wire", text="")

            col = col.column(align=True)
            row = col.row(align=True)
            row.prop_enum(self, "mode", 'STORE_DEFAULT', text="Invert Default")
            row.prop_enum(self, "mode", 'STORE_TEMP', text="Invert Temp")
            row = col.row(align=True)
            row.prop_enum(self, "mode", 'RESTORE_DEFAULT', text="Invert Current")

            row = col.row(align=False)
            row.prop_enum(self, "mode", 'SET_COLOR', text="Do Nothing")
        elif self.source == 'SWAP':
            v3d = bpy.context.preferences.themes[0].view_3d
            scene = context.scene

            row = col.row(align=True)
            row.label(text="Current:")
            row.prop(v3d, "wire", text="")
            row.prop(v3d, "wire_edit", text="")

            row = col.row(align=True)
            row.label(text="Default:")
            row.prop(colorz, "default_obj_wire", text="")
            row.prop(colorz, "default_edit_wire", text="")

            row = col.row(align=True)
            row.label(text="Temp:")
            row.prop(colorz, "temp_obj_wire", text="")
            row.prop(colorz, "temp_edit_wire", text="")

            col = col.column(align=True)
            row = col.row(align=True)
            row.prop_enum(self, "mode", 'STORE_DEFAULT', text="Swap Current/Default")
            row.prop_enum(self, "mode", 'STORE_TEMP', text="Swap Current/Temp")
            row = col.row(align=True)
            row.prop_enum(self, "mode", 'RESTORE_TEMP', text="Swap Default/Temp")

            row = col.row(align=False)
            row.prop_enum(self, "mode", 'SET_COLOR', text="Do Nothing")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
