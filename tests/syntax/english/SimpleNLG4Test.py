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
from simplenlg.framework.NLGFactory      import *
from simplenlg.framework.PhraseElement   import *
from simplenlg.lexicon.XMLLexicon        import *
from simplenlg.lexicon.Lexicon           import *
from simplenlg.phrasespec.VPPhraseSpec   import *
from simplenlg.realiser.english.Realiser import *


# This class is the base class for all JUnit simplenlg.test cases for
# simplenlg. It sets up a a JUnit fixture, i.e. the basic objects (basic
# constituents) that all other tests can use.
class SimpleNLG4Test(unittest.TestCase):
    # Instantiates a new simplenlg test.
    def SimpleNLG4Test(self, name):
        super().__init__(name)

    # Set up the variables we'll need for this simplenlg.test to run
    # @Override @Before
    def setUp(self):
        self.lexicon = XMLLexicon()

        self.phraseFactory = NLGFactory(self.lexicon)
        self.realiser = Realiser(self.lexicon)

        self.man = self.phraseFactory.createNounPhrase("the", "man")
        self.woman = self.phraseFactory.createNounPhrase("the", "woman")
        self.dog = self.phraseFactory.createNounPhrase("the", "dog")
        self.boy = self.phraseFactory.createNounPhrase("the", "boy")

        self.beautiful = self.phraseFactory.createAdjectivePhrase("beautiful")
        self.stunning = self.phraseFactory.createAdjectivePhrase("stunning")
        self.salacious = self.phraseFactory.createAdjectivePhrase("salacious")

        self.onTheRock = self.phraseFactory.createPrepositionPhrase("on")
        self.np4 = self.phraseFactory.createNounPhrase("the", "rock")
        self.onTheRock.addComplement(self.np4)

        self.behindTheCurtain = self.phraseFactory.createPrepositionPhrase("behind")
        self.np5 = self.phraseFactory.createNounPhrase("the", "curtain")
        self.behindTheCurtain.addComplement(self.np5)

        self.inTheRoom = self.phraseFactory.createPrepositionPhrase("in")
        self.np6 = self.phraseFactory.createNounPhrase("the", "room")
        self.inTheRoom.addComplement(self.np6)

        self.underTheTable = self.phraseFactory.createPrepositionPhrase("under")
        self.underTheTable.addComplement(self.phraseFactory.createNounPhrase("the", "table"))

        self.proTest1 = self.phraseFactory.createNounPhrase("the", "singer")
        self.proTest2 = self.phraseFactory.createNounPhrase("some", "person")

        self.kick = self.phraseFactory.createVerbPhrase("kick")
        self.kiss = self.phraseFactory.createVerbPhrase("kiss")
        self.walk = self.phraseFactory.createVerbPhrase("walk")
        self.talk = self.phraseFactory.createVerbPhrase("talk")
        self.getUp = self.phraseFactory.createVerbPhrase("get up")
        self.fallDown = self.phraseFactory.createVerbPhrase("fall down")
        self.give = self.phraseFactory.createVerbPhrase("give")
        self.say = self.phraseFactory.createVerbPhrase("say")

    # @Override @After
    def tearDown(self):
        self.lexicon  = None
        self.realiser = None
        self.phraseFactory = None
        self.man = None
        self.woman = None
        self.dog = None
        self.boy = None
        self.np4 = None
        self.np5 = None
        self.np6 = None
        self.proTest1 = None
        self.proTest2 = None
        self.beautiful = None
        self.stunning = None
        self.salacious = None
        self.onTheRock = None
        self.behindTheCurtain= None
        self.inTheRoom = None
        self.underTheTable = None
        self.kick = None
        self.kiss = None
        self.walk = None
        self.talk = None
        self.getUp = None
        self.fallDown = None
        self.give = None
        self.say = None
