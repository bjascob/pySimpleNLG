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
sys.path.append('../../..')
import unittest
from simplenlg.format.english.NumberedPrefix import *


class NumberedPrefixTest(unittest.TestCase):

    def testNewInstancePrefixIsZero(self):
        prefix = NumberedPrefix()
        self.assertEqual("0", prefix.getPrefix())

    def testIncrementFromNewInstanceIsOne(self):
        prefix =  NumberedPrefix()
        prefix.increment()
        self.assertEqual("1", prefix.getPrefix())

    def testIncrementForTwoPointTwoIsTwoPointThree(self):
        prefix = NumberedPrefix()
        prefix.setPrefix("2.2");
        prefix.increment();
        self.assertEqual("2.3", prefix.getPrefix())

    def testIncrementForThreePointFourPointThreeIsThreePointFourPointFour(self):
        prefix = NumberedPrefix()
        prefix.setPrefix("3.4.3")
        prefix.increment()
        self.assertEqual("3.4.4", prefix.getPrefix())

    def testUpALevelForNewInstanceIsOne(self):
        prefix = NumberedPrefix()
        prefix.upALevel()
        self.assertEqual("1", prefix.getPrefix())

    def testDownALevelForNewInstanceIsZero(self):
        prefix = NumberedPrefix()
        prefix.downALevel()
        self.assertEqual("0", prefix.getPrefix())


    def testDownALevelForSevenIsZero(self):
        prefix = NumberedPrefix()
        prefix.setPrefix("7")
        prefix.downALevel()
        self.assertEqual("0", prefix.getPrefix())

    def testDownALevelForTwoPointSevenIsTwo(self):
        prefix = NumberedPrefix()
        prefix.setPrefix("2.7")
        prefix.downALevel()
        self.assertEqual("2", prefix.getPrefix())

    def testDownALevelForThreePointFourPointThreeIsThreePointFour(self):
        prefix = NumberedPrefix()
        prefix.setPrefix("3.4.3")
        prefix.downALevel()
        self.assertEqual("3.4", prefix.getPrefix())


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
