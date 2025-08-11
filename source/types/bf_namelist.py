# SPDX-License-Identifier: GPL-3.0-or-later

"""!
BFDS, Blender interfaces to FDS namelists.
"""

import logging
from bpy.types import Object, Scene, Material
from .. import config, utils
from .fds_list import FDSList, FDSNamelist
from .bf_exception import BFException, BFNotImported
from .bf_param import BFParam, BFParamOther

log = logging.getLogger(__name__)


class BFNamelist(BFParam):
    """!
    Blender representation of an FDS namelist group.
    """

    ## List of subclassess
    subclasses = list()
    ## Dict of subclassess by fds_label
    _subclasses_by_fds_label = dict()
    ## Dict of subclassess by cls name
    _subclasses_by_cls_name = dict()

    def __init__(self, element):
        ## FDS element represented by this class instance
        self.element = element
        ## My sub params, tuple of element instances of type BFParam
        self.bf_params = tuple(p(element=element) for p in self.bf_params)

    # inherit __str__(), __repr()__, __init_subclass__(), get_subclass()

    @classmethod
    def register(cls):
        super().register()
        # Indexes are used to link both the class and the instance
        # otherwise the references are changed when instancing
        cls._bf_param_idx_by_fds_label = dict()  # fds_label: index of param
        cls._bf_param_other_idx = None  # ... of type BFParamOther
        for i, p in enumerate(cls.bf_params):
            if p.fds_label:
                cls._bf_param_idx_by_fds_label[p.fds_label] = i
            elif issubclass(p, BFParamOther):
                cls._bf_param_other_idx = i

    @classmethod
    def has_bf_param(cls, bf_param):
        """!
        Check if bf_param (class) is in cls.bf_params.
        @param bf_param: parameter to be tested.
        @return True or False.
        """
        return bf_param in cls.bf_params

    def _get_bf_param(self, fds_label):
        """!
        Return bf_param (class or instance) by its fds_label.
        @param fds_label: FDS parameter to be obtained.
        @return BFParam or None.
        """
        i = self._bf_param_idx_by_fds_label.get(fds_label)
        if i is not None:
            return self.bf_params[i]

    def _get_bf_param_other(self):
        """!
        Return the reference of the other bf_param (class or instance).
        """
        if self._bf_param_other_idx is not None:
            return self.bf_params[self._bf_param_other_idx]

    # Override the following methods in child classes for different behaviours

    def get_active(self, context):
        """!
        Return True if self is active.
        """
        return True

    def get_exported(self, context):
        """!
        Return True if self is exported to FDS.
        """
        # Check if active
        if not self.get_active(context):
            return False
        # Check if bpy_export is True
        if self.bpy_export:
            return bool(getattr(self.element, self.bpy_export))
        return True

    def draw_header(self, context, layout, panel):
        """!
        Draw my header on layout.
        @param context: the Blender context.
        @param layout: the Blender panel layout.
        @param panel: the calling panel.
        """
        if self.bpy_export:
            layout.prop(self.element, self.bpy_export, icon_only=True)
        if self.description:
            panel.bl_label = f"FDS {self.label} ({self.description})"
        else:
            panel.bl_label = self.label

    def draw_operators(self, context, layout):
        """!
        Draw my operators on layout.
        @param context: the Blender context.
        @param layout: the Blender panel layout.
        @return used layout.
        """
        layout.label(text="None available")

    def draw(self, context, layout):
        """!
        Draw my UI on layout.
        @param context: the Blender context.
        @param layout: the Blender panel layout.
        @return used layout.
        """
        # Check and active
        try:
            self.check(context)
        except BFException:
            layout.alert = True
        layout.active = self.get_exported(context)
        # Parameters
        col = layout.column()
        for p in self.bf_params:
            p.draw(context, col)
        return col

    def set_appearance(self, context):
        """!
        Set the default appearance of self.element in Blender.
        """
        pass  # Set appearance of self.element in subclasses

    def to_fds_list(self, context) -> FDSList:
        """!
        Return the FDSList instance from self, never None.
        """
        if not self.get_exported(context):
            return FDSList()
        self.check(context)
        if self.fds_label:
            return FDSNamelist(
                fds_label=self.fds_label,
                iterable=(
                    bf_param.to_fds_list(context)
                    for bf_param in self.bf_params
                    if bf_param
                ),
            )
        return FDSList()

    def from_fds_list(self, context, fds_list, fds_label=None):
        """!
        Set self.bf_params value, on error raise BFException.
        @param context: the Blender context.
        @param fds_list: instance of type FDSList, that contains BFParam instances.
        @param fds_label: if set, import only self.bf_params with fds_label
        """
        for fds_param in fds_list.get_fds_params(fds_label=fds_label, remove=True):
            is_imported = False

            # Try managed bf_param
            bf_param = self._get_bf_param(fds_label=fds_param.fds_label)
            if not is_imported and bf_param:
                try:
                    bf_param.set_value(context=context, value=fds_param.get_value())
                except BFNotImported as err:
                    utils.ui.write_bl_text(
                        context,
                        bl_text=context.scene.bf_config_text,
                        header="-- Import error",
                        texts=(str(err),),
                    )
                else:
                    bf_param.set_exported(context=context, value=True)
                    is_imported = True

            # Try bf_param_other
            bf_param_other = self._get_bf_param_other()
            if not is_imported and bf_param_other:
                try:
                    bf_param_other.set_value(context, value=fds_param.to_string())
                except BFNotImported as err:
                    utils.ui.write_bl_text(
                        context,
                        bl_text=context.scene.bf_config_text,
                        header="-- Import error",
                        texts=(str(err),),
                    )
                else:
                    is_imported = True

            # Raise if still not imported
            if not is_imported:
                raise BFException(self, f"Value {fds_param} not imported")

        # Set namelist exported and appearance
        self.set_exported(context, True)
        self.set_appearance(context)

    def copy_to(self, context, dest_element):
        """!
        Copy self values to destination element.
        @param dest_element: element of the same type of self.element.
        """
        log.debug(f"Copying <{self}> to <{dest_element.name}>")
        # self.bf_namelist_cls is copied by the operator
        if self.bpy_export:
            value = getattr(self.element, self.bpy_export)
            setattr(dest_element, self.bpy_export, value)
        for p in self.bf_params:
            p.copy_to(context=context, dest_element=dest_element)


class BFNamelistSc(BFNamelist):
    """!
    Blender representation of an FDS namelist group related to a Blender Scene.
    """

    bpy_type = Scene

    def set_appearance(self, context):
        if not config.SET_SCENE_APPEARANCE:
            return
        self.element.render.engine = "BLENDER_WORKBENCH"


class BFNamelistOb(BFNamelist):
    """!
    Blender representation of an FDS namelist group related to a Blender Object.
    """

    bpy_type = Object
    bpy_export = "hide_render"

    def get_exported(self, context):
        return not self.element.hide_render

    def set_exported(self, context, value=None):
        if value is None:
            self.element.hide_render = not self.bpy_export_default
        else:
            self.element.hide_render = not bool(value)

    def set_appearance(self, context):
        if not config.SET_OBJECT_APPEARANCE:
            return
        match self.bf_other.get("appearance"):
            case "BBOX":
                ob = self.element
                ob.display_type = "WIRE"
                ob.show_name = True
            case "WIRE":
                ob = self.element
                ob.display_type = "WIRE"
            case _:
                ob = self.element
                ob.display_type = "TEXTURED"
        # ob.show_in_front = show_in_front  # unused
        # ob.show_wire = show_wire  # unused

    def draw_header(self, context, layout, panel):
        ob = self.element
        # Manage temporary Object
        if ob.bf_is_tmp:
            panel.bl_label = "FDS Temporary Geometry"
            return
        # Manage all others
        if self.bpy_export:
            layout.prop(
                self.element,
                self.bpy_export,
                icon_only=True,
                toggle=False,
                invert_checkbox=True,
            )
        if self.description:
            panel.bl_label = f"FDS {self.label} ({self.description})"
        else:
            panel.bl_label = self.label

    def draw(self, context, layout):
        ob = self.element
        # Manage temporary Object
        if ob.bf_is_tmp:
            layout.operator("scene.bf_hide_fds_geometry", icon="HIDE_ON")
            return
        # Manage all others
        row = layout.row()
        if ob.bf_has_tmp:
            row.operator("scene.bf_hide_fds_geometry", icon="HIDE_ON")
        else:
            row.operator("object.bf_show_fds_geometry", icon="HIDE_OFF")
        row.operator("object.bf_show_fds_code", icon="HIDE_OFF")
        return super().draw(context, layout)


class BFNamelistMa(BFNamelist):
    """!
    Blender representation of an FDS namelist group related to a Blender Material.
    """

    bpy_type = Material

    def get_exported(self, context):
        if self.element.name in config.DEFAULT_MAS:
            return False  # default fds material
        elif self.element.bf_surf_export:
            return True  # user requested
        return False

    def set_appearance(self, context):
        if not config.SET_MATERIAL_APPEARANCE:
            return
        # This forces the use of diffuse_color for 3DView render
        self.element.use_nodes = False

    def draw_header(self, context, layout, panel):
        ma = self.element
        if self.bpy_export and ma.name not in config.DEFAULT_MAS:
            layout.prop(self.element, self.bpy_export, icon_only=True)
        if self.description:
            panel.bl_label = f"FDS {self.label} ({self.description})"
        else:
            panel.bl_label = self.label

    def draw(self, context, layout):
        ma = self.element
        layout.operator("material.bf_show_fds_code", icon="HIDE_OFF")
        # Manage default Materials
        if ma.name in config.DEFAULT_MAS:
            layout.label(text=f"Predefined {self.element.name} boundary condition")
            layout.prop(ma, "diffuse_color", text="RGB")
            return
        # Manage all others
        return super().draw(context, layout)
