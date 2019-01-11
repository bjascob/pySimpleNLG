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

from SimpleNLG4Test      import *
from simplenlg.features  import Feature
from simplenlg.framework import CoordinatedPhraseElement


# This class groups together some tests for prepositional phrases and
# coordinate prepositional phrases.
class PrepositionalPhraseTest(SimpleNLG4Test):
    # Basic test for the pre-set PP fixtures.
    def testBasic(self):
        self.assertEqual("in the room", self.realiser.realise(self.inTheRoom).getRealisation())
        self.assertEqual("behind the curtain", self.realiser.realise(self.behindTheCurtain).getRealisation())
        self.assertEqual("on the rock", self.realiser.realise(self.onTheRock).getRealisation())

    # Test for coordinate NP complements of PPs.
    def testComplementation(self):
        self.inTheRoom.clearComplements()
        self.inTheRoom.addComplement(CoordinatedPhraseElement( \
                self.phraseFactory.createNounPhrase("the", "room"),
                self.phraseFactory.createNounPhrase("a", "car")))
        self.assertEqual("in the room and a car", \
                self.realiser.realise(self.inTheRoom).getRealisation())

    # Test for PP coordination.
    def testCoordination(self):
        # simple coordination
        coord1 = CoordinatedPhraseElement(self.inTheRoom, self.behindTheCurtain)
        self.assertEqual("in the room and behind the curtain", \
                self.realiser.realise(coord1).getRealisation())
        # change the conjunction
        coord1.setFeature(Feature.CONJUNCTION, "or")
        self.assertEqual("in the room or behind the curtain", \
                self.realiser.realise(coord1).getRealisation())
        # new coordinate
        coord2 = CoordinatedPhraseElement(self.onTheRock, self.underTheTable)
        coord2.setFeature(Feature.CONJUNCTION, "or")
        self.assertEqual("on the rock or under the table", \
                self.realiser.realise(coord2).getRealisation())
        # coordinate two coordinates
        coord3 = CoordinatedPhraseElement(coord1,coord2)
        text = self.realiser.realise(coord3).getRealisation()
        self.assertEqual("in the room or behind the curtain and on the rock or under the table", text)


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
