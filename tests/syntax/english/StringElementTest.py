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
from simplenlg.framework     import CoordinatedPhraseElement, DocumentElement
from simplenlg.framework     import LexicalCategory, NLGElement, NLGFactory, StringElement
from simplenlg.lexicon       import Lexicon
from simplenlg.phrasespec    import NPPhraseSpec, SPhraseSpec
from simplenlg.realiser.english  import Realiser


# Tests for string elements as parts of larger phrases
class StringElementTest(unittest.TestCase):
    def setUp(self):
        self.lexicon = Lexicon.getDefaultLexicon()
        self.phraseFactory = NLGFactory(self.lexicon)
        self.realiser = Realiser(self.lexicon)

    # Test that string elements can be used as heads of NP
    def testStringElementAsHead(self):
        np = self.phraseFactory.createNounPhrase()
        np.setHead(self.phraseFactory.createStringElement("dogs and cats"))
        np.setSpecifier(self.phraseFactory.createWord("the", LexicalCategory.DETERMINER))
        self.assertEqual("the dogs and cats", self.realiser.realise(np).getRealisation())

    # Sentences whose VP is a canned string
    def testStringElementAsVP(self):
        s = self.phraseFactory.createClause()
        s.setVerbPhrase(self.phraseFactory.createStringElement("eats and drinks"))
        s.setSubject(self.phraseFactory.createStringElement("the big fat man"))
        self.assertEqual("the big fat man eats and drinks", self.realiser.realise(s).getRealisation())

    # Test for when the SPhraseSpec has a NPSpec added directly after it:
    # "Mary loves NP[the cow]."
    def testTailNPStringElement(self):
        senSpec = self.phraseFactory.createClause()
        senSpec.addComplement((self.phraseFactory.createStringElement("mary loves")))
        np = self.phraseFactory.createNounPhrase()
        np.setHead("cow")
        np.setDeterminer("the")
        senSpec.addComplement(np)
        completeSen = self.phraseFactory.createSentence()
        completeSen.addComponent(senSpec)
        self.assertEqual("Mary loves the cow.", self.realiser.realise(completeSen).getRealisation())

    # Test for a NP followed by a canned text: "NP[A cat] loves a dog".
    def testFrontNPStringElement(self):
        senSpec = self.phraseFactory.createClause()
        np = self.phraseFactory.createNounPhrase()
        np.setHead("cat")
        np.setDeterminer("the")
        senSpec.addComplement(np)
        senSpec.addComplement(self.phraseFactory.createStringElement("loves a dog"))
        completeSen = self.phraseFactory.createSentence()
        completeSen.addComponent(senSpec)
        self.assertEqual("The cat loves a dog.", \
            self.realiser.realise(completeSen).getRealisation())

    # Test for a StringElement followed by a NP followed by a StringElement
    # "The world loves NP[ABBA] but not a sore loser."
    def testMulitpleStringElements(self):
        senSpec = self.phraseFactory.createClause()
        senSpec.addComplement(self.phraseFactory.createStringElement("the world loves"))
        np = self.phraseFactory.createNounPhrase()
        np.setHead("ABBA")
        senSpec.addComplement(np)
        senSpec.addComplement(self.phraseFactory.createStringElement("but not a sore loser"))
        completeSen = self.phraseFactory.createSentence()
        completeSen.addComponent(senSpec)
        self.assertEqual("The world loves ABBA but not a sore loser.", \
                self.realiser.realise(completeSen).getRealisation())

    # Test for multiple NP phrases with a single StringElement phrase:
    # "NP[John is] a trier NP[for cheese]."
    def testMulitpleNPElements(self):
        senSpec = self.phraseFactory.createClause()
        frontNoun = self.phraseFactory.createNounPhrase()
        frontNoun.setHead("john")
        senSpec.addComplement(frontNoun)
        senSpec.addComplement(self.phraseFactory.createStringElement("is a trier"))
        backNoun = self.phraseFactory.createNounPhrase()
        backNoun.setDeterminer("for")
        backNoun.setNoun("cheese")
        senSpec.addComplement(backNoun)
        completeSen = self.phraseFactory.createSentence()
        completeSen.addComponent(senSpec)
        self.assertEqual("John is a trier for cheese.", \
                self.realiser.realise(completeSen).getRealisation())

    # White space check: Test to see how SNLG deals with additional whitespaces:
    # NP[The Nasdaq] rose steadily during NP[early trading], however it plummeted due to NP[a shock] after NP[IBM] announced poor
    # NP[first quarter results].
    def testWhiteSpaceNP(self):
        senSpec = self.phraseFactory.createClause()
        firstNoun = self.phraseFactory.createNounPhrase()
        firstNoun.setDeterminer("the")
        firstNoun.setNoun("Nasdaq")
        senSpec.addComplement(firstNoun)
        senSpec.addComplement(self.phraseFactory.createStringElement(" rose steadily during "))
        secondNoun = self.phraseFactory.createNounPhrase()
        secondNoun.setSpecifier("early")
        secondNoun.setNoun("trading")
        senSpec.addComplement(secondNoun)
        senSpec.addComplement(self.phraseFactory.createStringElement(" , however it plummeted due to"))
        thirdNoun = self.phraseFactory.createNounPhrase()
        thirdNoun.setSpecifier("a")
        thirdNoun.setNoun("shock")
        senSpec.addComplement(thirdNoun)
        senSpec.addComplement(self.phraseFactory.createStringElement(" after "))
        fourthNoun = self.phraseFactory.createNounPhrase()
        fourthNoun.setNoun("IBM")
        senSpec.addComplement(fourthNoun)
        senSpec.addComplement(self.phraseFactory.createStringElement("announced poor    "))
        fifthNoun = self.phraseFactory.createNounPhrase()
        fifthNoun.setSpecifier("first quarter")
        fifthNoun.setNoun("results")
        fifthNoun.setPlural(True)
        senSpec.addComplement(fifthNoun)
        completeSen = self.phraseFactory.createSentence()
        completeSen.addComponent(senSpec)
        correct = "The Nasdaq rose steadily during early trading, however it plummeted " \
                + "due to a shock after IBM announced poor first quarter results."
        self.assertEqual(correct,  self.realiser.realise(completeSen).getRealisation())

    # Point absorption test: Check to see if SNLG respects abbreviations at the end of a sentence.
    # "NP[Yahya] was sleeping his own and dreaming etc."
    def testPointAbsorption(self):
        senSpec = self.phraseFactory.createClause()
        firstNoun = self.phraseFactory.createNounPhrase()
        firstNoun.setNoun("yaha")
        senSpec.addComplement(firstNoun)
        senSpec.addComplement("was sleeping on his own and dreaming etc.")
        completeSen = self.phraseFactory.createSentence()
        completeSen.addComponent(senSpec)
        self.assertEqual("Yaha was sleeping on his own and dreaming etc.", \
                self.realiser.realise(completeSen).getRealisation())

    # Point absorption test: As above, but with trailing white space.
    # "NP[Yaha] was sleeping his own and dreaming etc.      "
    def testPointAbsorptionTrailingWhiteSpace(self):
        senSpec = self.phraseFactory.createClause()
        firstNoun = self.phraseFactory.createNounPhrase()
        firstNoun.setNoun("yaha")
        senSpec.addComplement(firstNoun)
        senSpec.addComplement("was sleeping on his own and dreaming etc.      ")
        completeSen = self.phraseFactory.createSentence()
        completeSen.addComponent(senSpec)
        self.assertEqual("Yaha was sleeping on his own and dreaming etc.", \
                self.realiser.realise(completeSen).getRealisation())

    # Abbreviation test: Check to see how SNLG deals with abbreviations in the middle of a sentence.
    # "NP[Yahya] and friends etc. went to NP[the park] to play."
    def testMiddleAbbreviation(self):
        senSpec = self.phraseFactory.createClause()
        firstNoun = self.phraseFactory.createNounPhrase()
        firstNoun.setNoun("yahya")
        senSpec.addComplement(firstNoun)
        senSpec.addComplement(self.phraseFactory.createStringElement("and friends etc. went to"))
        secondNoun = self.phraseFactory.createNounPhrase()
        secondNoun.setDeterminer("the")
        secondNoun.setNoun("park")
        senSpec.addComplement(secondNoun)
        senSpec.addComplement("to play")
        completeSen = self.phraseFactory.createSentence()
        completeSen.addComponent(senSpec)
        self.assertEqual("Yahya and friends etc. went to the park to play.", \
                self.realiser.realise(completeSen).getRealisation())

    # Indefinite Article Inflection: StringElement to test how SNLG handles a/an situations.
    # "I see an NP[elephant]"
    def testStringIndefiniteArticleInflectionVowel(self):
        senSpec = self.phraseFactory.createClause()
        senSpec.addComplement(self.phraseFactory.createStringElement("I see a"))
        firstNoun = self.phraseFactory.createNounPhrase("elephant")
        senSpec.addComplement(firstNoun)
        completeSen = self.phraseFactory.createSentence()
        completeSen.addComponent(senSpec)
        self.assertEqual("I see an elephant.", self.realiser.realise(completeSen).getRealisation())

    # Indefinite Article Inflection: StringElement to test how SNLG handles a/an situations.
    # "I see NP[a elephant]" -->
    def testNPIndefiniteArticleInflectionVowel(self):
        senSpec = self.phraseFactory.createClause()
        senSpec.addComplement(self.phraseFactory.createStringElement("I see"))
        firstNoun = self.phraseFactory.createNounPhrase("elephant")
        firstNoun.setDeterminer("a")
        senSpec.addComplement(firstNoun)
        completeSen = self.phraseFactory.createSentence()
        completeSen.addComponent(senSpec)
        self.assertEqual("I see an elephant.", self.realiser.realise(completeSen).getRealisation())

    '''
    # Not useful in python.  Java code returns "I see an cow." (ie.. it doesn't change the article)
    # assertNotSame simply verifies that two objects do not refer to the same object.
    # Indefinite Article Inflection: StringElement to test how SNLG handles a/an situations.
    # "I see an NP[cow]"
    def testStringIndefiniteArticleInflectionConsonant(self):
        senSpec = self.phraseFactory.createClause()
        senSpec.addComplement(self.phraseFactory.createStringElement("I see an"))
        firstNoun = self.phraseFactory.createNounPhrase("cow")
        senSpec.addComplement(firstNoun)
        completeSen = self.phraseFactory.createSentence()
        completeSen.addComponent(senSpec)
        # Do not attempt "an" -> "a"
        self.assertNotSame("I see an cow.", self.realiser.realise(completeSen).getRealisation())
    '''

    # Indefinite Article Inflection: StringElement to test how SNLG handles a/an situations.
    # "I see NP[an cow]" -->
    def testNPIndefiniteArticleInflectionConsonant(self):
        senSpec = self.phraseFactory.createClause()
        senSpec.addComplement(self.phraseFactory.createStringElement("I see"))
        firstNoun = self.phraseFactory.createNounPhrase("cow")
        firstNoun.setDeterminer("an")
        senSpec.addComplement(firstNoun)
        completeSen = self.phraseFactory.createSentence()
        completeSen.addComponent(senSpec)
        # Do not attempt "an" -> "a"
        self.assertEqual("I see an cow.", self.realiser.realise(completeSen).getRealisation())

    # aggregationStringElementTest: Test to see if we can aggregate two StringElements
    # in a CoordinatedPhraseElement.
    def testAggregationStringElement(self):
        coordinate = self.phraseFactory.createCoordinatedPhrase( \
                StringElement("John is going to Tesco"), StringElement("Mary is going to Sainsburys"))
        sentence = self.phraseFactory.createClause()
        sentence.addComplement(coordinate)
        self.assertEqual("John is going to Tesco and Mary is going to Sainsburys.", \
                self.realiser.realiseSentence(sentence))

    # Tests that no empty space is added when a StringElement is instantiated with an empty string
    # or None object.
    def testNullAndEmptyStringElement(self):
        NoneStringElement = self.phraseFactory.createStringElement(None)
        emptyStringElement = self.phraseFactory.createStringElement("")
        beautiful = self.phraseFactory.createStringElement("beautiful")
        horseLike = self.phraseFactory.createStringElement("horse-like")
        creature = self.phraseFactory.createStringElement("creature")
        # Test1: None or empty at beginning
        test1 = self.phraseFactory.createClause("a unicorn", "be", "regarded as a")
        test1.addPostModifier(emptyStringElement)
        test1.addPostModifier(beautiful)
        test1.addPostModifier(horseLike)
        test1.addPostModifier(creature)
        self.assertEqual("A unicorn is regarded as a beautiful horse-like creature.", \
                            self.realiser.realiseSentence(test1))
        # Test2: empty or None at end
        test2 = self.phraseFactory.createClause("a unicorn", "be", "regarded as a")
        test2.addPostModifier(beautiful)
        test2.addPostModifier(horseLike)
        test2.addPostModifier(creature)
        test2.addPostModifier(NoneStringElement)
        self.assertEqual("A unicorn is regarded as a beautiful horse-like creature.", \
                            self.realiser.realiseSentence(test2))
        # Test3: empty or None in the middle
        test3 = self.phraseFactory.createClause("a unicorn", "be", "regarded as a")
        test3.addPostModifier("beautiful")
        test3.addPostModifier("horse-like")
        test3.addPostModifier("")
        test3.addPostModifier("creature")
        self.assertEqual("A unicorn is regarded as a beautiful horse-like creature.", \
                            self.realiser.realiseSentence(test3))
        # Test4: empty or None in the middle with empty or None at beginning
        test4 = self.phraseFactory.createClause("a unicorn", "be", "regarded as a")
        test4.addPostModifier("")
        test4.addPostModifier("beautiful")
        test4.addPostModifier("horse-like")
        test4.addPostModifier(NoneStringElement)
        test4.addPostModifier("creature")
        self.assertEqual("A unicorn is regarded as a beautiful horse-like creature.", \
                            self.realiser.realiseSentence(test4))

if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
