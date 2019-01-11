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

from SimpleNLG4Test                                  import *
from simplenlg.features.ClauseStatus                 import *
from simplenlg.features.DiscourseFunction            import *
from simplenlg.features.Feature                      import *
from simplenlg.features.Form                         import *
from simplenlg.features.InternalFeature              import *
from simplenlg.features.NumberAgreement              import *
from simplenlg.features.Tense                        import *
from simplenlg.framework.CoordinatedPhraseElement    import *
from simplenlg.framework.LexicalCategory             import *
from simplenlg.framework.NLGElement                  import *
from simplenlg.framework.PhraseCategory              import *
from simplenlg.framework.PhraseElement               import *
from simplenlg.framework.PhraseElement               import *
from simplenlg.phrasespec.AdjPhraseSpec              import *
from simplenlg.phrasespec.AdvPhraseSpec              import *
from simplenlg.phrasespec.NPPhraseSpec               import *
from simplenlg.phrasespec.PPPhraseSpec               import *
from simplenlg.phrasespec.SPhraseSpec                import *
from simplenlg.phrasespec.VPPhraseSpec               import *


class ClauseTest(SimpleNLG4Test):
    # Instantiates a new s test.
    def ClauseTest(self, name):
        super().__init__(name)

    # @Override @Before
    def setUp(self):
        super().setUp()
        # the woman kisses the man
        self.s1 = self.phraseFactory.createClause()
        self.s1.setSubject(self.woman)
        self.s1.setVerbPhrase(self.kiss)
        self.s1.setObject(self.man)

        # there is the dog on the rock
        self.s2 = self.phraseFactory.createClause()
        self.s2.setSubject("there")
        self.s2.setVerb("be")
        self.s2.setObject(self.dog)
        self.s2.addPostModifier(self.onTheRock)

        # the man gives the woman John's flower
        self.s3 = self.phraseFactory.createClause()
        self.s3.setSubject(self.man)
        self.s3.setVerbPhrase(self.give)

        flower = self.phraseFactory.createNounPhrase("flower")
        john = self.phraseFactory.createNounPhrase("John")
        john.setFeature(Feature.POSSESSIVE, True)
        flower.setFeature(InternalFeature.SPECIFIER, john)
        self.s3.setObject(flower)
        self.s3.setIndirectObject(self.woman)

        self.s4 = self.phraseFactory.createClause()
        self.s4.setFeature(Feature.CUE_PHRASE, "however")
        self.s4.addFrontModifier("tomorrow")

        subject = self.phraseFactory.createCoordinatedPhrase(self.phraseFactory \
                .createNounPhrase("Jane"), self.phraseFactory.createNounPhrase("Andrew"))

        self.s4.setSubject(subject)

        pick = self.phraseFactory.createVerbPhrase("pick up")
        self.s4.setVerbPhrase(pick)
        self.s4.setObject("the balls") #$NON-NLS-1$
        self.s4.addPostModifier("in the shop") #$NON-NLS-1$
        self.s4.setFeature(Feature.TENSE, Tense.FUTURE)

    # @After
    def tearDown(self):
        super().tearDown()
        self.s1 = None
        self.s2 = None
        self.s3 = None
        self.s4 = None

    # Initial test for basic sentences.
    def testBasic(self):
        self.assertEqual("the woman kisses the man", self.realiser.realise(self.s1).getRealisation())
        self.assertEqual("there is the dog on the rock", self.realiser.realise(self.s2).getRealisation())
        self.setUp()
        self.assertEqual("the man gives the woman John's flower", self.realiser.realise(self.s3).getRealisation())
        self.assertEqual("however tomorrow Jane and Andrew will pick up the balls in the shop", \
                self.realiser.realise(self.s4).getRealisation())

    # Test did not
    def testDidNot(self):
        s = self.phraseFactory.createClause("John", "eat")
        s.setFeature(Feature.TENSE, Tense.PAST)
        s.setFeature(Feature.NEGATED, True)
        self.assertEqual("John did not eat", self.realiser.realise(s).getRealisation())

    # Test did not
    def testVPNegation(self):
        # negate the VP
        vp = self.phraseFactory.createVerbPhrase("lie")
        vp.setFeature(Feature.TENSE, Tense.PAST)
        vp.setFeature(Feature.NEGATED, True)
        compl = self.phraseFactory.createVerbPhrase("etherize")
        compl.setFeature(Feature.TENSE, Tense.PAST)
        vp.setComplement(compl)
        s = self.phraseFactory.createClause(self.phraseFactory.createNounPhrase("the", "patient"), vp)
        self.assertEqual("the patient did not lie etherized", self.realiser.realise(s).getRealisation())

    # Test that pronominal args are being correctly cast as NPs.
    def testPronounArguments(self):
        # the subject of s2 should have been cast into a pronominal NP
        subj = self.s2.getFeatureAsElementList(InternalFeature.SUBJECTS)[0]
        self.assertTrue(subj.isA(PhraseCategory.NOUN_PHRASE))

    # Tests for setting tense, aspect and passive from the sentence interface.
    def testTenses(self):
        # simple past
        self.s3.setFeature(Feature.TENSE, Tense.PAST)
        self.assertEqual("the man gave the woman John's flower", \
                self.realiser.realise(self.s3).getRealisation())
        # perfect
        self.s3.setFeature(Feature.PERFECT, True)
        self.assertEqual("the man had given the woman John's flower", \
                self.realiser.realise(self.s3).getRealisation())
        # negation
        self.s3.setFeature(Feature.NEGATED, True)
        self.assertEqual("the man had not given the woman John's flower", \
                self.realiser.realise(self.s3).getRealisation())
        self.s3.setFeature(Feature.PROGRESSIVE, True)
        self.assertEqual("the man had not been giving the woman John's flower", \
                self.realiser.realise(self.s3).getRealisation())
        # passivisation with direct and indirect object
        self.s3.setFeature(Feature.PASSIVE, True)

    # Test what happens when a sentence is subordinated as complement of a verb
    def testSubordination(self):
        # subordinate sentence by setting it as complement of a verb
        self.say.addComplement(self.s3)
        # check the getter
        self.assertEqual(ClauseStatus.SUBORDINATE, self.s3.getFeature(InternalFeature.CLAUSE_STATUS))
        # check realisation
        self.assertEqual("says that the man gives the woman John's flower", \
                self.realiser.realise(self.say).getRealisation())

    # Test the various forms of a sentence, including subordinates.
    def testForm(self):
        # check the getter method
        self.assertEqual(Form.NORMAL, self.s1.getFeatureAsElement( \
                InternalFeature.VERB_PHRASE).getFeature(Feature.FORM))
        # infinitive
        self.s1.setFeature(Feature.FORM, Form.INFINITIVE)
        self.assertEqual("to kiss the man", self.realiser.realise(self.s1).getRealisation())
        # gerund with "there"
        self.s2.setFeature(Feature.FORM, Form.GERUND)
        self.assertEqual("there being the dog on the rock", self.realiser.realise(self.s2).getRealisation())
        # gerund with possessive
        self.s3.setFeature(Feature.FORM, Form.GERUND)
        self.assertEqual("the man's giving the woman John's flower", \
                self.realiser.realise(self.s3).getRealisation())
        # imperative
        self.s3.setFeature(Feature.FORM, Form.IMPERATIVE)
        self.assertEqual("give the woman John's flower", self.realiser.realise(self.s3).getRealisation())
        # subordinating the imperative to a verb should turn it to infinitive
        self.say.addComplement(self.s3)
        self.assertEqual("says to give the woman John's flower", \
                self.realiser.realise(self.say).getRealisation())
        # imperative -- case II
        self.s4.setFeature(Feature.FORM, Form.IMPERATIVE)
        self.assertEqual("however tomorrow pick up the balls in the shop", \
                self.realiser.realise(self.s4).getRealisation())
        # infinitive -- case II
        self.s4 = self.phraseFactory.createClause()
        self.s4.setFeature(Feature.CUE_PHRASE, "however")
        self.s4.addFrontModifier("tomorrow")
        subject = CoordinatedPhraseElement(self.phraseFactory.createNounPhrase("Jane"), \
                self.phraseFactory.createNounPhrase("Andrew"))
        self.s4.setFeature(InternalFeature.SUBJECTS, subject)
        pick = self.phraseFactory.createVerbPhrase("pick up")
        self.s4.setFeature(InternalFeature.VERB_PHRASE, pick)
        self.s4.setObject("the balls")
        self.s4.addPostModifier("in the shop")
        self.s4.setFeature(Feature.TENSE, Tense.FUTURE)
        self.s4.setFeature(Feature.FORM, Form.INFINITIVE)
        self.assertEqual("however to pick up the balls in the shop tomorrow", \
                self.realiser.realise(self.s4).getRealisation())

    # Slightly more complex tests for forms.
    def testForm2(self):
        # set s4 as subject of a new sentence
        temp = self.phraseFactory.createClause(self.s4, "be", "recommended")
        self.assertEqual("however tomorrow Jane and Andrew's picking up the " + \
                "balls in the shop is recommended", \
                self.realiser.realise(temp).getRealisation())
        # compose self with a new sentence
        # ER - switched direct and indirect object in sentence
        temp2 = self.phraseFactory.createClause("I", "tell", temp)
        temp2.setFeature(Feature.TENSE, Tense.FUTURE)
        indirectObject = self.phraseFactory.createNounPhrase("John")
        temp2.setIndirectObject(indirectObject)
        self.assertEqual("I will tell John that however tomorrow Jane and " +  \
                "Andrew's picking up the balls in the shop is recommended", \
                self.realiser.realise(temp2).getRealisation())
        # turn s4 to imperative and put it in indirect object position
        self.s4 = self.phraseFactory.createClause()
        self.s4.setFeature(Feature.CUE_PHRASE, "however")
        self.s4.addFrontModifier("tomorrow")
        subject =  CoordinatedPhraseElement(self.phraseFactory.createNounPhrase("Jane"), \
                self.phraseFactory.createNounPhrase("Andrew"))
        self.s4.setSubject(subject)
        pick = self.phraseFactory.createVerbPhrase("pick up")
        self.s4.setVerbPhrase(pick)
        self.s4.setObject("the balls")
        self.s4.addPostModifier("in the shop")
        self.s4.setFeature(Feature.TENSE, Tense.FUTURE)
        self.s4.setFeature(Feature.FORM, Form.IMPERATIVE)
        temp2 = self.phraseFactory.createClause("I", "tell", self.s4)
        indirectObject = self.phraseFactory.createNounPhrase("John")
        temp2.setIndirectObject(indirectObject)
        temp2.setFeature(Feature.TENSE, Tense.FUTURE)
        self.assertEqual("I will tell John however to pick up the balls " \
                + "in the shop tomorrow", self.realiser.realise(temp2).getRealisation())

    # Tests for gerund forms and genitive subjects.
    def testGerundsubject(self):
        # the man's giving the woman John's flower upset Peter
        _s4 = self.phraseFactory.createClause()
        _s4.setVerbPhrase(self.phraseFactory.createVerbPhrase("upset"))
        _s4.setFeature(Feature.TENSE, Tense.PAST)
        _s4.setObject(self.phraseFactory.createNounPhrase("Peter"))
        self.s3.setFeature(Feature.PERFECT, True)
        # set the sentence as subject of another: makes it a gerund
        _s4.setSubject(self.s3)
        # suppress the genitive realisation of the NP subject in gerund sentences
        self.s3.setFeature(Feature.SUPPRESS_GENITIVE_IN_GERUND, True)
        # check the realisation: subject should not be genitive
        self.assertEqual("the man having given the woman John's flower upset Peter", \
                self.realiser.realise(_s4).getRealisation())

    # Some tests for multiple embedded sentences.
    def testComplexSentence1(self):
        self.setUp()
        # the man's giving the woman John's flower upset Peter
        complexS = self.phraseFactory.createClause()
        complexS.setVerbPhrase(self.phraseFactory.createVerbPhrase("upset"))
        complexS.setFeature(Feature.TENSE, Tense.PAST)
        complexS.setObject(self.phraseFactory.createNounPhrase("Peter"))
        self.s3.setFeature(Feature.PERFECT, True)
        complexS.setSubject(self.s3)
        # check the realisation: subject should be genitive
        self.assertEqual("the man's having given the woman John's flower upset Peter", \
                self.realiser.realise(complexS).getRealisation())
        self.setUp()
        # coordinate sentences in subject position
        s5 = self.phraseFactory.createClause()
        s5.setSubject(self.phraseFactory.createNounPhrase("some", "person"))
        s5.setVerbPhrase(self.phraseFactory.createVerbPhrase("stroke"))
        s5.setObject(self.phraseFactory.createNounPhrase("the", "cat"))
        coord = CoordinatedPhraseElement(self.s3, s5)
        complexS = self.phraseFactory.createClause()
        complexS.setVerbPhrase(self.phraseFactory.createVerbPhrase("upset"))
        complexS.setFeature(Feature.TENSE, Tense.PAST)
        complexS.setObject(self.phraseFactory.createNounPhrase("Peter"))
        complexS.setSubject(coord)
        self.s3.setFeature(Feature.PERFECT, True)
        self.assertEqual("the man's having given the woman John's flower " \
                + "and some person's stroking the cat upset Peter", \
                self.realiser.realise(complexS).getRealisation())
        self.setUp()
        # now subordinate the complex sentence
        # coord.setClauseStatus(SPhraseSpec.ClauseType.MAIN)
        s6 = self.phraseFactory.createClause()
        s6.setVerbPhrase(self.phraseFactory.createVerbPhrase("tell"))
        s6.setFeature(Feature.TENSE, Tense.PAST)
        s6.setSubject(self.phraseFactory.createNounPhrase("the", "boy"))
        # ER - switched indirect and direct object
        indirect = self.phraseFactory.createNounPhrase("every", "girl")
        s6.setIndirectObject(indirect)
        complexS = self.phraseFactory.createClause()
        complexS.setVerbPhrase(self.phraseFactory.createVerbPhrase("upset"))
        complexS.setFeature(Feature.TENSE, Tense.PAST)
        complexS.setObject(self.phraseFactory.createNounPhrase("Peter"))
        s6.setObject(complexS)
        coord = CoordinatedPhraseElement(self.s3, s5)
        complexS.setSubject(coord)
        self.s3.setFeature(Feature.PERFECT, True)
        self.assertEqual("the boy told every girl that the man's having given the woman " \
                        + "John's flower and some person's stroking the cat " \
                        + "upset Peter", self.realiser.realise(s6).getRealisation())

    # More coordination tests.
    def testComplexSentence3(self):
        self.setUp()
        self.s1 = self.phraseFactory.createClause()
        self.s1.setSubject(self.woman)
        self.s1.setVerb("kiss")
        self.s1.setObject(self.man)
        _man = self.phraseFactory.createNounPhrase("the", "man")
        self.s3 = self.phraseFactory.createClause()
        self.s3.setSubject(_man)
        self.s3.setVerb("give")
        flower = self.phraseFactory.createNounPhrase("flower")
        john = self.phraseFactory.createNounPhrase("John")
        john.setFeature(Feature.POSSESSIVE, True)
        flower.setSpecifier(john)
        self.s3.setObject(flower)
        _woman = self.phraseFactory.createNounPhrase("the", "woman")
        self.s3.setIndirectObject(_woman)
        # the coordinate sentence allows us to raise and lower complementiser
        coord2 = CoordinatedPhraseElement(self.s1, self.s3)
        coord2.setFeature(Feature.TENSE, Tense.PAST)
        #self.realiser.setDebugMode(True)
        self.assertEqual("the woman kissed the man and the man gave the woman John's flower", \
                self.realiser.realise(coord2).getRealisation())

    def testStringRecognition(self):
        # test recognition of forms of "be"
        _s1 = self.phraseFactory.createClause("my cat", "be", "sad")
        self.assertEqual("my cat is sad", self.realiser.realise(_s1).getRealisation())
        # test recognition of pronoun for afreement
        _s2 = self.phraseFactory.createClause("I", "want", "Mary")
        self.assertEqual("I want Mary", self.realiser.realise(_s2).getRealisation())
        # test recognition of pronoun for correct form
        subject = self.phraseFactory.createNounPhrase("dog")
        subject.setFeature(InternalFeature.SPECIFIER, "a")
        subject.addPostModifier("from next door")
        object = self.phraseFactory.createNounPhrase("I")
        s = self.phraseFactory.createClause(subject, "chase", object)
        s.setFeature(Feature.PROGRESSIVE, True)
        self.assertEqual("a dog from next door is chasing me", self.realiser.realise(s).getRealisation())

    # Tests complex agreement.
    def testAgreement(self):
        # basic agreement
        np = self.phraseFactory.createNounPhrase("dog")
        np.setSpecifier("the")
        np.addPreModifier("angry")
        _s1 = self.phraseFactory.createClause(np, "chase", "John")
        self.assertEqual("the angry dog chases John", self.realiser.realise(_s1).getRealisation())
        # plural
        np = self.phraseFactory.createNounPhrase("dog")
        np.setSpecifier("the")
        np.addPreModifier("angry")
        np.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        _s1 = self.phraseFactory.createClause(np, "chase", "John")
        self.assertEqual("the angry dogs chase John", self.realiser.realise(_s1).getRealisation())
        # test agreement with "there is"
        np = self.phraseFactory.createNounPhrase("dog")
        np.addPreModifier("angry")
        np.setFeature(Feature.NUMBER, NumberAgreement.SINGULAR)
        np.setSpecifier("a") #$NON-NLS-1$
        _s2 = self.phraseFactory.createClause("there", "be", np)
        self.assertEqual("there is an angry dog", self.realiser.realise(_s2).getRealisation())
        # plural with "there"
        np = self.phraseFactory.createNounPhrase("dog")
        np.addPreModifier("angry")
        np.setSpecifier("a")
        np.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        _s2 = self.phraseFactory.createClause("there", "be", np)
        self.assertEqual("there are some angry dogs", self.realiser.realise(_s2).getRealisation())

    # Tests passive.
    def testPassive(self):
        # passive with just complement
        _s1 = self.phraseFactory.createClause(None, "intubate", \
                self.phraseFactory.createNounPhrase("the", "baby"))
        _s1.setFeature(Feature.PASSIVE, True)
        self.assertEqual("the baby is intubated", self.realiser.realise(_s1).getRealisation())
        # passive with subject and complement
        _s1 = self.phraseFactory.createClause(None, "intubate", \
                self.phraseFactory.createNounPhrase("the", "baby"))
        _s1.setSubject(self.phraseFactory.createNounPhrase("the nurse"))
        _s1.setFeature(Feature.PASSIVE, True)
        self.assertEqual("the baby is intubated by the nurse", \
            self.realiser.realise(_s1).getRealisation())
        # passive with subject and indirect object
        _s2 = self.phraseFactory.createClause(None, "give",\
                self.phraseFactory.createNounPhrase("the", "baby"))
        morphine = self.phraseFactory.createNounPhrase("50ug of morphine")
        _s2.setIndirectObject(morphine)
        _s2.setFeature(Feature.PASSIVE, True)
        self.assertEqual("the baby is given 50ug of morphine", \
                self.realiser.realise(_s2).getRealisation())
        # passive with subject, complement and indirect object
        _s2 = self.phraseFactory.createClause(self.phraseFactory.createNounPhrase("the", "nurse"), \
                "give", self.phraseFactory.createNounPhrase("the", "baby"))
        morphine = self.phraseFactory.createNounPhrase("50ug of morphine")
        _s2.setIndirectObject(morphine)
        _s2.setFeature(Feature.PASSIVE, True)
        self.assertEqual("the baby is given 50ug of morphine by the nurse", \
                self.realiser.realise(_s2).getRealisation())
        # test agreement in passive
        _s3 = self.phraseFactory.createClause(\
                CoordinatedPhraseElement("my dog", "your cat"), "chase", "George")
        _s3.setFeature(Feature.TENSE, Tense.PAST)
        _s3.addFrontModifier("yesterday")
        self.assertEqual("yesterday my dog and your cat chased George", \
                self.realiser.realise(_s3).getRealisation())
        _s3 = self.phraseFactory.createClause(CoordinatedPhraseElement( \
                "my dog", "your cat"), "chase", self.phraseFactory.createNounPhrase("George"))
        _s3.setFeature(Feature.TENSE, Tense.PAST)
        _s3.addFrontModifier("yesterday")
        _s3.setFeature(Feature.PASSIVE, True)
        self.assertEqual("yesterday George was chased by my dog and your cat", \
                self.realiser.realise(_s3).getRealisation())
        # test correct pronoun forms
        _s4 = self.phraseFactory.createClause(self.phraseFactory.createNounPhrase("he"), "chase", \
                self.phraseFactory.createNounPhrase("I"))
        self.assertEqual("he chases me", self.realiser.realise(_s4).getRealisation())
        _s4 = self.phraseFactory.createClause(\
                self.phraseFactory.createNounPhrase("he"), "chase", self.phraseFactory.createNounPhrase("me"))
        _s4.setFeature(Feature.PASSIVE, True)
        self.assertEqual("I am chased by him", self.realiser.realise(_s4).getRealisation())
        # same thing, but giving the S constructor "me". Should recognise correct pro anyway
        _s5 = self.phraseFactory.createClause("him", "chase", "I")
        self.assertEqual("he chases me", self.realiser.realise(_s5).getRealisation())
        _s5 = self.phraseFactory.createClause("him", "chase", "I")
        _s5.setFeature(Feature.PASSIVE, True)
        self.assertEqual("I am chased by him", self.realiser.realise(_s5).getRealisation())

    # Test that complements set within the VP are raised when sentence is passivised.
    def testPassiveWithInternalVPComplement(self):
        vp = self.phraseFactory.createVerbPhrase(self.phraseFactory.createWord("upset", LexicalCategory.VERB))
        vp.addComplement(self.phraseFactory.createNounPhrase("the", "man"))
        _s6 = self.phraseFactory.createClause(self.phraseFactory.createNounPhrase("the", "child"), vp)
        _s6.setFeature(Feature.TENSE, Tense.PAST)
        self.assertEqual("the child upset the man", self.realiser.realise(_s6).getRealisation())
        _s6.setFeature(Feature.PASSIVE, True)
        self.assertEqual("the man was upset by the child", self.realiser.realise(_s6).getRealisation())

    # Tests tenses with modals.
    def testModal(self):
        self.setUp()
        # simple modal in present tense
        self.s3.setFeature(Feature.MODAL, "should")
        self.assertEqual("the man should give the woman John's flower", \
                self.realiser.realise(self.s3).getRealisation())
        # modal + future -- uses present
        self.setUp()
        self.s3.setFeature(Feature.MODAL, "should")
        self.s3.setFeature(Feature.TENSE, Tense.FUTURE)
        self.assertEqual("the man should give the woman John's flower", \
                self.realiser.realise(self.s3).getRealisation())
        # modal + present progressive
        self.setUp()
        self.s3.setFeature(Feature.MODAL, "should")
        self.s3.setFeature(Feature.TENSE, Tense.FUTURE)
        self.s3.setFeature(Feature.PROGRESSIVE, True)
        self.assertEqual("the man should be giving the woman John's flower", \
                self.realiser.realise(self.s3).getRealisation())
        # modal + past tense
        self.setUp()
        self.s3.setFeature(Feature.MODAL, "should")
        self.s3.setFeature(Feature.TENSE, Tense.PAST)
        self.assertEqual("the man should have given the woman John's flower", \
                self.realiser.realise(self.s3).getRealisation())
        # modal + past progressive
        self.setUp()
        self.s3.setFeature(Feature.MODAL, "should")
        self.s3.setFeature(Feature.TENSE, Tense.PAST)
        self.s3.setFeature(Feature.PROGRESSIVE, True)
        self.assertEqual("the man should have been giving the woman John's flower", \
                self.realiser.realise(self.s3).getRealisation())

    # Test for passivisation with mdoals
    def testModalWithPassive(self):
        object = self.phraseFactory.createNounPhrase("the", "pizza")
        post = self.phraseFactory.createAdjectivePhrase("good")
        as_obj = self.phraseFactory.createAdverbPhrase("as")
        as_obj.addComplement(post)
        verb = self.phraseFactory.createVerbPhrase("classify")
        verb.addPostModifier(as_obj)
        verb.addComplement(object)
        s = self.phraseFactory.createClause()
        s.setVerbPhrase(verb)
        s.setFeature(Feature.MODAL, "can")
        # s.setFeature(Feature.FORM, Form.INFINITIVE)
        s.setFeature(Feature.PASSIVE, True)
        self.assertEqual("the pizza can be classified as good", \
                self.realiser.realise(s).getRealisation())

    def testPassiveWithPPCompl(self):
        # passive with just complement
        subject = self.phraseFactory.createNounPhrase("wave")
        subject.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        object = self.phraseFactory.createNounPhrase("surfer")
        object.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        _s1 = self.phraseFactory.createClause(subject, "carry", object)
        # add a PP complement
        pp = self.phraseFactory.createPrepositionPhrase("to", self.phraseFactory.createNounPhrase("the", "shore"))
        pp.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.INDIRECT_OBJECT)
        _s1.addComplement(pp)
        _s1.setFeature(Feature.PASSIVE, True)
        self.assertEqual("surfers are carried to the shore by waves", \
                self.realiser.realise(_s1).getRealisation())

    def testPassiveWithPPMod(self):
        # passive with just complement
        subject = self.phraseFactory.createNounPhrase("wave")
        subject.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        object = self.phraseFactory.createNounPhrase("surfer")
        object.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        _s1 = self.phraseFactory.createClause(subject, "carry", object)
        # add a PP complement
        pp = self.phraseFactory.createPrepositionPhrase("to", \
                self.phraseFactory.createNounPhrase("the", "shore"))
        _s1.addPostModifier(pp)
        _s1.setFeature(Feature.PASSIVE, True)
        self.assertEqual("surfers are carried to the shore by waves", \
                self.realiser.realise(_s1).getRealisation())

    def testCuePhrase(self):
        subject = self.phraseFactory.createNounPhrase("wave")
        subject.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        object = self.phraseFactory.createNounPhrase("surfer")
        object.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        _s1 = self.phraseFactory.createClause(subject, "carry", object)
        # add a PP complement
        pp = self.phraseFactory.createPrepositionPhrase("to", \
                self.phraseFactory.createNounPhrase("the", "shore"))
        _s1.addPostModifier(pp)
        _s1.setFeature(Feature.PASSIVE, True)
        _s1.addFrontModifier("however")
        #without comma separation of cue phrase
        self.assertEqual( "however surfers are carried to the shore by waves", \
                self.realiser.realise(_s1).getRealisation())
        #with comma separation
        self.realiser.setCommaSepCuephrase(True)
        self.assertEqual("however, surfers are carried to the shore by waves", \
                self.realiser.realise(_s1).getRealisation())

    # Check that setComplement replaces earlier complements
    def testSetComplement(self):
        s = self.phraseFactory.createClause()
        s.setSubject("I")
        s.setVerb("see")
        s.setObject("a dog")
        self.assertEqual("I see a dog", self.realiser.realise(s).getRealisation())
        s.setObject("a cat")
        self.assertEqual("I see a cat", self.realiser.realise(s).getRealisation())
        s.setObject("a wolf")
        self.assertEqual("I see a wolf", self.realiser.realise(s).getRealisation())

    # Test for subclauses involving WH-complements Based on a query by Owen Bennett
    def testSubclauses(self):
        # Once upon a time, there was an Accountant, called Jeff, who lived in
        # a forest. # main sentence
        acct = self.phraseFactory.createNounPhrase("a", "accountant")
        # first postmodifier of "an accountant"
        sub1 = self.phraseFactory.createVerbPhrase("call")
        sub1.addComplement("Jeff")
        sub1.setFeature(Feature.FORM, Form.PAST_PARTICIPLE)
        # self is an appositive modifier, which makes simplenlg put it between commas
        sub1.setFeature(Feature.APPOSITIVE, True)
        acct.addPostModifier(sub1)
        # second postmodifier of "an accountant" is "who lived in a forest"
        sub2 = self.phraseFactory.createClause()
        subvp = self.phraseFactory.createVerbPhrase("live")
        subvp.setFeature(Feature.TENSE, Tense.PAST)
        subvp.setComplement(self.phraseFactory.createPrepositionPhrase("in", \
                self.phraseFactory.createNounPhrase("a", "forest")))
        sub2.setVerbPhrase(subvp)
        # simplenlg can't yet handle wh-clauses in NPs, so we need to hack it
        # by setting the subject to "who"
        sub2.setSubject("who")
        acct.addPostModifier(sub2)
        # main sentence
        s = self.phraseFactory.createClause("there", "be", acct)
        s.setFeature(Feature.TENSE, Tense.PAST)
        # add front modifier "once upon a time"
        s.addFrontModifier("once upon a time")
        self.assertEqual("once upon a time there was an accountant, called Jeff, who lived in a forest", \
                self.realiser.realise(s).getRealisation())


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
