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
import bl_ui


# Mirrors UnifiedPaintPanel from properties_paint_common.py
class UT_SculptPieBase():
    ut_name = None
    ut_group = None
    ut_flags = {}

    @staticmethod
    def get_brush_mode(context):
        """ Get the correct mode for this context. For any context where this returns None,
            no brush options should be displayed."""
        mode = context.mode

        if mode == 'PARTICLE':
            # Particle brush settings currently completely do their own thing.
            return None

        from bl_ui.space_toolsystem_common import ToolSelectPanelHelper
        tool = ToolSelectPanelHelper.tool_active_from_context(context)

        if not tool:
            # If there is no active tool, then there can't be an active brush.
            return None

        if not tool.has_datablock:
            # tool.has_datablock is always true for tools that use brushes.
            return None

        space_data = context.space_data
        tool_settings = context.tool_settings

        if space_data:
            space_type = space_data.type
            if space_type == 'IMAGE_EDITOR':
                if space_data.show_uvedit:
                    return 'UV_SCULPT'
                return 'PAINT_2D'
            elif space_type in {'VIEW_3D', 'PROPERTIES'}:
                if mode == 'PAINT_TEXTURE':
                    if tool_settings.image_paint:
                        return mode
                    else:
                        return None
                return mode
        return None

    @staticmethod
    def paint_settings(context):
        tool_settings = context.tool_settings

        mode = UT_SculptPieBase.get_brush_mode(context)

        # 3D paint settings
        if mode == 'SCULPT':
            return tool_settings.sculpt
        elif mode == 'PAINT_VERTEX':
            return tool_settings.vertex_paint
        elif mode == 'PAINT_WEIGHT':
            return tool_settings.weight_paint
        elif mode == 'PAINT_TEXTURE':
            return tool_settings.image_paint
        elif mode == 'PARTICLE':
            return tool_settings.particle_edit
        # 2D paint settings
        elif mode == 'PAINT_2D':
            return tool_settings.image_paint
        elif mode == 'UV_SCULPT':
            return tool_settings.uv_sculpt
        # Grease Pencil settings
        elif mode == 'PAINT_GPENCIL':
            return tool_settings.gpencil_paint
        elif mode == 'SCULPT_GPENCIL':
            return tool_settings.gpencil_sculpt_paint
        elif mode == 'WEIGHT_GPENCIL':
            return tool_settings.gpencil_weight_paint
        elif mode == 'VERTEX_GPENCIL':
            return tool_settings.gpencil_vertex_paint
        return None

    @staticmethod
    def prop_unified(
            layout,
            context,
            brush,
            prop_name,
            unified_name=None,
            pressure_name=None,
            icon='NONE',
            text=None,
            slider=False,
            header=False,
    ):
        """ Generalized way of adding brush options to the UI,
            along with their pen pressure setting and global toggle, if they exist. """
        row = layout.row(align=True)
        ups = context.tool_settings.unified_paint_settings
        prop_owner = brush
        if unified_name and getattr(ups, unified_name):
            prop_owner = ups

        row.prop(prop_owner, prop_name, icon=icon, text=text, slider=slider)

        if pressure_name:
            row.prop(brush, pressure_name, text="")

        if unified_name and not header:
            # NOTE: We don't draw UnifiedPaintSettings in the header to reduce clutter. D5928#136281
            row.prop(ups, unified_name, text="", icon='BRUSHES_ALL')

        return row

    @staticmethod
    def prop_unified_color(parent, context, brush, prop_name, *, text=None):
        ups = context.tool_settings.unified_paint_settings
        prop_owner = ups if ups.use_unified_color else brush
        parent.prop(prop_owner, prop_name, text=text)

    @staticmethod
    def prop_unified_color_picker(parent, context, brush, prop_name, value_slider=True):
        ups = context.tool_settings.unified_paint_settings
        prop_owner = ups if ups.use_unified_color else brush
        parent.template_color_picker(prop_owner, prop_name, value_slider=value_slider)


def do_pie(self, context, event, func):
    wm = context.window_manager
    wm.popup_menu_pie(event, draw_func=func, title="", icon='NONE')
    return{'FINISHED'}


def do_panel(self, context, event, func):
    wm = context.window_manager
    wm.popover(draw_func=func)
    return{'FINISHED'}


def pick_func(self, context, event, pie, panel):
        loc = (event.mouse_region_x, event.mouse_region_y)

        if event.is_tablet:
            tablet = True
        else:
            tablet = False

        pie_mode = False if event.alt else True
        if pie_mode:
            do_pie(self, context, event, pie)
        else:
            do_panel(self, context, event, panel)


def sculpt_strokes_pie(self, context):
    ut_name = "sculpt_pie_strokes"
    settings = UT_SculptPieBase.paint_settings(context)
    mode = UT_SculptPieBase.get_brush_mode(context)
    brush = settings.brush

    pie = self.layout.menu_pie()
    pie.operator_context = 'INVOKE_DEFAULT'

    # LEFT
    pie.prop_enum(brush, "stroke_method", 'DOTS')

    # RIGHT
    pie.prop_enum(brush, "stroke_method", 'DRAG_DOT')

    # BOTTOM
    pie.prop_enum(brush, "stroke_method", 'SPACE')

    # TOP
    pie.popover(panel="VIEW3D_PT_tools_brush_stroke", text="Settings")

    # TOP LEFT
    pie.prop_enum(brush, "stroke_method", 'ANCHORED')

    # TOP RIGHT
    pie.prop_enum(brush, "stroke_method", 'LINE')

    # BOTTOM LEFT
    pie.prop_enum(brush, "stroke_method", 'CURVE')

    # BOTTOM RIGHT
    pie.prop_enum(brush, "stroke_method", 'AIRBRUSH')
    


def sculpt_strokes_panel(self, context):
    layout = self.layout
    settings = UT_SculptPieBase.paint_settings(context)
    mode = UT_SculptPieBase.get_brush_mode(context)
    brush = settings.brush

    col = layout.column()
    if brush.use_anchor:
        col.prop(brush, "use_edge_to_edge", text="Edge To Edge")

    if brush.use_airbrush:
        col.prop(brush, "rate", text="Rate", slider=True)

    if brush.use_space:
        row = col.row(align=True)
        row.prop(brush, "spacing", text="Spacing")
        row.prop(brush, "use_pressure_spacing", toggle=True, text="")

    if brush.use_line or brush.use_curve:
        row = col.row(align=True)
        row.prop(brush, "spacing", text="Spacing")

    if mode == 'SCULPT':
        col.row().prop(brush, "use_scene_spacing", text="Spacing Distance", expand=True)

    if mode in {'PAINT_TEXTURE', 'PAINT_2D', 'SCULPT'}:
        if brush.image_paint_capabilities.has_space_attenuation or brush.sculpt_capabilities.has_space_attenuation:
            col.prop(brush, "use_space_attenuation")

    if brush.use_curve:
        col.separator()
        col.template_ID(brush, "paint_curve", new="paintcurve.new")
        col.operator("paintcurve.draw")
        col.separator()

    if brush.use_space:
        col.separator()
        row = col.row(align=True)
        col.prop(brush, "dash_ratio", text="Dash Ratio")
        col.prop(brush, "dash_samples", text="Dash Length")

    if (mode == 'SCULPT' and brush.sculpt_capabilities.has_jitter) or mode != 'SCULPT':
        col.separator()
        row = col.row(align=True)
        if brush.jitter_unit == 'BRUSH':
            row.prop(brush, "jitter", slider=True)
        else:
            row.prop(brush, "jitter_absolute")
        row.prop(brush, "use_pressure_jitter", toggle=True, text="")
        col.row().prop(brush, "jitter_unit", expand=True)


def func_map():
    function_map = {
        "BRUSH": (),
        "STROKE": (sculpt_strokes_pie, sculpt_strokes_panel),
        "PLANE": (),
        "SYMM": (),
    }

class ATB_OT_SculptPie(bpy.types.Operator):
    """A pie menu for common sculpt settings"""
    bl_idname = "atb.sculpt_pie"
    bl_label = "ATB Sculpt Pie"
    bl_description = """Fancy Things"""
    bl_options = {'REGISTER'}

    mode_items = [
        ("BRUSH", "Brush", ""),
        ("STROKE", "Stroke", ""),
        ("PLANE", "Plane", ""),
        ("SYMM", "Symmetry", ""),
    ]

    mode: bpy.props.EnumProperty(
        items=mode_items,
        name="Mode",
        description="The invocation mode, used to select which sculpt functions are displayed",
        default='STROKE'
    )

    @classmethod
    def poll(cls, context):
        if context.mode == 'SCULPT':
            return True
        else:
            return False

    def invoke(self, context, event):
        self.loc = (event.mouse_region_x, event.mouse_region_y)

        if event.is_tablet:
            self.tablet = True
        else:
            self.tablet = False

        pick_func(self, context, event, sculpt_strokes_pie, sculpt_strokes_panel)
        return {'FINISHED'}
