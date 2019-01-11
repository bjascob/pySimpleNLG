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

from SimpleNLG4Test          import *
from simplenlg.features      import DiscourseFunction, Feature, Gender, InternalFeature
from simplenlg.features      import LexicalFeature, NumberAgreement, Person, Tense
from simplenlg.framework     import CoordinatedPhraseElement, LexicalCategory, NLGElement
from simplenlg.framework     import PhraseElement, NPPhraseSpec, SPhraseSpec


# Tests for the NPPhraseSpec and CoordinateNPPhraseSpec classes.
class NounPhraseTest(SimpleNLG4Test):
    # Test the setPlural() method in noun phrases.
    def testPlural(self):
        self.np4.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        self.assertEqual("the rocks", self.realiser.realise(self.np4).getRealisation())
        self.np5.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        self.assertEqual("the curtains", self.realiser.realise(self.np5).getRealisation())
        self.np5.setFeature(Feature.NUMBER, NumberAgreement.SINGULAR)
        self.assertEqual(NumberAgreement.SINGULAR, self.np5.getFeature(Feature.NUMBER))
        self.assertEqual("the curtain", self.realiser.realise(self.np5).getRealisation())
        self.np5.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        self.assertEqual("the curtains", self.realiser.realise(self.np5).getRealisation())

    # Test the pronominalisation method for full NPs.
    def testPronominalisation(self):
        # sing
        self.proTest1.setFeature(LexicalFeature.GENDER, Gender.FEMININE)
        self.proTest1.setFeature(Feature.PRONOMINAL, True)
        self.assertEqual("she", self.realiser.realise(self.proTest1).getRealisation())
        # sing, possessive
        self.proTest1.setFeature(Feature.POSSESSIVE, True)
        self.assertEqual("her", self.realiser.realise(self.proTest1).getRealisation())
        # plural pronoun
        self.proTest2.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        self.proTest2.setFeature(Feature.PRONOMINAL, True)
        self.assertEqual("they", self.realiser.realise(self.proTest2).getRealisation())
        # accusative: "them"
        self.proTest2.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.OBJECT)
        self.assertEqual("them", self.realiser.realise(self.proTest2).getRealisation())

    # Test the pronominalisation method for full NPs (more thorough than above)
    def testPronominalisation2(self):
        # Ehud - added extra pronominalisation tests
        pro = self.phraseFactory.createNounPhrase("Mary")
        pro.setFeature(Feature.PRONOMINAL, True)
        pro.setFeature(Feature.PERSON, Person.FIRST)
        sent = self.phraseFactory.createClause(pro, "like", "John")
        self.assertEqual("I like John.", self.realiser.realiseSentence(sent))
        #
        pro = self.phraseFactory.createNounPhrase("Mary")
        pro.setFeature(Feature.PRONOMINAL, True)
        pro.setFeature(Feature.PERSON, Person.SECOND)
        sent = self.phraseFactory.createClause(pro, "like", "John")
        self.assertEqual("You like John.", self.realiser.realiseSentence(sent))
        #
        pro = self.phraseFactory.createNounPhrase("Mary")
        pro.setFeature(Feature.PRONOMINAL, True)
        pro.setFeature(Feature.PERSON, Person.THIRD)
        pro.setFeature(LexicalFeature.GENDER, Gender.FEMININE)
        sent = self.phraseFactory.createClause(pro, "like", "John")
        self.assertEqual("She likes John.", self.realiser.realiseSentence(sent))
        #
        pro = self.phraseFactory.createNounPhrase("Mary")
        pro.setFeature(Feature.PRONOMINAL, True)
        pro.setFeature(Feature.PERSON, Person.FIRST)
        pro.setPlural(True)
        sent = self.phraseFactory.createClause(pro, "like", "John")
        self.assertEqual("We like John.", self.realiser.realiseSentence(sent))
        #
        pro = self.phraseFactory.createNounPhrase("Mary")
        pro.setFeature(Feature.PRONOMINAL, True)
        pro.setFeature(Feature.PERSON, Person.SECOND)
        pro.setPlural(True)
        sent = self.phraseFactory.createClause(pro, "like", "John")
        self.assertEqual("You like John.", self.realiser.realiseSentence(sent))
        #
        pro = self.phraseFactory.createNounPhrase("Mary")
        pro.setFeature(Feature.PRONOMINAL, True)
        pro.setFeature(Feature.PERSON, Person.THIRD)
        pro.setPlural(True)
        pro.setFeature(LexicalFeature.GENDER, Gender.FEMININE)
        sent = self.phraseFactory.createClause(pro, "like", "John")
        self.assertEqual("They like John.", self.realiser.realiseSentence(sent))
        #
        pro = self.phraseFactory.createNounPhrase("John")
        pro.setFeature(Feature.PRONOMINAL, True)
        pro.setFeature(Feature.PERSON, Person.FIRST)
        sent = self.phraseFactory.createClause("Mary", "like", pro)
        self.assertEqual("Mary likes me.", self.realiser.realiseSentence(sent))
        #
        pro = self.phraseFactory.createNounPhrase("John")
        pro.setFeature(Feature.PRONOMINAL, True)
        pro.setFeature(Feature.PERSON, Person.SECOND)
        sent = self.phraseFactory.createClause("Mary", "like", pro)
        self.assertEqual("Mary likes you.", self.realiser.realiseSentence(sent))
        #
        pro = self.phraseFactory.createNounPhrase("John")
        pro.setFeature(Feature.PRONOMINAL, True)
        pro.setFeature(Feature.PERSON, Person.THIRD)
        pro.setFeature(LexicalFeature.GENDER, Gender.MASCULINE)
        sent = self.phraseFactory.createClause("Mary", "like", pro)
        self.assertEqual("Mary likes him.", self.realiser.realiseSentence(sent))
        #
        pro = self.phraseFactory.createNounPhrase("John")
        pro.setFeature(Feature.PRONOMINAL, True)
        pro.setFeature(Feature.PERSON, Person.FIRST)
        pro.setPlural(True)
        sent = self.phraseFactory.createClause("Mary", "like", pro)
        self.assertEqual("Mary likes us.", self.realiser.realiseSentence(sent))
        #
        pro = self.phraseFactory.createNounPhrase("John")
        pro.setFeature(Feature.PRONOMINAL, True)
        pro.setFeature(Feature.PERSON, Person.SECOND)
        pro.setPlural(True)
        sent = self.phraseFactory.createClause("Mary", "like", pro)
        self.assertEqual("Mary likes you.", self.realiser.realiseSentence(sent))
        #
        pro = self.phraseFactory.createNounPhrase("John")
        pro.setFeature(Feature.PRONOMINAL, True)
        pro.setFeature(Feature.PERSON, Person.THIRD)
        pro.setFeature(LexicalFeature.GENDER, Gender.MASCULINE)
        pro.setPlural(True)
        sent = self.phraseFactory.createClause("Mary", "like", pro)
        self.assertEqual("Mary likes them.", self.realiser.realiseSentence(sent))

    # Test premodification in NPS.
    def testPremodification(self):
        self.man.addPreModifier(self.salacious)
        self.assertEqual("the salacious man", self.realiser.realise(self.man).getRealisation())
        #
        self.woman.addPreModifier(self.beautiful)
        self.assertEqual("the beautiful woman", self.realiser.realise(self.woman).getRealisation())
        #
        self.dog.addPreModifier(self.stunning)
        self.assertEqual("the stunning dog", self.realiser.realise(self.dog).getRealisation())
        # premodification with a WordElement
        self.man.setPreModifier(self.phraseFactory.createWord("idiotic", LexicalCategory.ADJECTIVE))
        self.assertEqual("the idiotic man", self.realiser.realise(self.man).getRealisation())

    # Test prepositional postmodification.
    def testPostmodification(self):
        self.man.addPostModifier(self.onTheRock)
        self.assertEqual("the man on the rock", self.realiser.realise(self.man).getRealisation())
        #
        self.woman.addPostModifier(self.behindTheCurtain)
        self.assertEqual("the woman behind the curtain", \
                self.realiser.realise(self.woman).getRealisation())
        # postmodification with a WordElement
        self.man.setPostModifier(self.phraseFactory.createWord("jack", LexicalCategory.NOUN))
        self.assertEqual("the man jack", self.realiser.realise(self.man).getRealisation())

    # Test nominal complementation
    def testComplementation(self):
        # complementation with a WordElement
        self.man.setComplement(self.phraseFactory.createWord("jack",LexicalCategory.NOUN))
        self.assertEqual("the man jack", self.realiser.realise(self.man).getRealisation())
        #
        self.woman.addComplement(self.behindTheCurtain)
        self.assertEqual("the woman behind the curtain", \
                self.realiser.realise(self.woman).getRealisation())

    # Test possessive constructions.
    def testPossessive(self):
        # simple possessive 's: 'a man's'
        possNP = self.phraseFactory.createNounPhrase("a", "man")
        possNP.setFeature(Feature.POSSESSIVE, True)
        self.assertEqual("a man's", self.realiser.realise(possNP).getRealisation())
        # now set self possessive as specifier of the NP 'the dog'
        self.dog.setFeature(InternalFeature.SPECIFIER, possNP)
        self.assertEqual("a man's dog", self.realiser.realise(self.dog).getRealisation())
        # convert possNP to pronoun and turn "a dog" into "his dog"
        # need to specify gender, as default is NEUTER
        possNP.setFeature(LexicalFeature.GENDER, Gender.MASCULINE)
        possNP.setFeature(Feature.PRONOMINAL, True)
        self.assertEqual("his dog", self.realiser.realise(self.dog).getRealisation())
        # make it slightly more complicated: "his dog's rock"
        self.dog.setFeature(Feature.POSSESSIVE, True) # his dog's
        # his dog's rock (substituting "the" for the entire phrase)
        self.np4.setFeature(InternalFeature.SPECIFIER, self.dog)
        self.assertEqual("his dog's rock", self.realiser.realise(self.np4).getRealisation())

    # Test NP coordination.
    def testCoordination(self):
        cnp1 = CoordinatedPhraseElement(self.dog,  self.woman)
        # simple coordination
        self.assertEqual("the dog and the woman", self.realiser.realise(cnp1).getRealisation())
        # simple coordination with complementation of entire coordinate NP
        cnp1.addComplement(self.behindTheCurtain)
        self.assertEqual("the dog and the woman behind the curtain", \
                  self.realiser.realise(cnp1).getRealisation())

    # Another battery of tests for NP coordination.
    def testCoordination2(self):
        # simple coordination of complementised nps
        self.dog.clearComplements()
        self.woman.clearComplements()
        cnp1 = CoordinatedPhraseElement(self.dog, self.woman)
        cnp1.setFeature(Feature.RAISE_SPECIFIER, True)
        realised = self.realiser.realise(cnp1)
        self.assertEqual("the dog and woman", realised.getRealisation())
        #
        self.dog.addComplement(self.onTheRock)
        self.woman.addComplement(self.behindTheCurtain)
        #
        cnp2 = CoordinatedPhraseElement(self.dog, self.woman)
        self.woman.setFeature(InternalFeature.RAISED, False)
        self.assertEqual("the dog on the rock and the woman behind the curtain", \
                self.realiser.realise(cnp2).getRealisation())
        # complementised coordinates + outer pp modifier
        cnp2.addPostModifier(self.inTheRoom)
        self.assertEqual("the dog on the rock and the woman behind the curtain in the room", \
                self.realiser.realise(cnp2).getRealisation())
        # set the specifier for self cnp should unset specifiers for all inner coordinates
        every = self.phraseFactory.createWord("every", LexicalCategory.DETERMINER)
        cnp2.setFeature(InternalFeature.SPECIFIER, every)
        self.assertEqual("every dog on the rock and every woman behind the curtain in the room", \
                self.realiser.realise(cnp2).getRealisation())
        # pronominalise one of the constituents
        self.dog.setFeature(Feature.PRONOMINAL, True) # ="it"
        self.dog.setFeature(InternalFeature.SPECIFIER, \
                self.phraseFactory.createWord("the", LexicalCategory.DETERMINER))
        # raising spec still returns True as spec has been set
        cnp2.setFeature(Feature.RAISE_SPECIFIER, True)
        # CNP should be realised with pronominal internal const
        self.assertEqual("it and every woman behind the curtain in the room", \
                self.realiser.realise(cnp2).getRealisation())

    # Test possessives in coordinate NPs.
    def testPossessiveCoordinate(self):
        # simple coordination
        cnp2 = CoordinatedPhraseElement(self.dog, self.woman)
        self.assertEqual("the dog and the woman", self.realiser.realise(cnp2).getRealisation())
        # set possessive -- wide-scope by default
        cnp2.setFeature(Feature.POSSESSIVE, True)
        self.assertEqual("the dog and the woman's", self.realiser.realise(cnp2).getRealisation())
        # set possessive with pronoun
        self.dog.setFeature(Feature.PRONOMINAL, True)
        self.dog.setFeature(Feature.POSSESSIVE, True)
        cnp2.setFeature(Feature.POSSESSIVE, True)
        self.assertEqual("its and the woman's", self.realiser.realise(cnp2).getRealisation())

    # Test A vs An.
    def testAAn(self):
        _dog = self.phraseFactory.createNounPhrase("a", "dog")
        self.assertEqual("a dog", self.realiser.realise(_dog).getRealisation())
        _dog.addPreModifier("enormous")
        self.assertEqual("an enormous dog", self.realiser.realise(_dog).getRealisation())
        elephant = self.phraseFactory.createNounPhrase("a", "elephant")
        self.assertEqual("an elephant", self.realiser.realise(elephant).getRealisation())
        elephant.addPreModifier("big")
        self.assertEqual("a big elephant", self.realiser.realise(elephant).getRealisation())
        # test treating of plural specifiers
        _dog.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        self.assertEqual("some enormous dogs", self.realiser.realise(_dog).getRealisation())

    # Further tests for a/an agreement with coordinated premodifiers
    def testAAnCoord(self):
        _dog = self.phraseFactory.createNounPhrase("a", "dog")
        _dog.addPreModifier(self.phraseFactory.createCoordinatedPhrase("enormous", "black"))
        realisation = self.realiser.realise(_dog).getRealisation()
        self.assertEqual("an enormous and black dog", realisation)

    # Test for a/an agreement with numbers
    def testAAnWithNumbers(self):
        num = self.phraseFactory.createNounPhrase("a", "change")
        # no an with "one"
        num.setPreModifier("one percent")
        realisation = self.realiser.realise(num).getRealisation()
        self.assertEqual("a one percent change", realisation)
        # an with "eighty"
        num.setPreModifier("eighty percent")
        realisation = self.realiser.realise(num).getRealisation()
        self.assertEqual("an eighty percent change", realisation)
        # an with 80
        num.setPreModifier("80%")
        realisation = self.realiser.realise(num).getRealisation()
        self.assertEqual("an 80% change", realisation)
        # an with 80000
        num.setPreModifier("80000")
        realisation = self.realiser.realise(num).getRealisation()
        self.assertEqual("an 80000 change", realisation)
        # an with 11,000
        num.setPreModifier("11,000")
        realisation = self.realiser.realise(num).getRealisation()
        self.assertEqual("an 11,000 change", realisation)
        # an with 18
        num.setPreModifier("18%")
        realisation = self.realiser.realise(num).getRealisation()
        self.assertEqual("an 18% change", realisation)
        # a with 180
        num.setPreModifier("180")
        realisation = self.realiser.realise(num).getRealisation()
        self.assertEqual("a 180 change", realisation)
        # a with 1100
        num.setPreModifier("1100")
        realisation = self.realiser.realise(num).getRealisation()
        self.assertEqual("a 1100 change", realisation)
        # a with 180,000
        num.setPreModifier("180,000")
        realisation = self.realiser.realise(num).getRealisation()
        self.assertEqual("a 180,000 change", realisation)
        # an with 11000
        num.setPreModifier("11000")
        realisation = self.realiser.realise(num).getRealisation()
        self.assertEqual("an 11000 change", realisation)
        # an with 18000
        num.setPreModifier("18000")
        realisation = self.realiser.realise(num).getRealisation()
        self.assertEqual("an 18000 change", realisation)
        # an with 18.1
        num.setPreModifier("18.1%")
        realisation = self.realiser.realise(num).getRealisation()
        self.assertEqual("an 18.1% change", realisation)
        # an with 11.1
        num.setPreModifier("11.1%")
        realisation = self.realiser.realise(num).getRealisation()
        self.assertEqual("an 11.1% change", realisation)

    # Test Modifier "guess" placement.
    def testModifier(self):
        _dog = self.phraseFactory.createNounPhrase("a", "dog")
        _dog.addPreModifier("angry")
        self.assertEqual("an angry dog", self.realiser.realise(_dog).getRealisation())
        _dog.addPostModifier("in the park")
        self.assertEqual("an angry dog in the park", self.realiser.realise(_dog).getRealisation())
        cat = self.phraseFactory.createNounPhrase("a", "cat")
        cat.addPreModifier(self.phraseFactory.createAdjectivePhrase("angry"))
        self.assertEqual("an angry cat", self.realiser.realise(cat).getRealisation())
        cat.addPostModifier(self.phraseFactory.createPrepositionPhrase("in", "the park"))
        self.assertEqual("an angry cat in the park", self.realiser.realise(cat).getRealisation())

    def testPluralNounsBelongingToASingular(self):
        sent = self.phraseFactory.createClause("I", "count up")
        sent.setFeature(Feature.TENSE, Tense.PAST)
        obj = self.phraseFactory.createNounPhrase("digit")
        obj.setPlural(True)
        possessor = self.phraseFactory.createNounPhrase("the", "box")
        possessor.setPlural(False)
        possessor.setFeature(Feature.POSSESSIVE, True)
        obj.setSpecifier(possessor)
        sent.setObject(obj)
        self.assertEqual("I counted up the box's digits", self.realiser.realise(sent).getRealisation())

    def testSingularNounsBelongingToAPlural(self):
        sent = self.phraseFactory.createClause("I", "clean")
        sent.setFeature(Feature.TENSE, Tense.PAST)
        obj = self.phraseFactory.createNounPhrase("car")
        obj.setPlural(False)
        possessor = self.phraseFactory.createNounPhrase("the", "parent")
        possessor.setPlural(True)
        possessor.setFeature(Feature.POSSESSIVE, True)
        obj.setSpecifier(possessor)
        sent.setObject(obj)
        self.assertEqual("I cleaned the parents' car", self.realiser.realise(sent).getRealisation())

    # Test for appositive postmodifiers
    def testAppositivePostmodifier(self):
        _dog = self.phraseFactory.createNounPhrase("the", "dog")
        _rott = self.phraseFactory.createNounPhrase("a", "rottweiler")
        _rott.setFeature(Feature.APPOSITIVE, True)
        _dog.addPostModifier(_rott)
        _sent = self.phraseFactory.createClause(_dog, "ran")
        self.assertEqual("The dog, a rottweiler runs.", self.realiser.realiseSentence(_sent))

if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
