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
from ctypes import *

# Handler type enum. Operator is 3
WM_HANDLER_TYPE_GIZMO = 1
WM_HANDLER_TYPE_UI = 2
WM_HANDLER_TYPE_OP = 3
WM_HANDLER_TYPE_DROPBOX = 4
WM_HANDLER_TYPE_KEYMAP = 5

# Generate listbase of appropriate type. None: generic
def listbase(type_=None):
    ptr = POINTER(type_)
    fields = ("first", ptr), ("last", ptr)
    return type("ListBase", (Structure,), {'_fields_': fields})

class wmOperatorType(Structure):
    pass

wmOperatorType._pack_ = True
wmOperatorType._fields_ = [
    ("name", c_char_p),
    ("idname", c_char_p),
]

class wmOperator(Structure):
    pass

class wmEventHandler(Structure):  # Generic
    pass

wmEventHandler._pack_ = True
wmEventHandler._fields_ = [
    ("next", POINTER(wmEventHandler)),
    ("prev", POINTER(wmEventHandler)),
    ("type", c_int),  # Enum
    ("flag", c_char),
    ("wmKeyMap", c_void_p),
    ("bblocal", c_void_p),
    ("bbwin", c_void_p),
    ("op", POINTER(wmOperator)),
]

class wmWindow(Structure):
    pass
   
class wmTabletData(Structure):
    pass

wmTabletData._pack_ = True
wmTabletData._fields_ = [
    ("active", c_int),
    ("pressure", c_float),
    ("x_tilt", c_float),
    ("y_tilt", c_float),
    ("is_motion_absolute", c_char)
]

class wmEvent(Structure):
    pass

wmEvent._pack_ = True
wmEvent._fields_ = [
    ("next", POINTER(wmEvent)),
    ("prev", POINTER(wmEvent)),
    ("type", c_short),
    ("val", c_short),
    ("x", c_int),
    ("y", c_int),
    ("is_repeat", c_char),
    ("prevtype", c_short),
    ("prevval", c_short),
    ("tablet", wmTabletData)
]

class OpContext(Structure):
    _fields_ = [
        ("win", POINTER(wmWindow)),
        ("area", c_void_p),  # <-- ScrArea ptr
        ("region", c_void_p),  # <-- ARegion ptr
        ("region_type", c_short),
    ]

class wmEventHandler_Op(Structure):  # Operator
    _fields_ = [
        ("head", wmEventHandler),
        ("op", POINTER(wmOperator)),  # <-- wmOperator
        ("is_file_select", c_bool),
        ("context", OpContext),
    ]

wmWindow._pack_ = True
wmWindow._fields_ = [  # from DNA_windowmanager_types.h
    ("next", POINTER(wmWindow)),
    ("prev", POINTER(wmWindow)),
    ("ghostwin", c_void_p),
    ("gpuctx", c_void_p),
    ("parent", POINTER(wmWindow)),
    ("scene", c_void_p),
    ("new_scene", c_void_p),
    ("view_layer_name", c_char * 64),
    ("workspace_hook", c_void_p),
    ("global_areas", listbase(type_=None) * 3),
    ("screen", c_void_p),
    ("posx", c_short),
    ("posy", c_short),
    ("sizex", c_short),
    ("sizey", c_short),
    ("windowstate", c_short),
    ("monitor", c_short),
    ("active", c_short),
    ("cursor", c_short),
    ("lastcursor", c_short),
    ("modalcursor", c_short),
    ("grabcursor", c_short),
    ("addmousemove", c_short),
    ("winid", c_int),
    ("lock_pie_event", c_short),
    ("last_pie_event", c_short),
    ("eventstate", c_void_p),
    ("tweak", c_void_p),
    ("ime_data", c_void_p),
    ("queue", listbase(type_=wmEvent)),
    ("handlers", listbase(type_=None)),
    ("modalhandlers", listbase(type_=wmEventHandler_Op)),
    ("gesture", listbase(type_=None)),
    ("stereo3d_format", c_void_p),
    ("drawcalls", listbase(type_=None)),
    ("cursor_keymap_status", c_void_p),
]

wmOperator._pack_ = True
wmOperator._fields_ = [
    ("next", POINTER(wmOperator)),
    ("prev", POINTER(wmOperator)),
    ("type", POINTER(wmOperatorType)),
    ("idname", c_char_p),
    ("name", c_char_p),
]

def isModalRunning():
    window = bpy.context.window
    w = cast(window.as_pointer(), POINTER(wmWindow)).contents

    handle = w.modalhandlers.first

    if handle.contents.head.type == 3:
        return True
    else:
        return False

def peekKeyQueue():
    window = bpy.context.window
    w = cast(window.as_pointer(), POINTER(wmWindow)).contents
    key = w.queue.first

    if key:
        return key.contents.type
    else:
        return -1

def isTablet():
    window = bpy.context.window
    w = cast(window.as_pointer(), POINTER(wmWindow)).contents
    key = w.queue.first

    if key:
        if key.contents.tablet.is_motion_absolute:
            return 1
    else:
        return -1