# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2009-2010 Olivier Tilloy <olivier@tilloy.net>
#
# This file is part of the pyexiv2 distribution.
#
# pyexiv2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# pyexiv2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyexiv2; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, 5th Floor, Boston, MA 02110-1301 USA.
#
# Author: Olivier Tilloy <olivier@tilloy.net>
#
# ******************************************************************************

import unittest

from pyexiv2.exif import ExifTag, ExifValueError
from pyexiv2.utils import Rational

import datetime


class ImageMetadataMock(object):

    tags = {}

    def _set_exif_tag_value(self, key, value):
        self.tags[key] = value


class TestExifTag(unittest.TestCase):

    def test_convert_to_python_ascii(self):
        # Valid values: datetimes
        tag = ExifTag('Exif.Image.DateTime')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_python('2009-03-01 12:46:51'),
                         datetime.datetime(2009, 03, 01, 12, 46, 51))
        self.assertEqual(tag._convert_to_python('2009:03:01 12:46:51'),
                         datetime.datetime(2009, 03, 01, 12, 46, 51))
        self.assertEqual(tag._convert_to_python('2009-03-01T12:46:51Z'),
                         datetime.datetime(2009, 03, 01, 12, 46, 51))

        # Valid values: dates
        tag = ExifTag('Exif.GPSInfo.GPSDateStamp')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_python('2009:08:04'),
                         datetime.date(2009, 8, 4))

        # Valid values: strings
        tag = ExifTag('Exif.Image.Copyright')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_python('Some text.'), 'Some text.')
        self.assertEqual(tag._convert_to_python(u'Some text with exotic chàräctérʐ.'),
                         u'Some text with exotic chàräctérʐ.')

        # Invalid values: datetimes
        tag = ExifTag('Exif.Image.DateTime')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_python('2009-13-01 12:46:51'),
                         '2009-13-01 12:46:51')
        self.assertEqual(tag._convert_to_python('2009-12-01'), '2009-12-01')

        # Invalid values: dates
        tag = ExifTag('Exif.GPSInfo.GPSDateStamp')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_python('2009:13:01'), '2009:13:01')
        self.assertEqual(tag._convert_to_python('2009-12-01'), '2009-12-01')

    def test_convert_to_string_ascii(self):
        # Valid values: datetimes
        tag = ExifTag('Exif.Image.DateTime')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_string(datetime.datetime(2009, 03, 01, 12, 54, 28)),
                         '2009:03:01 12:54:28')
        self.assertEqual(tag._convert_to_string(datetime.date(2009, 03, 01)),
                         '2009:03:01 00:00:00')

        # Valid values: dates
        tag = ExifTag('Exif.GPSInfo.GPSDateStamp')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_string(datetime.date(2009, 03, 01)),
                         '2009:03:01')

        # Valid values: strings
        tag = ExifTag('Exif.Image.Copyright')
        self.assertEqual(tag.type, 'Ascii')
        self.assertEqual(tag._convert_to_string(u'Some text'), 'Some text')
        self.assertEqual(tag._convert_to_string(u'Some text with exotic chàräctérʐ.'),
                         'Some text with exotic chàräctérʐ.')
        self.assertEqual(tag._convert_to_string('Some text with exotic chàräctérʐ.'),
                         'Some text with exotic chàräctérʐ.')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, None)

    def test_convert_to_python_byte(self):
        # Valid values
        tag = ExifTag('Exif.GPSInfo.GPSVersionID')
        self.assertEqual(tag.type, 'Byte')
        self.assertEqual(tag._convert_to_python('D'), 'D')

    def test_convert_to_string_byte(self):
        # Valid values
        tag = ExifTag('Exif.GPSInfo.GPSVersionID')
        self.assertEqual(tag.type, 'Byte')
        self.assertEqual(tag._convert_to_string('Some text'), 'Some text')
        self.assertEqual(tag._convert_to_string(u'Some text'), 'Some text')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, None)

    def test_convert_to_python_sbyte(self):
        # Valid values
        tag = ExifTag('Exif.Pentax.Temperature')
        self.assertEqual(tag.type, 'SByte')
        self.assertEqual(tag._convert_to_python('15'), '15')

    def test_convert_to_string_sbyte(self):
        # Valid values
        tag = ExifTag('Exif.Pentax.Temperature')
        self.assertEqual(tag.type, 'SByte')
        self.assertEqual(tag._convert_to_string('13'), '13')
        self.assertEqual(tag._convert_to_string(u'13'), '13')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, None)

    def test_convert_to_python_short(self):
        # Valid values
        tag = ExifTag('Exif.Image.BitsPerSample')
        self.assertEqual(tag.type, 'Short')
        self.assertEqual(tag._convert_to_python('8'), 8)
        self.assertEqual(tag._convert_to_python('+5628'), 5628)

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, 'abc')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5,64')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '47.0001')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '1E3')

    def test_convert_to_string_short(self):
        # Valid values
        tag = ExifTag('Exif.Image.BitsPerSample')
        self.assertEqual(tag.type, 'Short')
        self.assertEqual(tag._convert_to_string(123), '123')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, -57)
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 'invalid')
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 3.14)

    def test_convert_to_python_long(self):
        # Valid values
        tag = ExifTag('Exif.Image.ImageWidth')
        self.assertEqual(tag.type, 'Long')
        self.assertEqual(tag._convert_to_python('8'), 8)
        self.assertEqual(tag._convert_to_python('+5628'), 5628)

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, 'abc')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5,64')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '47.0001')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '1E3')

    def test_convert_to_string_long(self):
        # Valid values
        tag = ExifTag('Exif.Image.ImageWidth')
        self.assertEqual(tag.type, 'Long')
        self.assertEqual(tag._convert_to_string(123), '123')
        self.assertEqual(tag._convert_to_string(678024), '678024')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, -57)
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 'invalid')
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 3.14)

    def test_convert_to_python_slong(self):
        # Valid values
        tag = ExifTag('Exif.OlympusCs.ManometerReading')
        self.assertEqual(tag.type, 'SLong')
        self.assertEqual(tag._convert_to_python('23'), 23)
        self.assertEqual(tag._convert_to_python('+5628'), 5628)
        self.assertEqual(tag._convert_to_python('-437'), -437)

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, 'abc')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5,64')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '47.0001')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '1E3')

    def test_convert_to_string_slong(self):
        # Valid values
        tag = ExifTag('Exif.OlympusCs.ManometerReading')
        self.assertEqual(tag.type, 'SLong')
        self.assertEqual(tag._convert_to_string(123), '123')
        self.assertEqual(tag._convert_to_string(678024), '678024')
        self.assertEqual(tag._convert_to_string(-437), '-437')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 'invalid')
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 3.14)

    def test_convert_to_python_rational(self):
        # Valid values
        tag = ExifTag('Exif.Image.XResolution')
        self.assertEqual(tag.type, 'Rational')
        self.assertEqual(tag._convert_to_python('5/3'), Rational(5, 3))

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, 'invalid')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '-5/3')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5 / 3')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5/-3')

    def test_convert_to_string_rational(self):
        # Valid values
        tag = ExifTag('Exif.Image.XResolution')
        self.assertEqual(tag.type, 'Rational')
        self.assertEqual(tag._convert_to_string(Rational(5, 3)), '5/3')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 'invalid')
        self.failUnlessRaises(ExifValueError,
                              tag._convert_to_string, Rational(-5, 3))

    def test_convert_to_python_srational(self):
        # Valid values
        tag = ExifTag('Exif.Image.BaselineExposure')
        self.assertEqual(tag.type, 'SRational')
        self.assertEqual(tag._convert_to_python('5/3'), Rational(5, 3))
        self.assertEqual(tag._convert_to_python('-5/3'), Rational(-5, 3))

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, 'invalid')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5 / 3')
        self.failUnlessRaises(ExifValueError, tag._convert_to_python, '5/-3')

    def test_convert_to_string_srational(self):
        # Valid values
        tag = ExifTag('Exif.Image.BaselineExposure')
        self.assertEqual(tag.type, 'SRational')
        self.assertEqual(tag._convert_to_string(Rational(5, 3)), '5/3')
        self.assertEqual(tag._convert_to_string(Rational(-5, 3)), '-5/3')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 'invalid')

    def test_convert_to_python_undefined(self):
        # Valid values
        tag = ExifTag('Exif.Photo.ExifVersion', '48 49 48 48 ')
        self.assertEqual(tag.type, 'Undefined')
        self.assertEqual(tag._convert_to_python('48 49 48 48 '), '1.00')

    def test_convert_to_string_undefined(self):
        # Valid values
        tag = ExifTag('Exif.Photo.ExifVersion')
        self.assertEqual(tag.type, 'Undefined')
        self.assertEqual(tag._convert_to_string('48 49 48 48 '), '48 49 48 48 ')
        self.assertEqual(tag._convert_to_string(u'48 49 48 48 '), '48 49 48 48 ')

        # Invalid values
        self.failUnlessRaises(ExifValueError, tag._convert_to_string, 3)

    def test_set_value_no_metadata(self):
        tag = ExifTag('Exif.Thumbnail.Orientation', 1) # top, left
        old_value = tag.value
        tag.value = 2
        self.failIfEqual(tag.value, old_value)

    def test_set_value_with_metadata(self):
        tag = ExifTag('Exif.Thumbnail.Orientation', 1) # top, left
        tag.metadata = ImageMetadataMock()
        old_value = tag.value
        tag.value = 2
        self.failIfEqual(tag.value, old_value)
        self.assertEqual(tag.metadata.tags[tag.key], '2')

