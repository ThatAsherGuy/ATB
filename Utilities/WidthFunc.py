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


def get_breakpoints(region, thresholds, values):
    area = bpy.context.area
    resolution = bpy.context.preferences.system.ui_scale

    for reg in area.regions:
        if reg.type == region:
            region_width_raw = reg.width

    region_width = region_width_raw - 40
    region_width_int = round(region_width / (20 * resolution))

    count = [0, 1]
    count[0] = 0
    count[1] = region_width_int

    for i, val in enumerate(thresholds):
        if region_width_int >= thresholds[i]:
            count[0] = values[i]

    return count


def get_break_full(region, thresholds, values, comparison, half, is_num):
    """
    Count[0] = Normal return
    Count[1] = Half numeric return
    Count[2] = Normal return at half threshold
    Count[3] = Half numeric return at half threshold
    Count[4] = region_width_int
    Count[5] =
    """
    area = bpy.context.area
    resolution = bpy.context.preferences.system.ui_scale

    for reg in area.regions:
        if reg.type == region:
            region_width_raw = reg.width

    region_width = region_width_raw - 40
    region_width_int = round(region_width / (20 * resolution))
    region_width_float = round(region_width / (20 * resolution), 4)

    count = [0, 1, 2, 3, 4, 5]
    count[0] = 0
    count[1] = 0
    count[2] = 0
    count[3] = 0
    count[4] = region_width_int
    count[5] = region_width_float

    for i, val in enumerate(thresholds):
        if comparison == '>':
            if region_width_int > thresholds[i]:
                count[0] = values[i]
                if is_num:
                    count[1] = (values[i] / 2)
        if comparison == '<':
            if region_width_int < thresholds[i]:
                count[0] = values[i]
                if is_num:
                    count[1] = (values[i] / 2)
        if comparison == '==':
            if region_width_int == thresholds[i]:
                count[0] = values[i]
                if is_num:
                    count[1] = (values[i] / 2)
        if comparison == '>=':
            if region_width_int >= thresholds[i]:
                count[0] = values[i]
                if is_num:
                    count[1] = (values[i] / 2)
        if comparison == '<=':
            if region_width_int <= thresholds[i]:
                count[0] = values[i]
                if is_num:
                    count[1] = (values[i] / 2)

    if half:
        for i, val in enumerate(thresholds):
            if comparison == '>':
                if region_width_int > (thresholds[i] / 2):
                    count[2] = values[i]
                    if is_num:
                        count[3] = (values[i] / 2)
            if comparison == '<':
                if region_width_int < (thresholds[i] / 2):
                    count[2] = values[i]
                    if is_num:
                        count[3] = (values[i] / 2)
            if comparison == '==':
                if region_width_int == (thresholds[i] / 2):
                    count[2] = values[i]
                    if is_num:
                        count[3] = (values[i] / 2)
            if comparison == '>=':
                if region_width_int >= (thresholds[i] / 2):
                    count[2] = values[i]
                    if is_num:
                        count[3] = (values[i] / 2)
            if comparison == '<=':
                if region_width_int <= (thresholds[i] / 2):
                    count[2] = values[i]
                    if is_num:
                        count[3] = (values[i] / 2)

    return count


def get_width_factor(region, max, clip):
    area = bpy.context.area
    resolution = bpy.context.preferences.system.ui_scale

    for reg in area.regions:
        if reg.type == region:
            region_width_raw = reg.width

    region_width = region_width_raw - 40
    region_width_int = round(region_width / (20 * resolution))

    region_width_factor = round((region_width_int / max), 3)

    if clip:
        if region_width_factor > 1:
            region_width_factor = 1

    return region_width_factor


def check_width(region, threshold, type, max=440):
    area = bpy.context.area
    resolution = bpy.context.preferences.system.ui_scale

    for reg in area.regions:
        if reg.type == region:
            region_width_raw = reg.width

    # if not max:
    #     max = 440

    region_width = region_width_raw - 40
    region_width_int = round(region_width / (20 * resolution))
    region_width_factor = round((region_width_int / max), 3)

    width_type = [region_width, region_width_int, region_width_factor]
    result = [0, 1]
    result[1] = width_type

    if width_type[type] >= threshold:
        result[0] = True
        return result
    else:
        result[0] = False
        return result
