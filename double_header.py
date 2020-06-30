
# Header Rendering
# def popover(self, context):
#     tool_settings = context.tool_settings
#     shading = context.space_data.shading
#     overlay = context.space_data.overlay
#     scene = bpy.context.scene

#     layout = self.layout

#     # Shading Type
#     col = layout.column(align=True)
#     pre_pre_row = col.row(align=True)
#     if not scene.snap_bool:
#         # row.prop(tool_settings, "use_snap", text="", toggle=True)
#         pre_pre_row.prop_enum(
#                               tool_settings,
#                               "snap_elements",
#                               text="",
#                               value='INCREMENT'
#         )
#         pre_pre_row.prop_enum(
#                               tool_settings,
#                               "snap_elements",
#                               text="",
#                               value='VERTEX'
#         )
#         pre_pre_row.prop_enum(
#                               tool_settings,
#                               "snap_elements",
#                               text="",
#                               value='EDGE'
#         )
#         pre_pre_row.prop_enum(
#                               tool_settings,
#                               "snap_elements",
#                               text="",
#                               value='FACE'
#         )
#         # row.prop(scene, "snap_bool", text="", icon="TRIA_LEFT")
#         pre_row = col.column(align=True)
#         pre_row.alignment = 'CENTER'
#         row = pre_row.row(align=True)
#         row.scale_y = 0.5
#         row.scale_x = 2
#         row.alignment = 'CENTER'
#         row.prop(scene, "snap_bool", text="", icon="TRIA_DOWN", expand=True)
#     if scene.snap_bool:
#         # row.prop(tool_settings, "use_snap", text="", toggle=True)
#         row = col.row(align=True)
#         row.prop_enum(
#                      tool_settings,
#                      "snap_elements",
#                      text="",
#                      value='INCREMENT'
#         )
#         row.prop_enum(
#                      tool_settings,
#                      "snap_elements",
#                      text="",
#                      value='VERTEX'
#         )
#         row.prop_enum(
#                      tool_settings,
#                      "snap_elements",
#                      text="",
#                      value='EDGE'
#         )
#         row.prop_enum(
#                      tool_settings,
#                      "snap_elements",
#                      text="",
#                      value='FACE'
#         )

#         subrow = col.row(align=True)
#         subrow.scale_x = 1
#         subrow.prop(tool_settings, "use_snap", text="", toggle=True)
#         subrow.prop_enum(
#                         tool_settings,
#                         "snap_elements",
#                         text="",
#                         value='EDGE_MIDPOINT'
#         )
#         subrow.prop_enum(
#                         tool_settings,
#                         "snap_elements",
#                         text="",
#                         value='EDGE_PERPENDICULAR'
#         )
#         subrow.prop_enum(
#                         tool_settings,
#                         "snap_elements",
#                         text="",
#                         value='VOLUME'
#         )
#         # subrow.prop(tool_settings, "snap_elements", text="")
#         pre_row = col.column(align=True)
#         pre_row.alignment = 'CENTER'
#         row = pre_row.row(align=True)
#         row.alignment = 'CENTER'
#         row.scale_y = 0.5
#         row.scale_x = 2
#         row.prop(scene, "snap_bool", text="", icon="TRIA_UP", expand=False)

#     box = layout.box()
#     col = box.column(align=True)
#     row = col.row(align=True)

#     row.prop_enum(
#                  tool_settings,
#                  "transform_pivot_point",
#                  text="",
#                  value='BOUNDING_BOX_CENTER'
#     )
#     row.prop_enum(
#                  tool_settings,
#                  "transform_pivot_point",
#                  text="",
#                  value='CURSOR'
#     )
#     row.prop(scene, "piv_bool", text="", icon="TRIA_DOWN")
#     if scene.piv_bool:
#         row = col.row(align=True)
#         row.prop_enum(
#                      tool_settings,
#                      "transform_pivot_point",
#                      text="",
#                      value='INDIVIDUAL_ORIGINS'
#         )
#         row.prop_enum(
#                      tool_settings,
#                      "transform_pivot_point",
#                      text="",
#                      value='MEDIAN_POINT'
#         )
#         row.prop_enum(
#                      tool_settings,
#                      "transform_pivot_point",
#                      text="",
#                      value='ATBIVE_ELEMENT'
#         )

#     col = layout.column(align=True)
#     row = col.row(align=True)
#     row.prop(shading, "show_xray", text="Xray", toggle=True, icon='XRAY')
#     row.popover('ATB_PT_HeaderButtons', text="", icon='NONE')
#     row = col.column(align=True)
#     row.scale_y = 0.65
#     if shading.show_xray:
#         row.prop(shading, "xray_alpha", text="")
#         row.prop(overlay, "backwire_opacity", text="")

#     col = layout.column(align=True)
#     row = col.row(align=True)
#     row.prop(
#             context.space_data,
#             "show_gizmo_object_translate",
#             text="",
#             icon='OBJECT_ORIGIN'
#     )
#     row.prop(
#             context.space_data,
#             "show_gizmo_object_rotate",
#             text="",
#             icon='ORIENTATION_GIMBAL'
#     )
#     row.prop(
#             context.space_data,
#             "show_gizmo_object_scale",
#             text="",
#             icon='STICKY_UVS_VERT'
#     )

#     # col = layout.column(align=True)
#     row = col.column(align=True)
#     row.alignment = 'RIGHT'
#     row.scale_x = 0.5
#     row.scale_y = 0.5
#     row.popover('VIEW3D_PT_gizmo_display', text="", icon='TRIA_DOWN')
