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
from simplenlg.features      import Feature, Tense
from simplenlg.framework     import DocumentElement, InflectedWordElement, LexicalCategory
from simplenlg.framework     import NLGElement, NLGFactory, StringElement, WordElement
from simplenlg.lexicon       import Lexicon, XMLLexicon
from simplenlg.phrasespec    import *
from simplenlg.realiser.english  import Realiser


class StandAloneExample(unittest.TestCase):
    def setUp(self):
        self.lexicon = XMLLexicon()
        self.nlgFactory = NLGFactory(self.lexicon)
        self.realiser = Realiser(self.lexicon)

    def testSentenceCreation(self):
        # create sentences
        thePark = self.nlgFactory.createNounPhrase("the", "park")
        bigp = self.nlgFactory.createAdjectivePhrase("big")
        bigp.setFeature(Feature.IS_COMPARATIVE, True)
        thePark.addModifier(bigp)
        # above relies on default placement rules.  You can force placement as a premodifier
        # (before head) by using addPreModifier
        toThePark = self.nlgFactory.createPrepositionPhrase("to")
        toThePark.setObject(thePark)
        # could also just say self.nlgFactory.createPrepositionPhrase("to", the Park)
        johnGoToThePark = self.nlgFactory.createClause("John", "go", toThePark)
        johnGoToThePark.setFeature(Feature.TENSE,Tense.PAST)
        johnGoToThePark.setFeature(Feature.NEGATED, True)
        # note that constituents (such as subject and object) are set with setXXX methods
        # while features are set with setFeature
        sentence = self.nlgFactory.createSentence(johnGoToThePark)
        # below creates a sentence DocumentElement by concatenating strings
        hePlayed = StringElement("he played")
        there = StringElement("there")
        football = WordElement("football")
        sentence2 = self.nlgFactory.createSentence()
        sentence2.addComponent(hePlayed)
        sentence2.addComponent(football)
        sentence2.addComponent(there)
        # now create a paragraph which contains these sentences
        paragraph = self.nlgFactory.createParagraph()
        paragraph.addComponent(sentence)
        paragraph.addComponent(sentence2)
        realised = self.realiser.realise(paragraph).getRealisation()
        # Test
        self.assertEqual("John did not go to the bigger park. He played football there.\n\n", realised)

    def testMorphology(self):
        # second example - using simplenlg just for morphology
        word = self.nlgFactory.createWord("child", LexicalCategory.NOUN)
        # create InflectedWordElement from word element
        inflectedWord = InflectedWordElement(word)
        # set the inflected word to plural
        inflectedWord.setPlural(True)
        # realise the inflected word
        realised = self.realiser.realise(inflectedWord).getRealisation()
        # Test
        self.assertEqual('children', realised)



if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
