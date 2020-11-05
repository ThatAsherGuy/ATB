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



# 99% of this is ripped from Pie Menu editor, and 100% of it goes straight over my head. Get PME. It's awesome.
import bpy
import re
from itertools import islice
from ctypes import (
    Structure, POINTER, cast, addressof, pointer,
    c_short, c_uint, c_int, c_float, c_bool, c_char, c_char_p, c_void_p, c_double
)

BKE_ST_MAXNAME = 64
UI_MAX_DRAW_STR = 400
UI_MAX_NAME_STR = 128
UI_BLOCK_LOOP = 1 << 0
UI_BLOCK_KEEP_OPEN = 1 << 8
UI_BLOCK_POPUP = 1 << 9
UI_BLOCK_RADIAL = 1 << 20
UI_EMBOSS = 0

re_field = re.compile(r"(\*?)(\w+)([\[\d\]]+)?$")


def struct(name, bases=None):
    bases = ((Structure,) + bases) if bases else (Structure,)
    return type(name, bases, {})


def gen_fields(*args):
    ret = []
    cur_tp = None

    def parse_str(arg):
        mo = re_field.match(arg)
        p, f, n = mo.groups()
        tp = POINTER(cur_tp) if p else cur_tp

        if n:
            for n in reversed(re.findall(r"\[(\d+)\]", n)):
                tp *= int(n)

        ret.append((f, tp))

    bl_version = bpy.app.version
    for a in args:
        if isinstance(a, tuple):
            if a[0] and bl_version < a[1] or \
                    not a[0] and bl_version >= a[1]:
                continue

            cur_tp = a[2]
            for t_arg in islice(a, 3, None):
                parse_str(t_arg)

        elif isinstance(a, str):
            parse_str(a)

        else:
            cur_tp = a

    return ret


def gen_pointer(obj, tp=None):
    if not tp:
        tp = Link

    if obj is None or isinstance(obj, int):
        return cast(obj, POINTER(tp))
    else:
        return pointer(obj)


class _ListBase:
    def __len__(self):
        ret = 0
        link_lp = cast(self.first, POINTER(Link))
        while link_lp:
            ret += 1
            link_lp = link_lp.contents.next

        return ret

    def insert(self, prevlink, newlink):
        if prevlink:
            a = prevlink if isinstance(prevlink, int) else \
                addressof(prevlink)
            prevlink_p = cast(a, POINTER(Link)).contents
        else:
            prevlink_p = None

        if newlink:
            a = newlink if isinstance(newlink, int) else \
                addressof(newlink)
            newlink_p = cast(a, POINTER(Link)).contents
        else:
            newlink_p = None

        if not newlink_p:
            return

        if not self.first:
            self.first = self.last = addressof(newlink_p)
            return

        if not prevlink_p:
            newlink_p.prev = None
            newlink_p.next = gen_pointer(self.first)
            newlink_p.next.contents.prev = gen_pointer(newlink_p)
            self.first = addressof(newlink_p)
            return

        if self.last == addressof(prevlink_p):
            self.last = addressof(newlink_p)

        newlink_p.next = prevlink_p.next
        newlink_p.prev = gen_pointer(prevlink_p)
        prevlink_p.next = gen_pointer(newlink_p)
        if newlink_p.next:
            newlink_p.next.contents.prev = gen_pointer(newlink_p)

    def remove(self, link):
        if link:
            a = link if isinstance(link, int) else addressof(link)
            link_p = cast(a, POINTER(Link)).contents
        else:
            return

        if link_p.next:
            link_p.next.contents.prev = link_p.prev
        if link_p.prev:
            link_p.prev.contents.next = link_p.next

        if self.last == addressof(link_p):
            self.last = cast(link_p.prev, c_void_p)
        if self.first == addressof(link_p):
            self.first = cast(link_p.next, c_void_p)

    def find(self, idx):
        if idx < 0:
            return None

        link_lp = cast(self.first, POINTER(Link))
        for i in range(idx):
            link_lp = link_lp.contents.next

        return link_lp.contents if link_lp else None


ID = struct("ID")
Link = struct("Link")
ListBase = struct("ListBase", (_ListBase,))
rctf = struct("rctf")
rcti = struct("rcti")
uiItem = struct("uiItem")
uiLayout = struct("uiLayout")
uiLayoutRoot = struct("uiLayoutRoot")
uiStyle = struct("uiStyle")
uiFontStyle = struct("uiFontStyle")
uiBlock = struct("uiBlock")
uiBut = struct("uiBut")
vec2s = struct("vec2s")
ScrVert = struct("ScrVert")
ScrArea = struct("ScrArea")
ScrAreaMap = struct("ScrAreaMap")
ARegion = struct("ARegion")
bScreen = struct("bScreen")
bContext = struct("bContext")
bContext_wm = struct("bContext_wm")
bContext_data = struct("bContext_data")
wmWindow = struct("wmWindow")
wmEventHandler_KeymapFn = struct("wmEventHandler_KeymapFn")
wmEventHandler_Op = struct("wmEventHandler_Op")
wmEventHandler = struct("wmEventHandler")
wmOperator = struct("wmOperator")
wmEvent = struct("wmEvent")

# source/blender/makesdna/DNA_ID.h
ID._fields_ = gen_fields(
    c_void_p, "*next", "*prev",
    ID, "*newid",
    c_void_p, "*lib",
    c_char, "name[66]",
    c_short, "flag",
    c_int, "tag",
    c_int, "us",
    c_int, "icon_id",
    (True, (2, 80, 0), c_int, "icon_id"),
    (True, (2, 80, 0), c_int, "recalc"),
    (True, (2, 80, 0), c_int, "pad"),
    c_void_p, "*properties",
)

rcti._fields_ = gen_fields(
    c_int, "xmin", "xmax",
    c_int, "ymin", "ymax",
)

rctf._fields_ = gen_fields(
    c_float, 'xmin', 'xmax',
    c_float, 'ymin', 'ymax',
)

uiFontStyle._fields_ = gen_fields(
    c_short, "uifont_id",
    c_short, "points",
    c_short, "kerning",
    c_char, "word_wrap",
    c_char, "pad[5]",
    c_short, "italic", "bold",
    c_short, "shadow",
    c_short, "shadx", "shady",
    c_short, "align",
    c_float, "shadowalpha",
    c_float, "shadowcolor",
)

# source/blender/makesdna/DNA_listBase.h
Link._fields_ = gen_fields(
    Link, '*next', '*prev',
)

# source/blender/makesdna/DNA_listBase.h
ListBase._fields_ = gen_fields(
    c_void_p, "first", "last",
)

uiItem._fields_ = gen_fields(
    c_void_p, "*next", "*prev",
    c_int, "type",
    c_int, "flag",
)

uiLayout._fields_ = gen_fields(
    uiItem, "item",
    uiLayoutRoot, "*root",
    c_void_p, "*context",
    ListBase, "items",
    (True, (2, 80, 0), uiLayout, "*child_items_layout"),
    c_int, "x", "y", "w", "h",
    c_float, "scale[2]",
    c_short, "space",
    c_bool, "align",
    c_bool, "active",
    c_bool, "enabled",
    c_bool, "redalert",
    c_bool, "keepaspect",
    (True, (2, 80, 0), c_bool, "variable_size"),
    c_char, "alignment",
)

uiLayoutRoot._fields_ = gen_fields(
    uiLayoutRoot, "*next", "*prev",
    c_int, "type",
    c_int, "opcontext",
    c_int, "emw", "emh",
    c_int, "padding",
    c_void_p, "handlefunc",
    c_void_p, "*argv",
    uiStyle, "*style",
    uiBlock, "*block",
    uiLayout, "*layout",
)

uiStyle._fields_ = gen_fields(
    uiStyle, "*next", "*prev",
    c_char, "name[64]",
    uiFontStyle, "paneltitle",
    uiFontStyle, "grouplabel",
    uiFontStyle, "widgetlabel",
    uiFontStyle, "widget",
    c_float, "panelzoom",
    c_short, "minlabelchars",
    c_short, "minwidgetchars",
    c_short, "columnspace",
    c_short, "templatespace",
    c_short, "boxspace",
    c_short, "buttonspacex",
    c_short, "buttonspacey",
    c_short, "panelspace",
    c_short, "panelouter",
    c_short, "pad",
)

uiBlock._fields_ = gen_fields(
    uiBlock, "*next", "*prev",
    ListBase, "buttons",
    c_void_p, "*panel",
    uiBlock, "*oldblock",
    ListBase, "butstore",
    ListBase, "layouts",
    c_void_p, "*curlayout",
    ListBase, "contexts",
    c_char * UI_MAX_NAME_STR, "name",
    c_float, "winmat[4][4]",
    rctf, "rect",
    c_float, "aspect",
    c_uint, "puphash",
    c_void_p, "func",
    c_void_p, "*func_arg1",
    c_void_p, "*func_arg2",
    c_void_p, "funcN",
    c_void_p, "*func_argN",
    c_void_p, "butm_func",
    c_void_p, "*butm_func_arg",
    c_void_p, "handle_func",
    c_void_p, "*handle_func_arg",
    c_void_p, "*block_event_func",
    c_void_p, "*drawextra",
    c_void_p, "*drawextra_arg1",
    c_void_p, "*drawextra_arg2",
    c_int, "flag",
    # c_short, "alignnr",
    # c_short, "content_hints",
    # c_char, "direction",
    # c_char, "theme_style",
    # c_char, "dt",
)

uiBut._fields_ = gen_fields(
    uiBut, "*next", "*prev",
    c_int, "flag", "drawflag",
    c_int, "type",
    c_int, "pointype",
    c_short, "bit", "bitnr", "retval", "strwidth", "alignnr",
    c_short, "ofs", "pos", "selsta", "selend",
    c_char, "*str",
    c_char * UI_MAX_NAME_STR, "strdata",
    c_char * UI_MAX_DRAW_STR, "drawstr",
    rctf, "rect",
)

bContext_wm._fields_ = gen_fields(
    c_void_p, "*manager",
    c_void_p, "*window",
    (True, (2, 80, 0), c_void_p, "*workspace"),
    c_void_p, "*screen",
    ScrArea, "*area",
    ARegion, "*region",
    c_void_p, "*menu",
    (True, (2, 80, 0), c_void_p, "*gizmo_group"),
    c_void_p, "*store",
    c_char_p, "*operator_poll_msg",
)

bContext_data._fields_ = gen_fields(
    c_void_p, "*main",
    c_void_p, "*scene",
    c_int, "recursion",
    c_int, "py_init",
    c_void_p, "py_context",
)

bContext._fields_ = gen_fields(
    c_int, "thread",
    bContext_wm, "wm",
    bContext_data, "data",
)

vec2s._fields_ = gen_fields(
    c_short, "x", "y"
)

ScrVert._fields_ = gen_fields(
    ScrVert, "*next", "*prev", "*newv",
    vec2s, "vec"
)

# source/blender/makesdna/DNA_screen_types.h
ScrArea._fields_ = gen_fields(
    ScrArea, "*next", "*prev",
    ScrVert, "*v1", "*v2", "*v3", "*v4",
    c_void_p, "*full",
    rcti, "totrct",
    c_char, "spacetype", "butspacetype",
    (True, (2, 80, 0), c_short, "butspacetype_subtype"),
    c_short, "winx", "winy",
    (True, (2, 80, 0), c_char, "headertype"),
    (False, (2, 80, 0), c_short, "headertype"),
    (True, (2, 80, 0), c_char, "do_refresh"),
    (False, (2, 80, 0), c_short, "do_refresh"),
    c_short, "flag",
    c_short, "region_active_win",
    c_char, "temp", "pad",
    c_void_p, "*type",
    (True, (2, 80, 0), c_void_p, "*global"),
    ListBase, "spacedata",
)

# source/blender/makesdna/DNA_screen_types.h
ScrAreaMap._fields_ = gen_fields(
    ListBase, "vertbase",
    ListBase, "edgebase",
    ListBase, "areabase",
)

# source/blender/makesdna/DNA_screen_types.h
bScreen._fields_ = gen_fields(
    ID, "id",
    ListBase, "vertbase",
    ListBase, "edgebase",
    ListBase, "areabase",
    ListBase, "regionbase",
    c_void_p, "*scene",
    (False, (2, 80, 0), c_void_p, "*newscene"),
    (True, (2, 80, 0), c_short, "flag"),
    c_short, "winid",
    c_short, "redraws_flag",
    c_char, "temp",
)


wmEvent._fields_ = gen_fields(
    wmEvent, "*next", "*prev",
    c_short, "type",
    c_short, "val",
    c_int, "x", "y",
    c_int, "mval[2]",
    c_char, "utf8_buf[6]",
    c_char, "ascii",
    c_char, "pad",
    c_short, "prevtype",
    c_short, "prevval",
    c_int, "prevx", "prevy",
    c_double, "prevclicktime",
    c_int, "prevclickx", "prevclicky",
    c_short, "shift", "ctrl", "alt", "oskey",
    c_short, "keymodifier",
)


wmWindow._fields_ = gen_fields(
    wmWindow, "*next", "*prev",
    c_void_p, "*ghostwin",
    (True, (2, 80, 0), c_void_p, "*gpuctx"),
    (True, (2, 80, 0), wmWindow, "*parent"),
    (False, (2, 80, 0), bScreen, "*screen"),
    (False, (2, 80, 0), bScreen, "*newscreen"),
    (True, (2, 80, 0), c_void_p, "*scene"),
    (True, (2, 80, 0), c_void_p, "*new_scene"),
    (True, (2, 80, 0), c_char, "view_layer_name[64]"),
    (False, (2, 80, 0), c_char, "screenname[64]"),
    (True, (2, 80, 0), c_void_p, "*workspace_hook"),
    (True, (2, 80, 0), ScrAreaMap, "global_areas"),
    (True, (2, 80, 0), bScreen, "*screen"),
    c_short, "posx", "posy", "sizex", "sizey",
    c_short, "windowstate",
    c_short, "monitor",
    c_short, "active",
    c_short, "cursor",
    c_short, "lastcursor",
    c_short, "modalcursor",
    c_short, "grabcursor",
    c_short, "addmousemove",
    (False, (2, 80, 0), c_short, "multisamples"),
    (False, (2, 80, 0), c_short, "pad[3]"),
    (True, (2, 80, 0), c_short, "pad[4]"),
    c_int, "winid",
    c_short, "lock_pie_event",
    c_short, "last_pie_event",
    c_void_p, "*eventstate",
    (False, (2, 80, 0), c_void_p, "*curswin"),
    c_void_p, "*tweak",
    c_void_p, "*ime_data",
    (False, (2, 80, 0), c_int, "drawmethod", "drawfail"),
    (False, (2, 80, 0), ListBase, "drawdata"),
    ListBase, "queue",
    ListBase, "handlers",
    ListBase, "modalhandlers",
)

wmEventHandler_KeymapFn._fields_ = gen_fields(
    c_void_p, "*handle_post_fn",
    c_void_p, "*user_data"
)

wmEventHandler._fields_ = gen_fields(
    wmEventHandler, "*next", "*prev",
    c_int, "type",
    c_char, "flag",
    c_void_p, "*keymap",
    c_void_p, "*bblocal", "*bbwin",
    (True, (2, 80, 0), wmEventHandler_KeymapFn, "keymap_callback"),
    (True, (2, 80, 0), c_void_p, "*keymap_tool"),
    wmOperator, "*op",
)

wmEventHandler_Op._fields_ = gen_fields(
    wmEventHandler, "head",
    wmOperator, "*op",
    c_bool, "is_fileselect",    
)

wmOperator._fields_ = gen_fields(
    wmOperator, "*next", "*prev",
    c_char, "idname[64]",
)

del re_field
del struct
del gen_fields


# Handler type enum. Operator is 3
WM_HANDLER_TYPE_GIZMO = 1
WM_HANDLER_TYPE_UI = 2
WM_HANDLER_TYPE_OP = 3
WM_HANDLER_TYPE_DROPBOX = 4
WM_HANDLER_TYPE_KEYMAP = 5


def isModalRunning_Alt():
    window = bpy.context.window
    w = cast(window.as_pointer(), POINTER(wmWindow)).contents

    eh_pointer = POINTER(wmEventHandler_Op)
    handle = cast(w.modalhandlers.first, eh_pointer)

    return handle.contents.head.type

    # return int.from_bytes(handle.contents.head.type, byteorder='little')