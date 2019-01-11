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
from simplenlg.features.Feature             import *
from simplenlg.features.Form                import *
from simplenlg.features.LexicalFeature      import *
from simplenlg.features.Gender              import *
from simplenlg.framework.DocumentElement    import *
from simplenlg.framework.NLGElement         import *
from simplenlg.framework.NLGFactory         import *
from simplenlg.framework.LexicalCategory    import *
from simplenlg.lexicon.Lexicon              import *
from simplenlg.phrasespec.NPPhraseSpec      import *
from simplenlg.phrasespec.PPPhraseSpec      import *
from simplenlg.phrasespec.SPhraseSpec       import *
from simplenlg.phrasespec.VPPhraseSpec      import *
from simplenlg.realiser.english.Realiser    import *


class RealiserTest(unittest.TestCase):

    def setUp(self):
        self.lexicon    = Lexicon.getDefaultLexicon()
        self.nlgFactory = NLGFactory(self.lexicon)
        self.realiser   = Realiser(self.lexicon)
        #self.realiser.setDebugMode(True)

    # Test the realization of List of NLGElements that is null
    def testEmptyNLGElementRealiser(self):
        elements = []
        realisedElements = self.realiser.realise(elements)
        # Expect emtpy listed returned:
        self.assertIsNotNone(realisedElements)
        self.assertEqual(0, len(realisedElements))

    # Test the realization of List of NLGElements that is null
    def testNullNLGElementRealiser(self):
        elements = None
        realisedElements = self.realiser.realise(elements)
        # Expect emtpy listed returned:
        self.assertIsNotNone(realisedElements)
        self.assertEqual(0, len(realisedElements))

    # Tests the realization of multiple NLGElements in a list.
    def testMultipleNLGElementListRealiser(self):
        # "The cat jumping on the counter."
        sentence1 = self.nlgFactory.createSentence()
        subject_1 = self.nlgFactory.createNounPhrase("the", "cat")
        verb_1 = self.nlgFactory.createVerbPhrase("jump")
        verb_1.setFeature(Feature.FORM, Form.PRESENT_PARTICIPLE)
        prep_1 = self.nlgFactory.createPrepositionPhrase()
        object_1 = self.nlgFactory.createNounPhrase()
        object_1.setDeterminer("the")
        object_1.setNoun("counter")
        prep_1.addComplement(object_1)
        prep_1.setPreposition("on")
        clause_1  = self.nlgFactory.createClause()
        clause_1.setSubject(subject_1)
        clause_1.setVerbPhrase(verb_1)
        clause_1.setObject(prep_1)
        sentence1.addComponent(clause_1)
        # "The dog running on the counter."
        sentence2 = self.nlgFactory.createSentence()
        subject_2 = self.nlgFactory.createNounPhrase("the", "dog")
        verb_2 = self.nlgFactory.createVerbPhrase("run")
        verb_2.setFeature(Feature.FORM, Form.PRESENT_PARTICIPLE)
        prep_2 = self.nlgFactory.createPrepositionPhrase()
        object_2 = self.nlgFactory.createNounPhrase()
        object_2.setDeterminer("the")
        object_2.setNoun("counter")
        prep_2.addComplement(object_2)
        prep_2.setPreposition("on")
        clause_2  = self.nlgFactory.createClause()
        clause_2.setSubject(subject_2)
        clause_2.setVerbPhrase(verb_2)
        clause_2.setObject(prep_2)
        sentence2.addComponent(clause_2)
        # Create test NLGElements to realize:
        elements = [sentence1, sentence2]
        realisedElements = self.realiser.realise(elements)
        #
        self.assertIsNotNone(realisedElements)
        self.assertEqual(2, len(realisedElements))
        self.assertEqual("The cat jumping on the counter.", realisedElements[0].getRealisation())
        self.assertEqual("The dog running on the counter.", realisedElements[1].getRealisation())

    # Tests the correct pluralization with possessives (GitHub issue #9)
    def testCorrectPluralizationWithPossessives(self):
        sisterNP = self.nlgFactory.createNounPhrase("sister")
        word = self.nlgFactory.createInflectedWord("Albert Einstein", LexicalCategory.NOUN)
        word.setFeature(LexicalFeature.PROPER, True)
        possNP = self.nlgFactory.createNounPhrase(word)
        possNP.setFeature(Feature.POSSESSIVE, True)
        sisterNP.setSpecifier(possNP)
        self.assertEqual("Albert Einstein's sister", self.realiser.realise(sisterNP).getRealisation())
        sisterNP.setPlural(True);
        self.assertEqual("Albert Einstein's sisters", self.realiser.realise(sisterNP).getRealisation())
        sisterNP.setPlural(False);
        possNP.setFeature(LexicalFeature.GENDER, Gender.MASCULINE)
        possNP.setFeature(Feature.PRONOMINAL, True)
        self.assertEqual("his sister", self.realiser.realise(sisterNP).getRealisation())
        sisterNP.setPlural(True);
        self.assertEqual("his sisters", self.realiser.realise(sisterNP).getRealisation())


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
