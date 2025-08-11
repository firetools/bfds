# SPDX-FileCopyrightText: 2009-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Header, Menu
from bpy.app.translations import (
    pgettext_iface as iface_,
    pgettext_rpt as rpt_,
    contexts as i18n_contexts,
)
from bpy.types import VIEW3D_MT_editor_menus, VIEW3D_PT_overlay_bones


class VIEW3D_HT_header(Header):
    bl_space_type = "VIEW_3D"

    @staticmethod
    def draw_xform_template(layout, context):
        obj = context.active_object
        object_mode = "OBJECT" if obj is None else obj.mode
        has_pose_mode = (object_mode == "POSE") or (
            object_mode == "WEIGHT_PAINT" and context.pose_object is not None
        )

        tool_settings = context.tool_settings

        # Mode & Transform Settings
        scene = context.scene

        # Orientation
        if has_pose_mode or object_mode in {"OBJECT", "EDIT", "EDIT_GPENCIL"}:
            orient_slot = scene.transform_orientation_slots[0]
            row = layout.row(align=True)

            sub = row.row()
            sub.prop_with_popover(
                orient_slot,
                "type",
                text="",
                panel="VIEW3D_PT_transform_orientations",
            )

        # Pivot
        if has_pose_mode or object_mode in {
            "OBJECT",
            "EDIT",
            "EDIT_GPENCIL",
            "SCULPT_GREASE_PENCIL",
        }:
            layout.prop(tool_settings, "transform_pivot_point", text="", icon_only=True)

        # Snap
        show_snap = False
        if obj is None:
            show_snap = True
        else:
            if has_pose_mode or (
                object_mode
                not in {
                    "SCULPT",
                    "SCULPT_CURVES",
                    "VERTEX_PAINT",
                    "WEIGHT_PAINT",
                    "TEXTURE_PAINT",
                    "PAINT_GREASE_PENCIL",
                    "SCULPT_GREASE_PENCIL",
                    "WEIGHT_GREASE_PENCIL",
                    "VERTEX_GREASE_PENCIL",
                }
            ):
                show_snap = True
            else:

                paint_settings = UnifiedPaintPanel.paint_settings(context)

                if paint_settings:
                    brush = paint_settings.brush
                    if (
                        brush
                        and hasattr(brush, "stroke_method")
                        and brush.stroke_method == "CURVE"
                    ):
                        show_snap = True

        if show_snap:
            snap_items = bpy.types.ToolSettings.bl_rna.properties[
                "snap_elements"
            ].enum_items
            snap_elements = tool_settings.snap_elements
            if len(snap_elements) == 1:
                text = ""
                for elem in snap_elements:
                    icon = snap_items[elem].icon
                    break
            else:
                text = iface_("Mix", i18n_contexts.editor_view3d)
                icon = "NONE"
            del snap_items, snap_elements

            row = layout.row(align=True)
            row.prop(tool_settings, "use_snap", text="")

            sub = row.row(align=True)
            sub.popover(
                panel="VIEW3D_PT_snapping",
                icon=icon,
                text=text,
                translate=False,
            )

        # Proportional editing
        if (
            object_mode
            in {
                "EDIT",
                "PARTICLE_EDIT",
                "SCULPT_GREASE_PENCIL",
                "EDIT_GPENCIL",
                "OBJECT",
            }
            and context.mode != "EDIT_ARMATURE"
        ):
            row = layout.row(align=True)
            kw = {}
            if object_mode == "OBJECT":
                attr = "use_proportional_edit_objects"
            else:
                attr = "use_proportional_edit"

                if tool_settings.use_proportional_edit:
                    if tool_settings.use_proportional_connected:
                        kw["icon"] = "PROP_CON"
                    elif tool_settings.use_proportional_projected:
                        kw["icon"] = "PROP_PROJECTED"
                    else:
                        kw["icon"] = "PROP_ON"
                else:
                    kw["icon"] = "PROP_OFF"

            row.prop(tool_settings, attr, icon_only=True, **kw)
            sub = row.row(align=True)
            sub.active = getattr(tool_settings, attr)
            sub.prop_with_popover(
                tool_settings,
                "proportional_edit_falloff",
                text="",
                icon_only=True,
                panel="VIEW3D_PT_proportional_edit",
            )

        if object_mode == "EDIT" and obj.type == "GREASEPENCIL":
            draw_topbar_grease_pencil_layer_panel(context, layout)

    def draw(self, context):
        layout = self.layout

        tool_settings = context.tool_settings
        view = context.space_data
        shading = view.shading

        layout.row(align=True).template_header()

        row = layout.row(align=True)
        obj = context.active_object
        mode_string = context.mode
        object_mode = "OBJECT" if obj is None else obj.mode
        has_pose_mode = (object_mode == "POSE") or (
            object_mode == "WEIGHT_PAINT" and context.pose_object is not None
        )

        # Note: This is actually deadly in case enum_items have to be dynamically generated
        #       (because internal RNA array iterator will free everything immediately...).
        # XXX This is an RNA internal issue, not sure how to fix it.
        # Note: Tried to add an accessor to get translated UI strings instead of manual call
        #       to pgettext_iface below, but this fails because translated enum-items
        #       are always dynamically allocated.
        act_mode_item = bpy.types.Object.bl_rna.properties["mode"].enum_items[
            object_mode
        ]
        act_mode_i18n_context = bpy.types.Object.bl_rna.properties[
            "mode"
        ].translation_context

        sub = row.row(align=True)
        # BFDS
        # sub.operator_menu_enum(
        #     "object.mode_set",
        #     "mode",
        #     text=iface_(act_mode_item.name, act_mode_i18n_context),
        #     icon=act_mode_item.icon,
        # )
        sub.operator(
            "object.editmode_toggle",
            text=iface_(act_mode_item.name, act_mode_i18n_context),
            icon=act_mode_item.icon,
        )
        del act_mode_item

        layout.template_header_3D_mode()

        # Contains buttons like Mode, Pivot, Layer, Mesh Select Mode...
        if obj:
            # Particle edit
            if object_mode == "PARTICLE_EDIT":
                row = layout.row()
                row.prop(
                    tool_settings.particle_edit, "select_mode", text="", expand=True
                )
            elif object_mode in {"EDIT", "SCULPT_CURVES"} and obj.type == "CURVES":
                curves = obj.data

                row = layout.row(align=True)
                domain = curves.selection_domain
                row.operator(
                    "curves.set_selection_domain",
                    text="",
                    icon="CURVE_BEZCIRCLE",
                    depress=(domain == "POINT"),
                ).domain = "POINT"
                row.operator(
                    "curves.set_selection_domain",
                    text="",
                    icon="CURVE_PATH",
                    depress=(domain == "CURVE"),
                ).domain = "CURVE"

        # Grease Pencil
        if obj and obj.type == "GREASEPENCIL":
            # Select mode for Editing
            if object_mode == "EDIT":
                row = layout.row(align=True)
                row.operator(
                    "grease_pencil.set_selection_mode",
                    text="",
                    icon="GP_SELECT_POINTS",
                    depress=(tool_settings.gpencil_selectmode_edit == "POINT"),
                ).mode = "POINT"
                row.operator(
                    "grease_pencil.set_selection_mode",
                    text="",
                    icon="GP_SELECT_STROKES",
                    depress=(tool_settings.gpencil_selectmode_edit == "STROKE"),
                ).mode = "STROKE"
                row.operator(
                    "grease_pencil.set_selection_mode",
                    text="",
                    icon="GP_SELECT_BETWEEN_STROKES",
                    depress=(tool_settings.gpencil_selectmode_edit == "SEGMENT"),
                ).mode = "SEGMENT"

            if object_mode == "SCULPT_GREASE_PENCIL":
                row = layout.row(align=True)
                row.prop(tool_settings, "use_gpencil_select_mask_point", text="")
                row.prop(tool_settings, "use_gpencil_select_mask_stroke", text="")
                row.prop(tool_settings, "use_gpencil_select_mask_segment", text="")

            if object_mode == "VERTEX_GREASE_PENCIL":
                row = layout.row(align=True)
                row.prop(tool_settings, "use_gpencil_vertex_select_mask_point", text="")
                row.prop(
                    tool_settings, "use_gpencil_vertex_select_mask_stroke", text=""
                )
                row.prop(
                    tool_settings, "use_gpencil_vertex_select_mask_segment", text=""
                )

        overlay = view.overlay

        VIEW3D_MT_editor_menus.draw_collapsible(context, layout)

        layout.separator_spacer()

        if object_mode in {"PAINT_GREASE_PENCIL", "SCULPT_GREASE_PENCIL"}:
            # Grease pencil
            if object_mode == "PAINT_GREASE_PENCIL":
                sub = layout.row(align=True)
                sub.prop_with_popover(
                    tool_settings,
                    "gpencil_stroke_placement_view3d",
                    text="",
                    panel="VIEW3D_PT_grease_pencil_origin",
                )

            sub = layout.row(align=True)
            sub.active = tool_settings.gpencil_stroke_placement_view3d != "SURFACE"
            sub.prop_with_popover(
                tool_settings.gpencil_sculpt,
                "lock_axis",
                text="",
                panel="VIEW3D_PT_grease_pencil_lock",
            )

            draw_topbar_grease_pencil_layer_panel(context, layout)

            if object_mode == "PAINT_GREASE_PENCIL":
                # FIXME: this is bad practice!
                # Tool options are to be displayed in the top-bar.
                tool = context.workspace.tools.from_space_view3d_mode(object_mode)
                if tool and tool.idname == "builtin_brush.Draw":
                    settings = tool_settings.gpencil_sculpt.guide
                    row = layout.row(align=True)
                    row.prop(settings, "use_guide", text="", icon="GRID")
                    sub = row.row(align=True)
                    sub.active = settings.use_guide
                    sub.popover(
                        panel="VIEW3D_PT_grease_pencil_guide",
                        text="Guides",
                    )
            if object_mode == "SCULPT_GREASE_PENCIL":
                layout.popover(
                    panel="VIEW3D_PT_grease_pencil_sculpt_automasking",
                    text="",
                    icon=VIEW3D_HT_header._grease_pencil_sculpt_automasking_icon(
                        tool_settings.gpencil_sculpt
                    ),
                )

        elif object_mode == "SCULPT":
            # If the active tool supports it, show the canvas selector popover.
            from bl_ui.space_toolsystem_common import ToolSelectPanelHelper

            tool = ToolSelectPanelHelper.tool_active_from_context(context)

            is_paint_tool = False
            if tool.use_brushes:
                paint = tool_settings.sculpt
                brush = paint.brush
                if brush:
                    is_paint_tool = brush.sculpt_tool in {"PAINT", "SMEAR"}
            else:
                is_paint_tool = tool and tool.use_paint_canvas

            shading = VIEW3D_PT_shading.get_shading(context)
            color_type = shading.color_type

            row = layout.row()
            row.active = is_paint_tool and color_type == "VERTEX"

            if context.preferences.experimental.use_sculpt_texture_paint:
                canvas_source = tool_settings.paint_mode.canvas_source
                icon = (
                    "GROUP_VCOL"
                    if canvas_source == "COLOR_ATTRIBUTE"
                    else canvas_source
                )
                row.popover(panel="VIEW3D_PT_slots_paint_canvas", icon=icon)
                # TODO: Update this boolean condition so that the Canvas button is only active when
                # the appropriate color types are selected in Solid mode, I.E. 'TEXTURE'
                row.active = is_paint_tool
            else:
                row.popover(panel="VIEW3D_PT_slots_color_attributes", icon="GROUP_VCOL")

            layout.popover(
                panel="VIEW3D_PT_sculpt_snapping",
                icon="SNAP_INCREMENT",
                text="",
                translate=False,
            )

            layout.popover(
                panel="VIEW3D_PT_sculpt_automasking",
                text="",
                icon=VIEW3D_HT_header._sculpt_automasking_icon(tool_settings.sculpt),
            )

        elif object_mode == "VERTEX_PAINT":
            row = layout.row()
            row.popover(panel="VIEW3D_PT_slots_color_attributes", icon="GROUP_VCOL")
        elif object_mode == "VERTEX_GREASE_PENCIL":
            draw_topbar_grease_pencil_layer_panel(context, layout)
        elif object_mode == "WEIGHT_PAINT":
            row = layout.row()
            row.popover(panel="VIEW3D_PT_slots_vertex_groups", icon="GROUP_VERTEX")

            layout.popover(
                panel="VIEW3D_PT_sculpt_snapping",
                icon="SNAP_INCREMENT",
                text="",
                translate=False,
            )
        elif object_mode == "WEIGHT_GREASE_PENCIL":
            row = layout.row()
            row.popover(panel="VIEW3D_PT_slots_vertex_groups", icon="GROUP_VERTEX")
            draw_topbar_grease_pencil_layer_panel(context, row)

        elif object_mode == "TEXTURE_PAINT":
            tool_mode = tool_settings.image_paint.mode
            icon = "MATERIAL" if tool_mode == "MATERIAL" else "IMAGE_DATA"

            row = layout.row()
            row.popover(panel="VIEW3D_PT_slots_projectpaint", icon=icon)
            row.popover(
                panel="VIEW3D_PT_mask",
                icon=VIEW3D_HT_header._texture_mask_icon(tool_settings.image_paint),
                text="",
            )
        else:
            # Transform settings depending on tool header visibility
            VIEW3D_HT_header.draw_xform_template(layout, context)

        layout.separator_spacer()

        # Viewport Settings
        layout.popover(
            panel="VIEW3D_PT_object_type_visibility",
            icon_value=view.icon_from_show_object_viewport,
            text="",
        )

        # Gizmo toggle & popover.
        row = layout.row(align=True)
        # FIXME: place-holder icon.
        row.prop(view, "show_gizmo", text="", toggle=True, icon="GIZMO")
        sub = row.row(align=True)
        sub.active = view.show_gizmo
        sub.popover(
            panel="VIEW3D_PT_gizmo_display",
            text="",
        )

        # Overlay toggle & popover.
        row = layout.row(align=True)
        row.prop(overlay, "show_overlays", icon="OVERLAY", text="")
        sub = row.row(align=True)
        sub.active = overlay.show_overlays
        sub.popover(panel="VIEW3D_PT_overlay", text="")

        if mode_string == "EDIT_MESH":
            sub.popover(
                panel="VIEW3D_PT_overlay_edit_mesh", text="", icon="EDITMODE_HLT"
            )
        if mode_string == "EDIT_CURVE":
            sub.popover(
                panel="VIEW3D_PT_overlay_edit_curve", text="", icon="EDITMODE_HLT"
            )
        elif mode_string == "EDIT_CURVES":
            sub.popover(
                panel="VIEW3D_PT_overlay_edit_curves", text="", icon="EDITMODE_HLT"
            )
        elif mode_string == "SCULPT":
            sub.popover(
                panel="VIEW3D_PT_overlay_sculpt", text="", icon="SCULPTMODE_HLT"
            )
        elif mode_string == "SCULPT_CURVES":
            sub.popover(
                panel="VIEW3D_PT_overlay_sculpt_curves", text="", icon="SCULPTMODE_HLT"
            )
        elif mode_string == "PAINT_WEIGHT":
            sub.popover(
                panel="VIEW3D_PT_overlay_weight_paint", text="", icon="WPAINT_HLT"
            )
        elif mode_string == "PAINT_TEXTURE":
            sub.popover(
                panel="VIEW3D_PT_overlay_texture_paint", text="", icon="TPAINT_HLT"
            )
        elif mode_string == "PAINT_VERTEX":
            sub.popover(
                panel="VIEW3D_PT_overlay_vertex_paint", text="", icon="VPAINT_HLT"
            )
        elif obj is not None and obj.type == "GREASEPENCIL":
            sub.popover(
                panel="VIEW3D_PT_overlay_grease_pencil_options",
                text="",
                icon="OUTLINER_DATA_GREASEPENCIL",
            )

        # Separate from `elif` chain because it may coexist with weight-paint.
        if has_pose_mode or (
            object_mode in {"EDIT_ARMATURE", "OBJECT"}
            and VIEW3D_PT_overlay_bones.is_using_wireframe(context)
        ):
            sub.popover(panel="VIEW3D_PT_overlay_bones", text="", icon="POSE_HLT")

        row = layout.row()
        row.active = (object_mode == "EDIT") or (shading.type in {"WIREFRAME", "SOLID"})

        # While exposing `shading.show_xray(_wireframe)` is correct.
        # this hides the key shortcut from users: #70433.
        if has_pose_mode:
            draw_depressed = overlay.show_xray_bone
        elif shading.type == "WIREFRAME":
            draw_depressed = shading.show_xray_wireframe
        else:
            draw_depressed = shading.show_xray
        row.operator(
            "view3d.toggle_xray",
            text="",
            icon="XRAY",
            depress=draw_depressed,
        )

        row = layout.row(align=True)
        row.prop(shading, "type", text="", expand=True)
        sub = row.row(align=True)
        # TODO, currently render shading type ignores mesh two-side, until it's supported
        # show the shading popover which shows double-sided option.

        # sub.enabled = shading.type != 'RENDERED'
        sub.popover(panel="VIEW3D_PT_shading", text="")

    @staticmethod
    def _sculpt_automasking_icon(sculpt):
        automask_enabled = (
            sculpt.use_automasking_topology
            or sculpt.use_automasking_face_sets
            or sculpt.use_automasking_boundary_edges
            or sculpt.use_automasking_boundary_face_sets
            or sculpt.use_automasking_cavity
            or sculpt.use_automasking_cavity_inverted
            or sculpt.use_automasking_start_normal
            or sculpt.use_automasking_view_normal
        )

        return "CLIPUV_DEHLT" if automask_enabled else "CLIPUV_HLT"

    @staticmethod
    def _grease_pencil_sculpt_automasking_icon(gpencil_sculpt):
        automask_enabled = (
            gpencil_sculpt.use_automasking_stroke
            or gpencil_sculpt.use_automasking_layer_stroke
            or gpencil_sculpt.use_automasking_material_stroke
            or gpencil_sculpt.use_automasking_material_active
            or gpencil_sculpt.use_automasking_layer_active
        )

        return "CLIPUV_DEHLT" if automask_enabled else "CLIPUV_HLT"

    @staticmethod
    def _texture_mask_icon(ipaint):
        mask_enabled = ipaint.use_stencil_layer or ipaint.use_cavity
        return "CLIPUV_DEHLT" if mask_enabled else "CLIPUV_HLT"


class VIEW3D_MT_add(Menu):
    bl_label = "Add"
    bl_translation_context = i18n_contexts.operator_default
    bl_options = {"SEARCH_ON_KEY_PRESS"}

    def draw(self, context):
        layout = self.layout

        if layout.operator_context == "EXEC_REGION_WIN":
            layout.operator_context = "INVOKE_REGION_WIN"
            layout.operator(
                "WM_OT_search_single_menu", text="Search...", icon="VIEWZOOM"
            ).menu_idname = "VIEW3D_MT_add"
            layout.separator()

        # NOTE: don't use 'EXEC_SCREEN' or operators won't get the `v3d` context.

        # NOTE: was `EXEC_AREA`, but this context does not have the `rv3d`, which prevents
        #       "align_view" to work on first call (see #32719).
        layout.operator_context = "EXEC_REGION_WIN"

        # layout.operator_menu_enum("object.mesh_add", "type", text="Mesh", icon='OUTLINER_OB_MESH')
        layout.menu("VIEW3D_MT_mesh_add", icon="OUTLINER_OB_MESH")

        # BFDS
        # layout.operator_menu_enum("object.curve_add", "type", text="Curve", icon='OUTLINER_OB_CURVE')
        # layout.menu("VIEW3D_MT_curve_add", icon="OUTLINER_OB_CURVE")
        # layout.operator_menu_enum("object.surface_add", "type", text="Surface", icon='OUTLINER_OB_SURFACE')
        # layout.menu("VIEW3D_MT_surface_add", icon="OUTLINER_OB_SURFACE")
        # layout.menu("VIEW3D_MT_metaball_add", text="Metaball", icon="OUTLINER_OB_META")
        # layout.operator("object.text_add", text="Text", icon="OUTLINER_OB_FONT")
        # layout.operator(
        #     "object.pointcloud_random_add",
        #     text="Point Cloud",
        #     icon="OUTLINER_OB_POINTCLOUD",
        # )
        # layout.menu(
        #     "VIEW3D_MT_volume_add",
        #     text="Volume",
        #     text_ctxt=i18n_contexts.id_id,
        #     icon="OUTLINER_OB_VOLUME",
        # )
        # layout.menu(
        #     "VIEW3D_MT_grease_pencil_add",
        #     text="Grease Pencil",
        #     icon="OUTLINER_OB_GREASEPENCIL",
        # )

        # layout.separator()

        # if VIEW3D_MT_armature_add.is_extended():
        #     layout.menu("VIEW3D_MT_armature_add", icon="OUTLINER_OB_ARMATURE")
        # else:
        #     layout.operator(
        #         "object.armature_add", text="Armature", icon="OUTLINER_OB_ARMATURE"
        #     )

        # layout.operator(
        #     "object.add", text="Lattice", icon="OUTLINER_OB_LATTICE"
        # ).type = "LATTICE"

        # layout.separator()

        # layout.menu("VIEW3D_MT_empty_add", icon="OUTLINER_OB_EMPTY")
        # layout.menu("VIEW3D_MT_image_add", text="Image", icon="OUTLINER_OB_IMAGE")

        layout.operator("object.empty_add", text="Empty", icon="EMPTY_ARROWS").type = (
            "ARROWS"
        )
        layout.operator(
            "object.empty_add", text="Image", icon="OUTLINER_OB_IMAGE"
        ).type = "IMAGE"

        # layout.separator()

        # layout.menu("VIEW3D_MT_light_add", icon="OUTLINER_OB_LIGHT")
        # layout.menu("VIEW3D_MT_lightprobe_add", icon="OUTLINER_OB_LIGHTPROBE")

        # layout.separator()

        # if VIEW3D_MT_camera_add.is_extended():
        #     layout.menu("VIEW3D_MT_camera_add", icon="OUTLINER_OB_CAMERA")
        # else:
        #     VIEW3D_MT_camera_add.draw(self, context)

        # layout.separator()

        # layout.operator(
        #     "object.speaker_add", text="Speaker", icon="OUTLINER_OB_SPEAKER"
        # )

        # layout.separator()

        # layout.operator_menu_enum(
        #     "object.effector_add",
        #     "type",
        #     text="Force Field",
        #     icon="OUTLINER_OB_FORCE_FIELD",
        # )

        layout.separator()

        has_collections = bool(bpy.data.collections)
        col = layout.column()
        col.enabled = has_collections

        if not has_collections or len(bpy.data.collections) > 10:
            col.operator_context = "INVOKE_REGION_WIN"
            col.operator(
                "object.collection_instance_add",
                text=(
                    "Collection Instance..."
                    if has_collections
                    else "No Collections to Instance"
                ),
                icon="OUTLINER_OB_GROUP_INSTANCE",
            )
        else:
            col.operator_menu_enum(
                "object.collection_instance_add",
                "collection",
                text="Collection Instance",
                icon="OUTLINER_OB_GROUP_INSTANCE",
            )


class VIEW3D_MT_editor_menus(Menu):
    bl_label = ""

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        mode_string = context.mode
        edit_object = context.edit_object
        tool_settings = context.tool_settings

        layout.menu("VIEW3D_MT_view")

        # Select Menu
        if mode_string in {"PAINT_WEIGHT", "PAINT_VERTEX", "PAINT_TEXTURE"}:
            mesh = obj.data
            if mesh.use_paint_mask:
                layout.menu("VIEW3D_MT_select_paint_mask")
            elif mesh.use_paint_mask_vertex and mode_string in {
                "PAINT_WEIGHT",
                "PAINT_VERTEX",
            }:
                layout.menu("VIEW3D_MT_select_paint_mask_vertex")
        elif mode_string not in {
            "SCULPT",
            "SCULPT_CURVES",
            "PAINT_GREASE_PENCIL",
            "SCULPT_GREASE_PENCIL",
            "WEIGHT_GREASE_PENCIL",
            "VERTEX_GREASE_PENCIL",
        }:
            layout.menu("VIEW3D_MT_select_" + mode_string.lower())

        if mode_string == "OBJECT":
            layout.menu("VIEW3D_MT_add")
        elif mode_string == "EDIT_MESH":
            layout.menu(
                "VIEW3D_MT_mesh_add",
                text="Add",
                text_ctxt=i18n_contexts.operator_default,
            )
        elif mode_string == "EDIT_CURVE":
            layout.menu(
                "VIEW3D_MT_curve_add",
                text="Add",
                text_ctxt=i18n_contexts.operator_default,
            )
        elif mode_string == "EDIT_CURVES":
            layout.menu(
                "VIEW3D_MT_edit_curves_add",
                text="Add",
                text_ctxt=i18n_contexts.operator_default,
            )
        elif mode_string == "EDIT_SURFACE":
            layout.menu(
                "VIEW3D_MT_surface_add",
                text="Add",
                text_ctxt=i18n_contexts.operator_default,
            )
        elif mode_string == "EDIT_METABALL":
            layout.menu(
                "VIEW3D_MT_metaball_add",
                text="Add",
                text_ctxt=i18n_contexts.operator_default,
            )
        elif mode_string == "EDIT_ARMATURE":
            layout.menu(
                "TOPBAR_MT_edit_armature_add",
                text="Add",
                text_ctxt=i18n_contexts.operator_default,
            )

        if edit_object:
            layout.menu("VIEW3D_MT_edit_" + edit_object.type.lower())

            if mode_string == "EDIT_MESH":
                layout.menu("VIEW3D_MT_edit_mesh_vertices")
                layout.menu("VIEW3D_MT_edit_mesh_edges")
                layout.menu("VIEW3D_MT_edit_mesh_faces")
                # BFDS
                # layout.menu("VIEW3D_MT_uv_map", text="UV")
                layout.template_node_operator_asset_root_items()
            elif mode_string in {"EDIT_CURVE", "EDIT_SURFACE"}:
                layout.menu("VIEW3D_MT_edit_curve_ctrlpoints")
                layout.menu("VIEW3D_MT_edit_curve_segments")
            elif mode_string == "EDIT_POINTCLOUD":
                layout.template_node_operator_asset_root_items()
            elif mode_string == "EDIT_CURVES":
                layout.menu("VIEW3D_MT_edit_curves_control_points")
                layout.menu("VIEW3D_MT_edit_curves_segments")
                layout.template_node_operator_asset_root_items()
            elif mode_string == "EDIT_GREASE_PENCIL":
                layout.menu("VIEW3D_MT_edit_greasepencil_point")
                layout.menu("VIEW3D_MT_edit_greasepencil_stroke")
                layout.template_node_operator_asset_root_items()

        elif obj:
            if mode_string not in {
                "PAINT_TEXTURE",
                "SCULPT_CURVES",
                "SCULPT_GREASE_PENCIL",
                "VERTEX_GREASE_PENCIL",
            }:
                layout.menu("VIEW3D_MT_" + mode_string.lower())
            if mode_string == "SCULPT":
                layout.menu("VIEW3D_MT_mask")
                layout.menu("VIEW3D_MT_face_sets")
                layout.template_node_operator_asset_root_items()
            elif mode_string == "SCULPT_CURVES":
                layout.menu("VIEW3D_MT_select_sculpt_curves")
                layout.menu("VIEW3D_MT_sculpt_curves")
                layout.template_node_operator_asset_root_items()
            elif mode_string == "VERTEX_GREASE_PENCIL":
                layout.menu("VIEW3D_MT_select_edit_grease_pencil")
                layout.menu("VIEW3D_MT_paint_vertex_grease_pencil")
                layout.template_node_operator_asset_root_items()
            elif mode_string == "SCULPT_GREASE_PENCIL":
                is_selection_mask = (
                    tool_settings.use_gpencil_select_mask_point
                    or tool_settings.use_gpencil_select_mask_stroke
                    or tool_settings.use_gpencil_select_mask_segment
                )
                if is_selection_mask:
                    layout.menu("VIEW3D_MT_select_edit_grease_pencil")
                layout.template_node_operator_asset_root_items()
            else:
                layout.template_node_operator_asset_root_items()

        else:
            layout.menu("VIEW3D_MT_object")
            layout.template_node_operator_asset_root_items()


class VIEW3D_MT_object(Menu):
    bl_context = "objectmode"
    bl_label = "Object"

    def draw(self, context):
        layout = self.layout

        ob = context.object

        layout.menu("VIEW3D_MT_transform_object")
        layout.operator_menu_enum(
            "object.origin_set", text="Set Origin", property="type"
        )
        layout.menu("VIEW3D_MT_mirror")
        layout.menu("VIEW3D_MT_object_clear")
        layout.menu("VIEW3D_MT_object_apply")
        layout.menu("VIEW3D_MT_snap")

        layout.separator()

        layout.operator("object.duplicate_move")
        layout.operator("object.duplicate_move_linked")
        layout.operator("object.join")

        layout.separator()

        layout.operator("view3d.copybuffer", text="Copy Objects", icon="COPYDOWN")
        layout.operator("view3d.pastebuffer", text="Paste Objects", icon="PASTEDOWN")

        layout.separator()

        layout.menu("VIEW3D_MT_object_asset", icon="ASSET_MANAGER")
        layout.menu("VIEW3D_MT_object_collection")

        layout.separator()

        layout.menu("VIEW3D_MT_object_liboverride", icon="LIBRARY_DATA_OVERRIDE")
        layout.menu("VIEW3D_MT_object_relations")
        layout.menu("VIEW3D_MT_object_parent")
        layout.menu("VIEW3D_MT_object_modifiers", icon="MODIFIER")
        # BFDS
        # layout.menu("VIEW3D_MT_object_constraints", icon='CONSTRAINT')
        # layout.menu("VIEW3D_MT_object_track")
        layout.menu("VIEW3D_MT_make_links")

        layout.separator()

        # layout.operator("object.shade_smooth")
        # if ob and ob.type == "MESH":
        #    layout.operator("object.shade_auto_smooth")
        # layout.operator("object.shade_flat")

        # layout.separator()

        # layout.menu("VIEW3D_MT_object_animation")
        # layout.menu("VIEW3D_MT_object_rigid_body")

        # layout.separator()

        # layout.menu("VIEW3D_MT_object_quick_effects")

        # layout.separator()

        layout.menu("VIEW3D_MT_object_convert")

        layout.separator()

        layout.menu("VIEW3D_MT_object_showhide")
        layout.menu("VIEW3D_MT_object_cleanup")

        layout.separator()

        layout.operator_context = "EXEC_REGION_WIN"
        layout.operator("object.delete", text="Delete").use_global = False
        layout.operator("object.delete", text="Delete Global").use_global = True

        layout.template_node_operator_asset_menu_items(catalog_path="Object")
