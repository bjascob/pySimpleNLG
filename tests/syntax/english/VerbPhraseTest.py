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
from simplenlg.features      import DiscourseFunction, Feature, Form
from simplenlg.features      import InternalFeature, NumberAgreement, Person, Tense
from simplenlg.framework     import CoordinatedPhraseElement, NLGElement, PhraseElement, WordElement
from simplenlg.phrasespec    import SPhraseSpec, VPPhraseSpec


# These are tests for the verb phrase and coordinate VP classes.
class VerbPhraseTest(SimpleNLG4Test):
    # Some tests to check for an early bug which resulted in reduplication of
    # verb particles in the past tense e.g. "fall down down" or "creep up up"
    def testVerbParticle(self):
        v = self.phraseFactory.createVerbPhrase("fall down")
        self.assertEqual("down", v.getFeatureAsString(Feature.PARTICLE))
        self.assertEqual("fall", v.getVerb().getBaseForm())
        v.setFeature(Feature.TENSE,Tense.PAST)
        v.setFeature(Feature.PERSON, Person.THIRD)
        v.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        self.assertEqual("fell down", self.realiser.realise(v).getRealisation())
        v.setFeature(Feature.FORM, Form.PAST_PARTICIPLE)
        self.assertEqual("fallen down", self.realiser.realise(v).getRealisation())

    # Tests for the tense and aspect.
    def testSimplePastTense(self):
        # "fell down"
        self.fallDown.setFeature(Feature.TENSE,Tense.PAST)
        self.assertEqual("fell down", self.realiser.realise(self.fallDown).getRealisation())

    # Test tense aspect.
    def testTenseAspect(self):
        # had fallen down
        self.realiser.setLexicon(self.lexicon)
        self.fallDown.setFeature(Feature.TENSE,Tense.PAST)
        self.fallDown.setFeature(Feature.PERFECT, True)
        self.assertEqual("had fallen down", \
                self.realiser.realise(self.fallDown).getRealisation())
        # had been falling down
        self.fallDown.setFeature(Feature.PROGRESSIVE, True)
        self.assertEqual("had been falling down", \
                self.realiser.realise(self.fallDown).getRealisation())
        # will have been kicked
        self.kick.setFeature(Feature.PASSIVE, True)
        self.kick.setFeature(Feature.PERFECT, True)
        self.kick.setFeature(Feature.TENSE,Tense.FUTURE)
        self.assertEqual("will have been kicked", \
                self.realiser.realise(self.kick).getRealisation())
        # will have been being kicked
        self.kick.setFeature(Feature.PROGRESSIVE, True)
        self.assertEqual("will have been being kicked", \
                self.realiser.realise(self.kick).getRealisation())
        # will not have been being kicked
        self.kick.setFeature(Feature.NEGATED, True)
        self.assertEqual("will not have been being kicked", \
                self.realiser.realise(self.kick).getRealisation())
        # passivisation should suppress the complement
        self.kick.clearComplements()
        self.kick.addComplement(self.man)
        self.assertEqual("will not have been being kicked", \
                self.realiser.realise(self.kick).getRealisation())
        # de-passivisation should now give us "will have been kicking the man"
        self.kick.setFeature(Feature.PASSIVE, False)
        self.assertEqual("will not have been kicking the man", \
                self.realiser.realise(self.kick).getRealisation())
        # remove the future tense --
        # self is a test of an earlier bug that would still realise "will"
        self.kick.setFeature(Feature.TENSE,Tense.PRESENT)
        self.assertEqual("has not been kicking the man", \
                self.realiser.realise(self.kick).getRealisation())

    # Test for realisation of VP complements.
    def testComplementation1(self):
        # was kissing Mary
        mary = self.phraseFactory.createNounPhrase("Mary")
        mary.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.OBJECT)
        self.kiss.clearComplements()
        self.kiss.addComplement(mary)
        self.kiss.setFeature(Feature.PROGRESSIVE, True)
        self.kiss.setFeature(Feature.TENSE,Tense.PAST)
        self.assertEqual("was kissing Mary", \
                self.realiser.realise(self.kiss).getRealisation())
        mary2 = CoordinatedPhraseElement(mary, self.phraseFactory.createNounPhrase("Susan"))
        # add another complement -- should come out as "Mary and Susan"
        self.kiss.clearComplements()
        self.kiss.addComplement(mary2)
        self.assertEqual("was kissing Mary and Susan", \
                self.realiser.realise(self.kiss).getRealisation())
        # passivise -- should make the direct object complement disappear
        # Note: The verb doesn't come out as plural because agreement
        # is determined by the sentential subjects and self VP isn't inside a
        # sentence
        self.kiss.setFeature(Feature.PASSIVE, True)
        self.assertEqual("was being kissed", \
                self.realiser.realise(self.kiss).getRealisation())
        # make it plural (self is usually taken care of in SPhraseSpec)
        self.kiss.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        self.assertEqual("were being kissed", self.realiser.realise(self.kiss).getRealisation())
        # depassivise and add post-mod: yields "was kissing Mary in the room"
        self.kiss.addPostModifier(self.inTheRoom)
        self.kiss.setFeature(Feature.PASSIVE, False)
        self.kiss.setFeature(Feature.NUMBER, NumberAgreement.SINGULAR)
        self.assertEqual("was kissing Mary and Susan in the room", \
                self.realiser.realise(self.kiss).getRealisation())
        # passivise again: should make direct object disappear, but not postMod
        # ="was being kissed in the room"
        self.kiss.setFeature(Feature.PASSIVE, True)
        self.kiss.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        self.assertEqual("were being kissed in the room", \
                self.realiser.realise(self.kiss).getRealisation())

    # This tests for the default complement ordering, relative to pre and
    def testComplementation2(self):
        # give the woman the dog
        self.woman.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.INDIRECT_OBJECT)
        self.dog.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.OBJECT)
        self.give.clearComplements()
        self.give.addComplement(self.dog)
        self.give.addComplement(self.woman)
        self.assertEqual("gives the woman the dog", \
            self.realiser.realise(self.give).getRealisation())
        # add a few premodifiers and postmodifiers
        self.give.addPreModifier("slowly")
        self.give.addPostModifier(self.behindTheCurtain)
        self.give.addPostModifier(self.inTheRoom)
        self.assertEqual("slowly gives the woman the dog behind the curtain in the room", \
                self.realiser.realise(self.give).getRealisation())
        # reset the arguments
        self.give.clearComplements()
        self.give.addComplement(self.dog)
        womanBoy = CoordinatedPhraseElement(self.woman, self.boy)
        womanBoy.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.INDIRECT_OBJECT)
        self.give.addComplement(womanBoy)
        # if we unset the passive, we should get the indirect objects
        # they won't be coordinated
        self.give.setFeature(Feature.PASSIVE, False)
        self.assertEqual("slowly gives the woman and the boy the dog behind the curtain in the room", \
                self.realiser.realise(self.give).getRealisation())
        # set them to a coordinate instead
        # set ONLY the complement INDIRECT_OBJECT, leaves OBJECT intact
        self.give.clearComplements()
        self.give.addComplement(womanBoy)
        self.give.addComplement(self.dog)
        complements = self.give.getFeatureAsElementList(InternalFeature.COMPLEMENTS)
        indirectCount = 0
        for eachElement in complements:
            if DiscourseFunction.INDIRECT_OBJECT==eachElement.getFeature(InternalFeature.DISCOURSE_FUNCTION):
                indirectCount += 1
        self.assertEqual(1, indirectCount) # only one indirect object
        # where
        # there were two before
        self.assertEqual("slowly gives the woman and the boy the dog behind the curtain in the room", \
                self.realiser.realise(self.give).getRealisation())

    # Test for complements raised in the passive case.
    def testPassiveComplement(self):
        # add some arguments
        self.dog.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.OBJECT)
        self.woman.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.INDIRECT_OBJECT)
        self.give.addComplement(self.dog)
        self.give.addComplement(self.woman)
        self.assertEqual("gives the woman the dog", \
                self.realiser.realise(self.give).getRealisation())
        # add a few premodifiers and postmodifiers
        self.give.addPreModifier("slowly") #$NON-NLS-1$
        self.give.addPostModifier(self.behindTheCurtain)
        self.give.addPostModifier(self.inTheRoom)
        self.assertEqual("slowly gives the woman the dog behind the curtain in the room", \
                self.realiser.realise(self.give).getRealisation())
        # passivise: This should suppress "the dog"
        self.give.clearComplements()
        self.give.addComplement(self.dog)
        self.give.addComplement(self.woman)
        self.give.setFeature(Feature.PASSIVE, True)
        self.assertEqual("is slowly given the woman behind the curtain in the room", \
                self.realiser.realise(self.give).getRealisation())

    # Test VP with sentential complements. This tests for structures like "said
    # that John was walking"
    def testClausalComplement(self):
        self.phraseFactory.setLexicon(self.lexicon)
        s = self.phraseFactory.createClause()
        s.setSubject(self.phraseFactory.createNounPhrase("John"))
        # Create a sentence first
        maryAndSusan = CoordinatedPhraseElement(self.phraseFactory.createNounPhrase("Mary"), \
                self.phraseFactory.createNounPhrase("Susan"))
        self.kiss.clearComplements()
        s.setVerbPhrase(self.kiss)
        s.setObject(maryAndSusan)
        s.setFeature(Feature.PROGRESSIVE, True)
        s.setFeature(Feature.TENSE,Tense.PAST)
        s.addPostModifier(self.inTheRoom)
        self.assertEqual("John was kissing Mary and Susan in the room", \
                self.realiser.realise(s).getRealisation())
        # make the main VP past
        self.say.setFeature(Feature.TENSE,Tense.PAST)
        self.assertEqual("said", self.realiser.realise(self.say).getRealisation())
        # now add the sentence as complement of "say". Should make the sentence
        # subordinate
        # note that sentential punctuation is suppressed
        self.say.addComplement(s)
        self.assertEqual("said that John was kissing Mary and Susan in the room", \
                self.realiser.realise(self.say).getRealisation())
        # add a postModifier to the main VP
        # yields [says [that John was kissing Mary and Susan in the room]
        # [behind the curtain]]
        self.say.addPostModifier(self.behindTheCurtain)
        self.assertEqual("said that John was kissing Mary and Susan in the room behind the curtain", \
            self.realiser.realise(self.say).getRealisation())
        # create a sentential complement
        s2 = self.phraseFactory.createClause(self.phraseFactory.createNounPhrase("all"), \
                "be", self.phraseFactory.createAdjectivePhrase("fine"))
        s2.setFeature(Feature.TENSE,Tense.FUTURE)
        self.assertEqual("all will be fine", self.realiser.realise(s2).getRealisation())
        # add the complement to the VP
        # yields [said [that John was kissing Mary and Susan in the room and
        # all will be fine] [behind the curtain]]
        s3 = CoordinatedPhraseElement(s, s2)
        self.say.clearComplements()
        self.say.addComplement(s3)
        # first with outer complementiser suppressed
        s3.setFeature(Feature.SUPRESSED_COMPLEMENTISER, True)
        self.assertEqual("said that John was kissing Mary and Susan in the room " \
                + "and all will be fine behind the curtain",
                self.realiser.realise(self.say).getRealisation())
        self.setUp()
        s = self.phraseFactory.createClause()
        s.setSubject(self.phraseFactory.createNounPhrase("John"))
        # Create a sentence first
        maryAndSusan = CoordinatedPhraseElement(self.phraseFactory.createNounPhrase("Mary"), \
                self.phraseFactory.createNounPhrase("Susan"))
        s.setVerbPhrase(self.kiss)
        s.setObject(maryAndSusan)
        s.setFeature(Feature.PROGRESSIVE, True)
        s.setFeature(Feature.TENSE,Tense.PAST)
        s.addPostModifier(self.inTheRoom)
        s2 = self.phraseFactory.createClause(self.phraseFactory.createNounPhrase("all"), "be", \
                self.phraseFactory.createAdjectivePhrase("fine"))
        s2.setFeature(Feature.TENSE,Tense.FUTURE)
        # then with complementiser not suppressed and not aggregated
        s3 = CoordinatedPhraseElement(s, s2)
        self.say.addComplement(s3)
        self.say.setFeature(Feature.TENSE,Tense.PAST)
        self.say.addPostModifier(self.behindTheCurtain)
        self.assertEqual("said that John was kissing Mary and Susan in the room and " \
                + "that all will be fine behind the curtain", #$NON-NLS-1$
                self.realiser.realise(self.say).getRealisation())

    # Test VP coordination and aggregation:
    #
    # If the simplenlg.features of a coordinate VP are set, they should be
    # inherited by its daughter VP</LI>
    # 2. We can aggregate the coordinate VP so it's realised with one
    # wide-scope auxiliary</LI>
    def testCoordination(self):
        # simple case
        self.kiss.addComplement(self.dog)
        self.kick.addComplement(self.boy)
        coord1 = CoordinatedPhraseElement(self.kiss, self.kick)
        coord1.setFeature(Feature.PERSON, Person.THIRD)
        coord1.setFeature(Feature.TENSE,Tense.PAST)
        self.assertEqual("kissed the dog and kicked the boy", \
                self.realiser.realise(coord1).getRealisation())
        # with negation: should be inherited by all components
        coord1.setFeature(Feature.NEGATED, True)
        self.realiser.setLexicon(self.lexicon)
        self.assertEqual("did not kiss the dog and did not kick the boy", \
                self.realiser.realise(coord1).getRealisation())
        # set a modal
        coord1.setFeature(Feature.MODAL, "could")
        self.assertEqual("could not have kissed the dog and could not have kicked the boy", \
                self.realiser.realise(coord1).getRealisation())
        # set perfect and progressive
        coord1.setFeature(Feature.PERFECT, True)
        coord1.setFeature(Feature.PROGRESSIVE, True)
        self.assertEqual("could not have been kissing the dog and " \
                + "could not have been kicking the boy",
                self.realiser.realise(coord1).getRealisation())
        # now aggregate
        coord1.setFeature(Feature.AGGREGATE_AUXILIARY, True)
        self.assertEqual("could not have been kissing the dog and kicking the boy", \
                self.realiser.realise(coord1).getRealisation())


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
