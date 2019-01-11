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

from SimpleNLG4Test       import *
from simplenlg.features   import Feature, InterrogativeType, Person, Tense
from simplenlg.framework  import CoordinatedPhraseElement, DocumentElement, LexicalCategory
from simplenlg.framework  import NLGElement, NLGFactory, PhraseElement
from simplenlg.lexicon    import Lexicon
from simplenlg.phrasespec import PhraseElement, NPPhraseSpec, PPPhraseSpec, SPhraseSpec
from simplenlg.realiser.english  import Realiser


class InterrogativeTest(SimpleNLG4Test):
    def setUp(self):
        super().setUp()
        # the man gives the woman John's flower
        john = self.phraseFactory.createNounPhrase("John")
        john.setFeature(Feature.POSSESSIVE, True)
        flower = self.phraseFactory.createNounPhrase(john, "flower")
        _woman = self.phraseFactory.createNounPhrase("the", "woman")
        self.s3 = self.phraseFactory.createClause(self.man, self.give, flower)
        self.s3.setIndirectObject(_woman)
        subjects = CoordinatedPhraseElement( \
                self.phraseFactory.createNounPhrase("Jane"), \
                self.phraseFactory.createNounPhrase("Andrew"))
        self.s4 = self.phraseFactory.createClause(subjects, "pick up", "the balls")
        self.s4.addPostModifier("in the shop")
        self.s4.setFeature(Feature.CUE_PHRASE, "however")
        self.s4.addFrontModifier("tomorrow")
        self.s4.setFeature(Feature.TENSE, Tense.FUTURE)

    # Tests a couple of fairly simple questions.
    def testSimpleQuestions(self):
        self.setUp()
        self.phraseFactory.setLexicon(self.lexicon)
        self.realiser.setLexicon(self.lexicon)
        # simple present
        self.s1 = self.phraseFactory.createClause(self.woman, self.kiss, self.man)
        self.s1.setFeature(Feature.TENSE, Tense.PRESENT)
        self.s1.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        docFactory = NLGFactory(self.lexicon)
        sent = docFactory.createSentence(self.s1)
        self.assertEqual("Does the woman kiss the man?", self.realiser.realise(sent).getRealisation())
        # simple past
        # sentence: "the woman kissed the man"
        self.s1 = self.phraseFactory.createClause(self.woman, self.kiss, self.man)
        self.s1.setFeature(Feature.TENSE, Tense.PAST)
        self.s1.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.assertEqual("did the woman kiss the man", self.realiser.realise(self.s1).getRealisation())
        # copular/existential: be-fronting
        # sentence = "there is the dog on the rock"
        self.s2 = self.phraseFactory.createClause("there", "be", self.dog)
        self.s2.addPostModifier(self.onTheRock)
        self.s2.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.assertEqual("is there the dog on the rock", self.realiser.realise(self.s2).getRealisation())
        # perfective
        # sentence -- "there has been the dog on the rock"
        self.s2 = self.phraseFactory.createClause("there", "be", self.dog)
        self.s2.addPostModifier(self.onTheRock)
        self.s2.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.s2.setFeature(Feature.PERFECT, True)
        self.assertEqual("has there been the dog on the rock", \
                self.realiser.realise(self.s2).getRealisation())
        # progressive
        # sentence: "the man was giving the woman John's flower"
        john = self.phraseFactory.createNounPhrase("John")
        john.setFeature(Feature.POSSESSIVE, True)
        flower = self.phraseFactory.createNounPhrase(john, "flower")
        _woman = self.phraseFactory.createNounPhrase("the", "woman")
        self.s3 = self.phraseFactory.createClause(self.man, self.give, flower)
        self.s3.setIndirectObject(_woman)
        self.s3.setFeature(Feature.TENSE, Tense.PAST)
        self.s3.setFeature(Feature.PROGRESSIVE, True)
        self.s3.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        realised = self.realiser.realise(self.s3)
        self.assertEqual("was the man giving the woman John's flower", realised.getRealisation())
        # modal
        # sentence: "the man should be giving the woman John's flower"
        self.setUp()
        john = self.phraseFactory.createNounPhrase("John")
        john.setFeature(Feature.POSSESSIVE, True)
        flower = self.phraseFactory.createNounPhrase(john, "flower")
        _woman = self.phraseFactory.createNounPhrase("the", "woman")
        self.s3 = self.phraseFactory.createClause(self.man, self.give, flower)
        self.s3.setIndirectObject(_woman)
        self.s3.setFeature(Feature.TENSE, Tense.PAST)
        self.s3.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.s3.setFeature(Feature.MODAL, "should")
        self.assertEqual("should the man have given the woman John's flower", \
                self.realiser.realise(self.s3).getRealisation())
        # complex case with cue phrases
        # sentence: "however, tomorrow, Jane and Andrew will pick up the balls in the shop"
        # self gets the front modifier "tomorrow" shifted to the end
        self.setUp()
        subjects = CoordinatedPhraseElement( \
                self.phraseFactory.createNounPhrase("Jane"),
                self.phraseFactory.createNounPhrase("Andrew"))
        self.s4 = self.phraseFactory.createClause(subjects, "pick up", "the balls")
        self.s4.addPostModifier("in the shop")
        self.s4.setFeature(Feature.CUE_PHRASE, "however,")
        self.s4.addFrontModifier("tomorrow")
        self.s4.setFeature(Feature.TENSE, Tense.FUTURE)
        self.s4.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.assertEqual("however, will Jane and Andrew pick up the balls in the shop tomorrow", \
                self.realiser.realise(self.s4).getRealisation())

    # Test for sentences with negation.
    def testNegatedQuestions(self):
        self.setUp()
        self.phraseFactory.setLexicon(self.lexicon)
        self.realiser.setLexicon(self.lexicon)
        # sentence: "the woman did not kiss the man"
        self.s1 = self.phraseFactory.createClause(self.woman, "kiss", self.man)
        self.s1.setFeature(Feature.TENSE, Tense.PAST)
        self.s1.setFeature(Feature.NEGATED, True)
        self.s1.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.assertEqual("did the woman not kiss the man", self.realiser \
                .realise(self.s1).getRealisation())
        # sentence: however, tomorrow, Jane and Andrew will not pick up the balls in the shop
        subjects = CoordinatedPhraseElement( \
                self.phraseFactory.createNounPhrase("Jane"),
                self.phraseFactory.createNounPhrase("Andrew"))
        self.s4 = self.phraseFactory.createClause(subjects, "pick up", "the balls")
        self.s4.addPostModifier("in the shop")
        self.s4.setFeature(Feature.CUE_PHRASE, "however,")
        self.s4.addFrontModifier("tomorrow")
        self.s4.setFeature(Feature.NEGATED, True)
        self.s4.setFeature(Feature.TENSE, Tense.FUTURE)
        self.s4.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.assertEqual("however, will Jane and Andrew not pick up the balls in the shop tomorrow", \
                self.realiser.realise(self.s4).getRealisation())

    # Tests for coordinate VPs in question form.
    def testCoordinateVPQuestions(self):
        # create a complex vp: "kiss the dog and walk in the room"
        self.setUp()
        complex = CoordinatedPhraseElement(self.kiss, self.walk)
        self.kiss.addComplement(self.dog)
        self.walk.addComplement(self.inTheRoom)
        # sentence: "However, tomorrow, Jane and Andrew will kiss the dog and
        # will walk in the room"
        subjects = CoordinatedPhraseElement( \
                self.phraseFactory.createNounPhrase("Jane"),
                self.phraseFactory.createNounPhrase("Andrew"))
        self.s4 = self.phraseFactory.createClause(subjects, complex)
        self.s4.setFeature(Feature.CUE_PHRASE, "however")
        self.s4.addFrontModifier("tomorrow")
        self.s4.setFeature(Feature.TENSE, Tense.FUTURE)
        self.assertEqual("however tomorrow Jane and Andrew will kiss the dog and will walk in the room", \
                self.realiser.realise(self.s4).getRealisation())
        # setting to interrogative should automatically give us a single,
        # wide-scope aux
        self.setUp()
        subjects = CoordinatedPhraseElement( \
                self.phraseFactory.createNounPhrase("Jane"),
                self.phraseFactory.createNounPhrase("Andrew"))
        self.kiss.addComplement(self.dog)
        self.walk.addComplement(self.inTheRoom)
        complex = CoordinatedPhraseElement(self.kiss, self.walk)
        self.s4 = self.phraseFactory.createClause(subjects, complex)
        self.s4.setFeature(Feature.CUE_PHRASE, "however")
        self.s4.addFrontModifier("tomorrow")
        self.s4.setFeature(Feature.TENSE, Tense.FUTURE)
        self.s4.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.assertEqual("however will Jane and Andrew kiss the dog and walk in the room tomorrow", \
                self.realiser.realise(self.s4).getRealisation())
        # slightly more complex -- perfective
        self.setUp()
        self.realiser.setLexicon(self.lexicon)
        subjects = CoordinatedPhraseElement( \
                self.phraseFactory.createNounPhrase("Jane"), \
                self.phraseFactory.createNounPhrase("Andrew"))
        complex = CoordinatedPhraseElement(self.kiss, self.walk)
        self.kiss.addComplement(self.dog)
        self.walk.addComplement(self.inTheRoom)
        self.s4 = self.phraseFactory.createClause(subjects, complex)
        self.s4.setFeature(Feature.CUE_PHRASE, "however")
        self.s4.addFrontModifier("tomorrow")
        self.s4.setFeature(Feature.TENSE, Tense.FUTURE)
        self.s4.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.s4.setFeature(Feature.PERFECT, True)
        self.assertEqual("however will Jane and Andrew have kissed the dog and walked in the room tomorrow", \
                self.realiser.realise(self.s4).getRealisation())

    # Test for simple WH questions in present tense.
    def testSimpleQuestions2(self):
        self.setUp()
        self.realiser.setLexicon(self.lexicon)
        s = self.phraseFactory.createClause("the woman", "kiss", "the man")
        # try with the simple yes/no type first
        s.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.assertEqual("does the woman kiss the man", self.realiser.realise(s).getRealisation())
        # now in the passive
        s = self.phraseFactory.createClause("the woman", "kiss", "the man")
        s.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        s.setFeature(Feature.PASSIVE, True)
        self.assertEqual("is the man kissed by the woman", self.realiser.realise(s).getRealisation())
        # # subject interrogative with simple present
        # # sentence: "the woman kisses the man"
        s = self.phraseFactory.createClause("the woman", "kiss", "the man")
        s.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_SUBJECT)
        self.assertEqual("who kisses the man", self.realiser.realise(s).getRealisation())
        # object interrogative with simple present
        s = self.phraseFactory.createClause("the woman", "kiss", "the man")
        s.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_OBJECT)
        self.assertEqual("who does the woman kiss", self.realiser.realise(s).getRealisation())
        # subject interrogative with passive
        s = self.phraseFactory.createClause("the woman", "kiss", "the man")
        s.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_SUBJECT)
        s.setFeature(Feature.PASSIVE, True)
        self.assertEqual("who is the man kissed by", self.realiser.realise(s).getRealisation())

    # Test for wh questions.
    def testWHQuestions(self):
        # subject interrogative
        self.setUp()
        self.realiser.setLexicon(self.lexicon)
        self.s4.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_SUBJECT)
        self.assertEqual("however who will pick up the balls in the shop tomorrow", \
                self.realiser.realise(self.s4).getRealisation())
        # subject interrogative in passive
        self.setUp()
        self.s4.setFeature(Feature.PASSIVE, True)
        self.s4.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_SUBJECT)
        self.assertEqual("however who will the balls be picked up in the shop by tomorrow", \
                self.realiser.realise(self.s4).getRealisation())
        # object interrogative
        self.setUp()
        self.s4.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        self.assertEqual("however what will Jane and Andrew pick up in the shop tomorrow", \
                self.realiser.realise(self.s4).getRealisation())
        # object interrogative with passive
        self.setUp()
        self.s4.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        self.s4.setFeature(Feature.PASSIVE, True)
        self.assertEqual("however what will be picked up in the shop by Jane and Andrew tomorrow", \
                self.realiser.realise(self.s4).getRealisation())
        # how-question + passive
        self.setUp()
        self.s4.setFeature(Feature.PASSIVE, True)
        self.s4.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.HOW)
        self.assertEqual("however how will the balls be picked up in the shop by Jane and Andrew tomorrow", \
                self.realiser.realise(self.s4).getRealisation())
        # # why-question + passive
        self.setUp()
        self.s4.setFeature(Feature.PASSIVE, True)
        self.s4.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHY)
        self.assertEqual("however why will the balls be picked up in the shop by Jane and Andrew tomorrow", \
                self.realiser.realise(self.s4).getRealisation())
        # how question with modal
        self.setUp()
        self.s4.setFeature(Feature.PASSIVE, True)
        self.s4.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.HOW)
        self.s4.setFeature(Feature.MODAL, "should")
        self.assertEqual("however how should the balls be picked up in the shop by Jane and Andrew tomorrow", \
                self.realiser.realise(self.s4).getRealisation())
        # indirect object
        self.setUp()
        self.realiser.setLexicon(self.lexicon)
        self.s3.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_INDIRECT_OBJECT)
        self.assertEqual("who does the man give John's flower to", \
                self.realiser.realise(self.s3).getRealisation())

    # WH movement in the progressive
    def testProgrssiveWHSubjectQuestions(self):
        p = self.phraseFactory.createClause()
        p.setSubject("Mary")
        p.setVerb("eat")
        p.setObject(self.phraseFactory.createNounPhrase("the", "pie"))
        p.setFeature(Feature.PROGRESSIVE, True)
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_SUBJECT)
        self.assertEqual("who is eating the pie",
                self.realiser.realise(p).getRealisation())

    # WH movement in the progressive
    def testProgrssiveWHObjectQuestions(self):
        p = self.phraseFactory.createClause()
        p.setSubject("Mary")
        p.setVerb("eat")
        p.setObject(self.phraseFactory.createNounPhrase("the", "pie"))
        p.setFeature(Feature.PROGRESSIVE, True)
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        self.assertEqual("what is Mary eating", self.realiser.realise(p).getRealisation())

    # Negation with WH movement for subject
    def testNegatedWHSubjQuestions(self):
        p = self.phraseFactory.createClause()
        p.setSubject("Mary")
        p.setVerb("eat")
        p.setObject(self.phraseFactory.createNounPhrase("the", "pie"))
        p.setFeature(Feature.NEGATED, True)
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_SUBJECT)
        self.assertEqual("who does not eat the pie", self.realiser.realise(p).getRealisation())

    # Negation with WH movement for object
    def testNegatedWHObjQuestions(self):
        p = self.phraseFactory.createClause()
        p.setSubject("Mary")
        p.setVerb("eat")
        p.setObject(self.phraseFactory.createNounPhrase("the", "pie"))
        p.setFeature(Feature.NEGATED, True)
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        realisation = self.realiser.realise(p)
        self.assertEqual("what does Mary not eat", realisation.getRealisation())

    # Test questyions in the tutorial.
    def testTutorialQuestions(self):
        self.setUp()
        self.realiser.setLexicon(self.lexicon)
        p = self.phraseFactory.createClause("Mary", "chase", "George")
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.assertEqual("does Mary chase George", self.realiser.realise(p).getRealisation())
        p = self.phraseFactory.createClause("Mary", "chase", "George")
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_OBJECT)
        self.assertEqual("who does Mary chase", self.realiser.realise(p).getRealisation())

    # Subject WH Questions with modals
    def testModalWHSubjectQuestion(self):
        p = self.phraseFactory.createClause(self.dog, "upset", self.man)
        p.setFeature(Feature.TENSE, Tense.PAST)
        self.assertEqual("the dog upset the man", self.realiser.realise(p).getRealisation())
        # first without modal
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_SUBJECT)
        self.assertEqual("who upset the man", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_SUBJECT)
        self.assertEqual("what upset the man", self.realiser.realise(p).getRealisation())
        # now with modal auxiliary
        p.setFeature(Feature.MODAL, "may")
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_SUBJECT)
        self.assertEqual("who may have upset the man", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.TENSE, Tense.FUTURE)
        self.assertEqual("who may upset the man", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.TENSE, Tense.PAST)
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_SUBJECT)
        self.assertEqual("what may have upset the man", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.TENSE, Tense.FUTURE)
        self.assertEqual("what may upset the man", self.realiser.realise(p).getRealisation())

    # Subject WH Questions with modals
    def testModalWHObjectQuestion(self):
        p = self.phraseFactory.createClause(self.dog, "upset", self.man)
        p.setFeature(Feature.TENSE, Tense.PAST)
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_OBJECT)
        self.assertEqual("who did the dog upset", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.MODAL, "may")
        self.assertEqual("who may the dog have upset", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        self.assertEqual("what may the dog have upset", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.TENSE, Tense.FUTURE)
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_OBJECT)
        self.assertEqual("who may the dog upset", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        self.assertEqual("what may the dog upset", self.realiser.realise(p).getRealisation())

    # Questions with tenses requiring auxiliaries + subject WH
    def testAuxWHSubjectQuestion(self):
        p = self.phraseFactory.createClause(self.dog, "upset", self.man)
        p.setFeature(Feature.TENSE, Tense.PRESENT)
        p.setFeature(Feature.PERFECT, True)
        self.assertEqual("the dog has upset the man", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_SUBJECT)
        self.assertEqual("who has upset the man", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_SUBJECT)
        self.assertEqual("what has upset the man", self.realiser.realise(p).getRealisation())

    # Questions with tenses requiring auxiliaries + subject WH
    def testAuxWHObjectQuestion(self):
        p = self.phraseFactory.createClause(self.dog, "upset", self.man)
        # first without any aux
        p.setFeature(Feature.TENSE, Tense.PAST)
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        self.assertEqual("what did the dog upset", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_OBJECT)
        self.assertEqual("who did the dog upset", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.TENSE, Tense.PRESENT)
        p.setFeature(Feature.PERFECT, True)
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_OBJECT)
        self.assertEqual("who has the dog upset", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        self.assertEqual("what has the dog upset", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.TENSE, Tense.FUTURE)
        p.setFeature(Feature.PERFECT, True)
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_OBJECT)
        self.assertEqual("who will the dog have upset", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        self.assertEqual("what will the dog have upset", self.realiser.realise(p).getRealisation())

    # Test for questions with "be"
    def testBeQuestions(self):
        p = self.phraseFactory.createClause( \
                self.phraseFactory.createNounPhrase("a", "ball"), \
                self.phraseFactory.createWord("be", LexicalCategory.VERB), \
                self.phraseFactory.createNounPhrase("a", "toy"))
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        self.assertEqual("what is a ball", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.assertEqual("is a ball a toy", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_SUBJECT)
        self.assertEqual("what is a toy", self.realiser.realise(p).getRealisation())
        p2 = self.phraseFactory.createClause("Mary", "be", "beautiful")
        p2.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHY)
        self.assertEqual("why is Mary beautiful", self.realiser.realise(p2).getRealisation())
        p2.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHERE)
        self.assertEqual("where is Mary beautiful", self.realiser.realise(p2).getRealisation())
        p2.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_SUBJECT)
        self.assertEqual("who is beautiful", self.realiser.realise(p2).getRealisation())

    # Test for questions with "be" in future tense
    def testBeQuestionsFuture(self):
        p = self.phraseFactory.createClause( \
                self.phraseFactory.createNounPhrase("a", "ball"), \
                self.phraseFactory.createWord("be", LexicalCategory.VERB), \
                self.phraseFactory.createNounPhrase("a", "toy"))
        p.setFeature(Feature.TENSE, Tense.FUTURE)
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        self.assertEqual("what will a ball be", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.assertEqual("will a ball be a toy", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_SUBJECT)
        self.assertEqual("what will be a toy", self.realiser.realise(p).getRealisation())
        p2 = self.phraseFactory.createClause("Mary", "be", "beautiful")
        p2.setFeature(Feature.TENSE, Tense.FUTURE)
        p2.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHY)
        self.assertEqual("why will Mary be beautiful", self.realiser.realise(p2).getRealisation())
        p2.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHERE)
        self.assertEqual("where will Mary be beautiful", self.realiser.realise(p2).getRealisation())
        p2.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_SUBJECT)
        self.assertEqual("who will be beautiful", self.realiser.realise(p2).getRealisation())

    # Tests for WH questions with be in past tense
    def testBeQuestionsPast(self):
        p = self.phraseFactory.createClause( \
                self.phraseFactory.createNounPhrase("a", "ball"), \
                self.phraseFactory.createWord("be", LexicalCategory.VERB), \
                self.phraseFactory.createNounPhrase("a", "toy"))
        p.setFeature(Feature.TENSE, Tense.PAST)
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        self.assertEqual("what was a ball", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.assertEqual("was a ball a toy", self.realiser.realise(p).getRealisation())
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_SUBJECT)
        self.assertEqual("what was a toy", self.realiser.realise(p).getRealisation())
        p2 = self.phraseFactory.createClause("Mary", "be", "beautiful")
        p2.setFeature(Feature.TENSE, Tense.PAST)
        p2.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHY)
        self.assertEqual("why was Mary beautiful", self.realiser.realise(p2).getRealisation())
        p2.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHERE)
        self.assertEqual("where was Mary beautiful", self.realiser.realise(p2).getRealisation())
        p2.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_SUBJECT)
        self.assertEqual("who was beautiful", self.realiser.realise(p2).getRealisation())

    # Test WHERE, HOW and WHY questions, with copular predicate "be"
    def testSimpleBeWHQuestions(self):
        p = self.phraseFactory.createClause("I", "be")
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHERE)
        self.assertEqual("Where am I?", self.realiser.realiseSentence(p))
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHY)
        self.assertEqual("Why am I?", self.realiser.realiseSentence(p))
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.HOW)
        self.assertEqual("How am I?", self.realiser.realiseSentence(p))

    # Test a simple "how" question, based on query from Albi Oxa
    def testHowPredicateQuestion(self):
        test = self.phraseFactory.createClause()
        subject = self.phraseFactory.createNounPhrase("You")
        subject.setFeature(Feature.PRONOMINAL, True)
        subject.setFeature(Feature.PERSON, Person.SECOND)
        test.setSubject(subject)
        test.setVerb("be")
        test.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.HOW_PREDICATE)
        test.setFeature(Feature.TENSE, Tense.PRESENT)
        result = self.realiser.realiseSentence(test)
        self.assertEqual("How are you?", result)

    # Case 1 checks that "What do you think about John?" can be generated.
    # Case 2 checks that the same clause is generated, even when an object is declared.
    def testWhatObjectInterrogative(self):
        # Case 1, no object is explicitly given:
        clause = self.phraseFactory.createClause("you", "think")
        aboutJohn = self.phraseFactory.createPrepositionPhrase("about", "John")
        clause.addPostModifier(aboutJohn)
        clause.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        realisation = self.realiser.realiseSentence(clause)
        self.assertEqual("What do you think about John?", realisation)
        # Case 2:
        # Add "bad things" as the object so the object doesn't remain null:
        clause.setObject("bad things")
        realisation = self.realiser.realiseSentence(clause)
        self.assertEqual("What do you think about John?", realisation)

if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
