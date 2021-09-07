#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
'''
svgGuitarChord.py
Inkscape extension for rendering custom guitar chords.

Copyright (C) 2013 Pablo Fernández <pablo.fbus(a)gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

__version__ = "1.0"

import inkex
from lxml import etree

FINGERBOARD_WIDTH = 90
FRET_WIDTH = 32
GAP_STRINGS = 18


def frets_path(coordinates, lenth_in_frets):
    path = f'M {str(coordinates[0])} , {str(coordinates[1])} h {FINGERBOARD_WIDTH}'
    for s in range(lenth_in_frets):
        path += f'm -{FINGERBOARD_WIDTH},{FRET_WIDTH} h {FINGERBOARD_WIDTH}'
    return path


def strings_path(coordinates, length_in_frets):
    string_length = length_in_frets * FRET_WIDTH
    path = f'M {str(coordinates[0])}, {str(coordinates[1])} v {string_length} '
    for i in range(5):
        path += f'm {GAP_STRINGS},-{string_length} v {string_length} '
    return path


def create_grid(length_in_frets, coordinates):
    style = {
        'color': '#000000',
        'fill': 'none',
        'stroke': '#000000',
        'stroke-width': '1.6',
        'stroke-linecap': 'round',
    }
    path = f'{frets_path(coordinates, length_in_frets)} {strings_path(coordinates, length_in_frets)}'
    return {
        'd': path,
        'style': str(inkex.Style(style)),
    }


def create_nut(coordinates):
    style = {
        'color': '#a85632',
        'fill': 'none',
        'stroke': '#a85632',
        'stroke-width': '3.2',
        'stroke-linecap': 'round',
    }
    path = f'M {str(coordinates[0])}, {str(coordinates[1])} h {FINGERBOARD_WIDTH} '
    return {'d': path, 'style': str(inkex.Style(style))}


def create_header(coordinates):
    textstyle = {'font-size': '18',
                 'font-family': 'Libertinus Serif',
                 'text-anchor': 'middle',
                 'fill': '#000000'}
    return {'style': str(inkex.Style(textstyle)),
            'x': str(coordinates[0]), 'y': str(coordinates[1])}


def create_tuning_labels(coor):
    textstyle = {'font-size': '8',
                 'font-family': 'Libertinus Serif',
                 'text-anchor': 'middle',
                 'fill': '#000000'}
    tu = []
    for n in range(6):
        tu.append({'style': str(inkex.Style(textstyle)),
                   'x': str(coor[n][0]), 'y': str(coor[n][1])})
    return tu


def create_per_string_comments(coordinates, length_in_frets):
    textstyle = {'font-size': '10',
                 'font-family': 'Libertinus Serif',
                 'text-anchor': 'middle',
                 'fill': '#000000'}
    y_coordinate_comment = length_in_frets * FRET_WIDTH + 15
    comments_coordinates = []
    for i in range(6):
        comments_coordinates.append(
            {
                'style': str(inkex.Style(textstyle)),
                'x': str(coordinates[0] + GAP_STRINGS * i),
                'y': str(coordinates[1] + y_coordinate_comment),
            }
        )
    return comments_coordinates


def create_first_fret_label(coor):
    textstyle = {'font-size': '8', 'font-family': 'Latin Modern Roman',
                 'font-weight': 'bold', 'text-anchor': 'end', 'fill': '#000000'}
    return {'style': str(inkex.Style(textstyle)),
            'x': str(coor[0] - 7), 'y': str(coor[1] + 28)}


def fret_to_text(fret_number):
    romans = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
              'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI']
    return romans[fret_number - 1]


def create_capo_path(coordinates, upper_lef_corner_grid):
    style = {'color': '#000000', 'fill': 'none', 'stroke': '#000000',
             'stroke-width': '1.6', 'stroke-linecap': 'round'}
    length_string = upper_lef_corner_grid[1] - coordinates[1]
    path = f'M {str(coordinates[0])} , {str(coordinates[1])} v {length_string} m {GAP_STRINGS},-{length_string} v {length_string} m {GAP_STRINGS},-{length_string} v {length_string} m {GAP_STRINGS},-{length_string} v {length_string} m {GAP_STRINGS},-{length_string} v {length_string} m {GAP_STRINGS},-{length_string} v {length_string}'
    return {'d': path, 'style': str(inkex.Style(style))}


def create_capo_label(coor):
    textstyle = {'font-size': '8', 'font-family': 'Latin Modern Roman',
                 'font-weight': 'bold', 'text-anchor': 'end', 'fill': '#000000'}
    return {'style': str(inkex.Style(textstyle)),
            'x': str(coor[0] - 5), 'y': str(coor[1] + 4)}


def createXAt(coordinates):
    style = {'color': '#000000', 'fill': 'none', 'stroke': '#000000',
             'stroke-width': '1.1', 'stroke-linecap': 'round'}
    path = 'M ' + str(coordinates[0]) + ',' + str(coordinates[1]) + ' m 4,4 ' \
                                                                    'l -8,-8 M ' + str(coordinates[0]) + ',' + str(
        coordinates[1]) + '' \
                          'm -4,4 l 8,-8'
    return {'d': path, 'style': str(inkex.Style(style))}


def create0At(coor):
    style = {'color': '#000000', 'fill': 'none', 'stroke': '#000000',
             'stroke-width': '1.1', 'stroke-linecap': 'round'}
    path = 'M ' + str(coor[0]) + ',' + str(coor[1]) + ' m -4,0 ' \
                                                      'a 4,4 0 1, 0 8 0 a 4,4 0 1, 0 -8 0'
    return {'d': path, 'style': str(inkex.Style(style))}


def createStringPressedAt(coor):
    style = {'color': '#000000', 'fill': '#000000'}
    path = 'M ' + str(coor[0]) + ','+ str(coor[1]) + ' m -6,0 ' \
                                          'a 6,6 0 1, 0 12 0 a 6,6 0 1, 0 -12 0'
    return {'d': path, 'style': str(inkex.Style(style))}


def leftFingerNumberAt(coor):
    textstyle = {'font-size': '8', 'font-family': 'Latin Modern Roman',
                 'font-weight': 'bold', 'text-anchor': 'start', 'fill': '#000000'}
    return {'style': str(inkex.Style(textstyle)),
            'x': str(coor[0]), 'y': str(coor[1])}


def createBarreAt(bp, coor):
    style = {'color': '#000000', 'fill': 'none', 'stroke': '#000000',
             'stroke-width': '2', 'stroke-linecap': 'round'}
    path = 'M ' + str(coor[bp[0]][bp[1]][0]) + ',' \
           + str(coor[bp[0]][bp[1]][1]) + 'L' \
           + str(coor[bp[2]][bp[3]][0]) + ',' \
           + str(coor[bp[2]][bp[3]][1])
    return {'d': path, 'style': str(inkex.Style(style))}


class SVGGuitarChord(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("--tab", type=str, dest="tab")
        self.arg_parser.add_argument("--headerTrue", type=inkex.Boolean, default="True", dest="headerTrue")
        self.arg_parser.add_argument("--header", type=str, default="Em", dest="header")
        self.arg_parser.add_argument("--nFrets", type=int, dest="nFrets", default=4)
        self.arg_parser.add_argument("--firstFret", type=int, dest="firstFret", default=1)
        self.arg_parser.add_argument("--capoPos", type=str, default="No", dest="capoPos")
        self.arg_parser.add_argument("--tuningTrue", type=inkex.Boolean, default="False", dest="tuningTrue")
        self.arg_parser.add_argument("--tuning", type=str, default='E-A-D-G-B-E', dest="tuning")
        self.arg_parser.add_argument("--perStringCommentsTrue", type=inkex.Boolean, default="False",
                                     dest="perStringCommentsTrue")
        self.arg_parser.add_argument("--perStringComments", type=str, default='R-5-R-3-5-R', dest="perStringComments")
        self.arg_parser.add_argument("--leftFingerNumberTrue", type=inkex.Boolean, default="True",
                                     dest="leftFingerNumberTrue")
        self.arg_parser.add_argument("--firstStringFret", type=str, default='x', dest="firstStringFret")
        self.arg_parser.add_argument("--firstStringFinger", type=str, default='x', dest="firstStringFinger")
        self.arg_parser.add_argument("--secondStringFret", type=str, default='x', dest="secondStringFret")
        self.arg_parser.add_argument("--secondStringFinger", type=str, default='x', dest="secondStringFinger")
        self.arg_parser.add_argument("--thirdStringFret", type=str, default='x', dest="thirdStringFret")
        self.arg_parser.add_argument("--thirdStringFinger", type=str, default='x', dest="thirdStringFinger")
        self.arg_parser.add_argument("--fourthStringFret", type=str, default='x', dest="fourthStringFret")
        self.arg_parser.add_argument("--fourthStringFinger", type=str, default='x', dest="fourthStringFinger")
        self.arg_parser.add_argument("--fifthStringFret", type=str, default='x', dest="fifthStringFret")
        self.arg_parser.add_argument("--fifthStringFinger", type=str, default='x', dest="fifthStringFinger")
        self.arg_parser.add_argument("--sixthStringFret", type=str, default='x', dest="sixthStringFret")
        self.arg_parser.add_argument("--sixthStringFinger", type=str, default='x', dest="sixthStringFinger")
        self.upper_left_corner_grid = [30, 30]

    def add_grid_to_svg_tree(self):
        attribs_grid = create_grid(self.options.nFrets, self.upper_left_corner_grid)
        etree.SubElement(
            self.svg.get_current_layer(),
            inkex.addNS('path', 'svg'),
            attribs_grid,
        )
        # debug_text = etree.SubElement(
        #      self.svg.get_current_layer(),
        #      'text',
        #  )
        # debug_text.text = self.get_pressed_frets_on_strings() +'\n' +self.get_muted_strings() + '\n' + self.get_opened_strings()

    def add_nut_to_svg_tree(self):
        if self.options.firstFret == 1 and self.options.capoPos == 'No':
            attribs_nut = create_nut(self.upper_left_corner_grid)
            etree.SubElement(
                self.svg.get_current_layer(),
                inkex.addNS('path', 'svg'),
                attribs_nut,
            )

    def add_first_fret_label_to_svg_tree(self):
        is_visible = (
                             self.options.firstFret != 1 and self.options.capoPos == 'No'
                     ) or (
                             self.options.firstFret > self.capoPos2 + 1 and self.options.capoPos != 'No'
                     )
        if is_visible:
            attribs_firstFret = create_first_fret_label(self.upper_left_corner_grid)
            textFirstFret = etree.SubElement(self.svg.get_current_layer(),
                                             'text', attribs_firstFret)
            textFirstFret.text = fret_to_text(self.options.firstFret)

    def add_capo_label_to_svg_tree(self):
        if self.options.capoPos != 'No':
            attribs_capoPos = create_capo_label(self.capo_upper_left_corner_coordinates)
            textCapoPos = etree.SubElement(self.svg.get_current_layer(),
                                           'text', attribs_capoPos)
            textCapoPos.text = 'C ' + fret_to_text(self.capoPos2)

    def add_capo_path_to_svg_tree(self):
        if self.options.capoPos != 'No' and not (self.options.firstFret > self.capoPos2 + 1):
            attribs_capo1 = create_nut(self.capo_upper_left_corner_coordinates)
            etree.SubElement(self.svg.get_current_layer(),
                             inkex.addNS('path', 'svg'), attribs_capo1)
            attribs_capo2 = create_capo_path(self.capo_upper_left_corner_coordinates, self.upper_left_corner_grid)
            etree.SubElement(self.svg.get_current_layer(),
                             inkex.addNS('path', 'svg'), attribs_capo2)

    def add_chord_label_to_svg_tree(self):
        if self.options.headerTrue:
            attribs_header = create_header(self.header_coordinates)
            textHeader = etree.SubElement(self.svg.get_current_layer(),
                                          'text', attribs_header)
            textHeader.text = self.options.header

    def add_tuning_labels_to_svg_tree(self):
        if self.options.tuningTrue:
            attribs_tuning = create_tuning_labels(self.tuning_label_coordinates)
            tuning = self.options.tuning.split('-')
            try:
                for n in range(6):
                    textTuning = etree.SubElement(self.svg.get_current_layer(),
                                                  'text', attribs_tuning[n])
                    textTuning.text = tuning[n]
            except IndexError:
                inkex.debug("WARNING: Wrong tuning input.\nUse 5 hyphens to separate notes. Example: E-A-D-G-B-E")

    def add_string_comment_to_svg_tree(self):
        if self.options.perStringCommentsTrue:
            attribs_psComments = create_per_string_comments(self.upper_left_corner_grid, self.options.nFrets)
            perStringComments = self.options.perStringComments.split('-')
            try:
                for n in range(6):
                    textTuning = etree.SubElement(self.svg.get_current_layer(),
                                                  'text', attribs_psComments[n])
                    textTuning.text = perStringComments[n]
            except IndexError:
                inkex.debug("WARNING: Wrong comments input.\nUse 5 hyphens as separators. A blank space leaves\na string without a comment. Example: R-5-R- - -5")

    def add_mute_string_label_to_svg_tree(self):
        muted_strings = self.get_muted_strings()
        for string_number in muted_strings:
            attribs_x = createXAt(self.X0_label_coordinates(string_number))
            etree.SubElement(self.svg.get_current_layer(),
                             inkex.addNS('path', 'svg'), attribs_x)

    def add_open_string_label_to_svg_tree(self):
        opened_strings = self.get_opened_strings()
        for number in opened_strings:
            attribs_o = create0At(self.X0_label_coordinates(number))
            etree.SubElement(self.svg.get_current_layer(),
                             inkex.addNS('path', 'svg'), attribs_o)

    def add_pressed_fret_to_svg_tree(self):
        nStringFret = self.get_pressed_frets_on_strings()
        for ns, nf in nStringFret.items():
            attribs_stringPressed = createStringPressedAt(self.get_pressd_fret_coordinates(ns, nf))
            etree.SubElement(self.svg.get_current_layer(),
                             inkex.addNS('path', 'svg'), attribs_stringPressed)

    def add_left_hand_finger_lables_to_svg_tree(self):
        nStringFret = self.get_pressed_frets_on_strings()
        for string_number, finger_number in nStringFret.items():
            if self.options.leftFingerNumberTrue:
                attribs_leftFinger = leftFingerNumberAt(self.get_finger_label_coordinates(string_number, finger_number))
                textLeftFinger = etree.SubElement(self.svg.get_current_layer(),
                                                  'text', attribs_leftFinger)
                textLeftFinger.text = str(finger_number)


    @property
    def capo_upper_left_corner_coordinates(self):
        #  Coordinates of capo, if applicable
        ulc = list(self.upper_left_corner_grid)
        # Corrected coordinates if there is a Capo
        if self.options.capoPos != 'No' and not self.options.firstFret > self.capoPos2 + 1:
            ulc[1] = self.upper_left_corner_grid[1] - 10
        else:
            ulc[1] = self.upper_left_corner_grid[1]
        return ulc

    @property
    def header_coordinates(self):
        if self.options.tuningTrue:
            header_coordinates = (
                self.capo_upper_left_corner_coordinates[0] + 45,
                self.capo_upper_left_corner_coordinates[1] - 25,
            )
        else:
            header_coordinates = (
                self.capo_upper_left_corner_coordinates[0] + 45,
                self.capo_upper_left_corner_coordinates[1] - 15,
            )
        return header_coordinates

    @property
    def tuning_label_coordinates(self):
        label_margin = 15
        ct = []
        for i in range(6):
            ct.append(
                [
                    self.capo_upper_left_corner_coordinates[0] + i * GAP_STRINGS,
                    self.capo_upper_left_corner_coordinates[1] - label_margin,
                ]
            )
        return ct

    @property
    def strings_frets(self):
        return {
            1: self.options.firstStringFret,
            2: self.options.secondStringFret,
            3: self.options.thirdStringFret,
            4: self.options.fourthStringFret,
            5: self.options.fifthStringFret,
            6: self.options.sixthStringFret,
        }

    @property
    def strings_fingers(self):
        return {
            1: self.options.firstStringFinger,
            2: self.options.secondStringFinger,
            3: self.options.thirdStringFinger,
            4: self.options.fourthStringFinger,
            5: self.options.fifthStringFinger,
            6: self.options.sixthStringFinger,
        }
    def get_used_fingers(self):
       return {sn: int(f) for sn, f in self.strings_fingers.items() if f.isdigit()}

    def get_pressed_frets_on_strings(self):
        return {sn: int(sf) for sn, sf in self.strings_frets.items() if sf.isdigit() and sf != '0'}

    def get_muted_strings(self):
        return [sn for sn, sf in self.strings_frets.items() if sf == 'x']

    def get_opened_strings(self):
        return [sn for sn, sf in self.strings_frets.items() if sf == '0']

    def X0_label_coordinates(self, string_number):
        margin = 7
        x = self.capo_upper_left_corner_coordinates[0] + FINGERBOARD_WIDTH - (string_number - 1) * GAP_STRINGS
        y = self.capo_upper_left_corner_coordinates[1] - margin
        return [x, y]

    def get_pressd_fret_coordinates(self, number_string, number_fret):
        shift = 20
        x = self.upper_left_corner_grid[0] + FINGERBOARD_WIDTH - (number_string - 1) * GAP_STRINGS
        y = self.upper_left_corner_grid[1] + shift + (number_fret - 1) * FRET_WIDTH
        return [x, y]

    def get_finger_label_coordinates(self, number_string, number_finger):
        shift = 25
        x = self.upper_left_corner_grid[0] + FINGERBOARD_WIDTH - (number_string - 1) * GAP_STRINGS + 7
        y = self.upper_left_corner_grid[1] + shift + (number_finger - 1) * FRET_WIDTH + 5
        return [x, y]

    def effect(self):
        self.capoPos2 = int(self.options.capoPos) if self.options.capoPos != 'No' else 0

        # Possible coordinates of pressed strings
        #
        pfp = [
            [
                [self.upper_left_corner_grid[0] + 90, self.upper_left_corner_grid[1] + 20],
                [self.upper_left_corner_grid[0] + 90, self.upper_left_corner_grid[1] + 52],
                [self.upper_left_corner_grid[0] + 90, self.upper_left_corner_grid[1] + 84],
                [self.upper_left_corner_grid[0] + 90, self.upper_left_corner_grid[1] + 116],
                [self.upper_left_corner_grid[0] + 90, self.upper_left_corner_grid[1] + 148]
            ],
            [
                [self.upper_left_corner_grid[0] + 72, self.upper_left_corner_grid[1] + 20],
                [self.upper_left_corner_grid[0] + 72, self.upper_left_corner_grid[1] + 52],
                [self.upper_left_corner_grid[0] + 72, self.upper_left_corner_grid[1] + 84],
                [self.upper_left_corner_grid[0] + 72, self.upper_left_corner_grid[1] + 116],
                [self.upper_left_corner_grid[0] + 72, self.upper_left_corner_grid[1] + 148]
            ],
            [
                [self.upper_left_corner_grid[0] + 54, self.upper_left_corner_grid[1] + 20],
                [self.upper_left_corner_grid[0] + 54, self.upper_left_corner_grid[1] + 52],
                [self.upper_left_corner_grid[0] + 54, self.upper_left_corner_grid[1] + 84],
                [self.upper_left_corner_grid[0] + 54, self.upper_left_corner_grid[1] + 116],
                [self.upper_left_corner_grid[0] + 54, self.upper_left_corner_grid[1] + 148]
            ],
            [
                [self.upper_left_corner_grid[0] + 36, self.upper_left_corner_grid[1] + 20],
                [self.upper_left_corner_grid[0] + 36, self.upper_left_corner_grid[1] + 52],
                [self.upper_left_corner_grid[0] + 36, self.upper_left_corner_grid[1] + 84],
                [self.upper_left_corner_grid[0] + 36, self.upper_left_corner_grid[1] + 116],
                [self.upper_left_corner_grid[0] + 36, self.upper_left_corner_grid[1] + 148]
            ],
            [
                [self.upper_left_corner_grid[0] + 18, self.upper_left_corner_grid[1] + 20],
                [self.upper_left_corner_grid[0] + 18, self.upper_left_corner_grid[1] + 52],
                [self.upper_left_corner_grid[0] + 18, self.upper_left_corner_grid[1] + 84],
                [self.upper_left_corner_grid[0] + 18, self.upper_left_corner_grid[1] + 116],
                [self.upper_left_corner_grid[0] + 18, self.upper_left_corner_grid[1] + 148]
            ],
            [
                [self.upper_left_corner_grid[0], self.upper_left_corner_grid[1] + 20],
                [self.upper_left_corner_grid[0], self.upper_left_corner_grid[1] + 52],
                [self.upper_left_corner_grid[0], self.upper_left_corner_grid[1] + 84],
                [self.upper_left_corner_grid[0], self.upper_left_corner_grid[1] + 116],
                [self.upper_left_corner_grid[0], self.upper_left_corner_grid[1] + 148]
            ]
        ]

        # Fret and finger per string
        fretFinger = [{'fret': self.options.firstStringFret,
                       'finger': self.options.firstStringFinger},
                      {'fret': self.options.secondStringFret,
                       'finger': self.options.secondStringFinger},
                      {'fret': self.options.thirdStringFret,
                       'finger': self.options.thirdStringFinger},
                      {'fret': self.options.fourthStringFret,
                       'finger': self.options.fourthStringFinger},
                      {'fret': self.options.fifthStringFret,
                       'finger': self.options.fifthStringFinger},
                      {'fret': self.options.sixthStringFret,
                       'finger': self.options.sixthStringFinger}]

        # Barres
        stringBarre = []
        fretBarre = []
        for n in range(6):
            for m in range(n + 1, 6):
                if fretFinger[n]['fret'] != 'x' and fretFinger[n]['fret'] != '0' \
                        and fretFinger[n]['finger'] != 'x' \
                        and fretFinger[n]['finger'] == fretFinger[m]['finger']:
                    stringBarre.append(n)
                    stringBarre.append(m)
                    fretBarre.append(int(fretFinger[n]['fret']) - 1)
                    fretBarre.append(int(fretFinger[m]['fret']) - 1)
                    break
        zipped = list(zip(stringBarre, fretBarre))
        barres = []
        for n in range(0, len(stringBarre) - 1, 2):
            barres.append(zipped[n] + zipped[n + 1])

        self.add_grid_to_svg_tree()
        self.add_nut_to_svg_tree()
        self.add_first_fret_label_to_svg_tree()
        self.add_capo_label_to_svg_tree()
        self.add_capo_path_to_svg_tree()
        self.add_chord_label_to_svg_tree()
        self.add_tuning_labels_to_svg_tree()
        self.add_string_comment_to_svg_tree()
        self.add_mute_string_label_to_svg_tree()
        self.add_open_string_label_to_svg_tree()
        self.add_pressed_fret_to_svg_tree()
        self.add_left_hand_finger_lables_to_svg_tree()

        ## Create barre
        if len(barres) != 0:
            for n in range(len(barres)):
                attribs_barre = createBarreAt(barres[n], pfp)
                etree.SubElement(self.svg.get_current_layer(),
                                 inkex.addNS('path', 'svg'), attribs_barre)


#
if __name__ == '__main__':
    e = SVGGuitarChord()
    e.run()
