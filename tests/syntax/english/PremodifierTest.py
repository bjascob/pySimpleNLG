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
from simplenlg.features         import Feature, Tense
from simplenlg.framework        import NLGFactory
from simplenlg.lexicon          import Lexicon
from simplenlg.phrasespec       import *
from simplenlg.realiser.english import Realiser

class PremodifierTest(unittest.TestCase):
    # @Before
    def setUp(self):
        self.lexicon = Lexicon.getDefaultLexicon()
        self.phraseFactory = NLGFactory(self.lexicon)
        self.realiser = Realiser(self.lexicon)

    # Test change from "a" to "an" in the presence of a premodifier with a vowel
    def testIndefiniteWithPremodifier(self):
        s = self.phraseFactory.createClause("there", "be")
        s.setFeature(Feature.TENSE, Tense.PRESENT)
        np = self.phraseFactory.createNounPhrase("a", "stenosis")
        s.setObject(np)
        # check without modifiers -- article should be "a"
        self.assertEqual("there is a stenosis", self.realiser.realise(s).getRealisation())
        # add a single modifier -- should turn article to "an"
        np.addPreModifier(self.phraseFactory.createAdjectivePhrase("eccentric"))
        self.assertEqual("there is an eccentric stenosis", self.realiser.realise(s).getRealisation())

    # Test for comma separation between premodifers
    def testMultipleAdjPremodifiers(self):
        np = self.phraseFactory.createNounPhrase("a", "stenosis")
        np.addPreModifier(self.phraseFactory.createAdjectivePhrase("eccentric"))
        np.addPreModifier(self.phraseFactory.createAdjectivePhrase("discrete"))
        self.assertEqual("an eccentric, discrete stenosis", self.realiser.realise(np).getRealisation())

    # Test for comma separation between verb premodifiers
    def testMultipleAdvPremodifiers(self):
        adv1 = self.phraseFactory.createAdverbPhrase("slowly")
        adv2 = self.phraseFactory.createAdverbPhrase("discretely")
        # case 1: concatenated premods: should have comma
        vp = self.phraseFactory.createVerbPhrase("run")
        vp.addPreModifier(adv1)
        vp.addPreModifier(adv2)
        self.assertEqual("slowly, discretely runs", self.realiser.realise(vp).getRealisation())
        # case 2: coordinated premods: no comma
        vp2 = self.phraseFactory.createVerbPhrase("eat")
        vp2.addPreModifier(self.phraseFactory.createCoordinatedPhrase(adv1, adv2))
        self.assertEqual("slowly and discretely eats", self.realiser.realise(vp2).getRealisation())

if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
