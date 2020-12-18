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
import time

def add_input(context, event):
    state = context.window_manager.ATB
    last = state.last_tap

    downtime = time.time() - 1608000000
    delta = downtime - last
    state.last_tap = downtime

    if state.combo_seq == "":
        cha = "q"
    else:
        if delta < state.quick_threshold:
            cha = "q"
        else:
            cha = "s"

    if event.pressure > state.hard_threshold:
        cha = cha.upper()

    state.combo_seq += cha
