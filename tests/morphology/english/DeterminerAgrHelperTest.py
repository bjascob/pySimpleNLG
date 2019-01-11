#!/usr/bin/python3
#
# The contents of this file are subject to the Mozilla Public License
# Version 1.1 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
# License for the specific language governing rights and limitations
# under the License.
#
# The Original Code is "Simplenlg".
#
# The Initial Developer of the Original Code is Ehud Reiter, Albert Gatt and Dave Westwater.
# Portions created by Ehud Reiter, Albert Gatt and Dave Westwater are
# Copyright (C) 2010-11 The University of Aberdeen. All Rights Reserved.
#
# Contributor(s): Ehud Reiter, Albert Gatt, Dave Wewstwater, Roman Kutlak, Margaret Mitchell.

import sys
import unittest
sys.path.append('../../..')
from simplenlg.morphology.english.DeterminerAgrHelper    import *


class DeterminerAgrHelperTest(unittest.TestCase):

    def testRequiresAn(self):
        self.assertTrue(DeterminerAgrHelper.requiresAn("elephant"))
        self.assertFalse(DeterminerAgrHelper.requiresAn("cow"))
        # Does not hand phonetics
        self.assertFalse(DeterminerAgrHelper.requiresAn("hour"))
        # But does have exceptions for some numerals
        self.assertFalse(DeterminerAgrHelper.requiresAn("one"))
        self.assertFalse(DeterminerAgrHelper.requiresAn("100"))

    def testCheckEndsWithIndefiniteArticle1(self):
        cannedText = "I see a"
        np = "elephant"
        expected = "I see an"
        actual = DeterminerAgrHelper.checkEndsWithIndefiniteArticle(cannedText, np)
        self.assertEqual(expected, actual)

    def testCheckEndsWithIndefiniteArticle2(self):
        cannedText = "I see a"
        np = "cow"
        expected = "I see a"
        actual = DeterminerAgrHelper.checkEndsWithIndefiniteArticle(cannedText, np)
        self.assertEqual(expected, actual)

    def testCheckEndsWithIndefiniteArticle3(self):
        cannedText = "I see an"
        np = "cow"
        # Does not handle "an" -> "a"
        expected = "I see an"
        actual = DeterminerAgrHelper.checkEndsWithIndefiniteArticle(cannedText, np)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
