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
from simplenlg.features.Feature                      import *
from simplenlg.features.Tense                        import *
from simplenlg.framework.CoordinatedPhraseElement    import *
from simplenlg.framework.DocumentElement             import *
from simplenlg.framework.LexicalCategory             import *
from simplenlg.framework.NLGElement                  import *
from simplenlg.framework.NLGFactory                  import *
from simplenlg.framework.PhraseElement               import *
from simplenlg.phrasespec.AdvPhraseSpec              import *
from simplenlg.phrasespec.NPPhraseSpec               import *
from simplenlg.phrasespec.SPhraseSpec                import *
from simplenlg.phrasespec.VPPhraseSpec               import *


# Tests that check that realization of different Features against NLGElements.
class FeatureTest(SimpleNLG4Test):

    def setUp(self):
        super().setUp()
        self.docFactory = NLGFactory(self.lexicon)

    def tearDown(self):
        super().tearDown()
        self.docFactory = None

    # Tests use of the Possessive Feature.
    def testPossessiveFeature_PastTense(self):
        self.phraseFactory.setLexicon(self.lexicon)
        self.realiser.setLexicon(self.lexicon)
        # Create the pronoun 'she'
        she = self.phraseFactory.createWord("she",LexicalCategory.PRONOUN)
        # Set possessive on the pronoun to make it 'her'
        she.setFeature(Feature.POSSESSIVE, True)
        # Create a noun phrase with the subject lover and the determiner as she
        herLover = self.phraseFactory.createNounPhrase(she,"lover")
        # Create a clause to say 'he be her lover'
        clause = self.phraseFactory.createClause("he", "be", herLover)
        # Add the cue phrase need the comma as orthography
        # currently doesn't handle self.
        # This could be expanded to be a noun phrase with determiner
        # 'two' and noun 'week', set to plural and with a premodifier of
        # 'after'
        clause.setFeature(Feature.CUE_PHRASE, "after two weeks,")
        # Add the 'for a fortnight' as a post modifier. Alternatively
        # self could be added as a prepositional phrase 'for' with a
        # complement of a noun phrase ('a' 'fortnight')
        clause.addPostModifier("for a fortnight")
        # Set 'be' to 'was' as past tense
        clause.setFeature(Feature.TENSE,Tense.PAST)
        # Add the clause to a sentence.phraseFactory
        sentence1 = self.docFactory.createSentence(clause)
        # Realise the sentence
        realised = self.realiser.realise(sentence1)
        self.assertEqual("After two weeks, he was her lover for a fortnight.", \
                realised.getRealisation())

    # Basic tests.
    def testTwoPossessiveFeature_PastTense(self):
        self.phraseFactory.setLexicon(self.lexicon)
        # Create the pronoun 'she'
        she = self.phraseFactory.createWord("she",LexicalCategory.PRONOUN)
        # Set possessive on the pronoun to make it 'her'
        she.setFeature(Feature.POSSESSIVE, True)
        # Create a noun phrase with the subject lover and the determiner
        # as she
        herLover = self.phraseFactory.createNounPhrase(she,"lover")
        herLover.setPlural(True)
        # Create the pronoun 'he'
        he = self.phraseFactory.createNounPhrase(LexicalCategory.PRONOUN,"he")
        he.setPlural(True)
        # Create a clause to say 'they be her lovers'
        clause = self.phraseFactory.createClause(he, "be", herLover)
        clause.setFeature(Feature.POSSESSIVE, True)
        # Add the cue phrase need the comma as orthography
        # currently doesn't handle self.
        # This could be expanded to be a noun phrase with determiner
        # 'two' and noun 'week', set to plural and with a premodifier of
        # 'after'
        clause.setFeature(Feature.CUE_PHRASE, "after two weeks,")
        # Add the 'for a fortnight' as a post modifier. Alternatively
        # self could be added as a prepositional phrase 'for' with a
        # complement of a noun phrase ('a' 'fortnight')
        clause.addPostModifier("for a fortnight")
        # Set 'be' to 'was' as past tense
        clause.setFeature(Feature.TENSE,Tense.PAST)
        # Add the clause to a sentence.
        sentence1 = self.docFactory.createSentence(clause)
        # Realise the sentence
        realised = self.realiser.realise(sentence1)
        self.assertEqual("After two weeks, they were her lovers for a fortnight.", \
                realised.getRealisation())

    # Test use of the Complementiser feature by combining two S's using cue phrase and gerund.
    def testComplementiserFeature_PastTense(self):
        self.phraseFactory.setLexicon(self.lexicon)
        born = self.phraseFactory.createClause("Dave Bus", "be", "born")
        born.setFeature(Feature.TENSE,Tense.PAST)
        born.addPostModifier("in")
        born.setFeature(Feature.COMPLEMENTISER, "which")
        theHouse = self.phraseFactory.createNounPhrase("the", "house")
        theHouse.addComplement(born)
        clause = self.phraseFactory.createClause(theHouse, "be", \
                self.phraseFactory.createPrepositionPhrase("in", "Edinburgh"))
        sentence = self.docFactory.createSentence(clause)
        realised = self.realiser.realise(sentence)
        # Retrieve the realisation and dump it to the console
        self.assertEqual("The house which Dave Bus was born in is in Edinburgh.", \
                realised.getRealisation())

    # Test use of the Complementiser feature in a  CoordinatedPhraseElement by combine two S's using cue phrase and gerund.
    def testComplementiserFeatureInACoordinatePhrase_PastTense(self):
        self.phraseFactory.setLexicon(self.lexicon)
        dave = self.phraseFactory.createWord("Dave Bus", LexicalCategory.NOUN)
        albert = self.phraseFactory.createWord("Albert", LexicalCategory.NOUN)
        coord1 = CoordinatedPhraseElement(dave, albert)
        born = self.phraseFactory.createClause(coord1, "be", "born")
        born.setFeature(Feature.TENSE,Tense.PAST)
        born.addPostModifier("in")
        born.setFeature(Feature.COMPLEMENTISER, "which")
        theHouse = self.phraseFactory.createNounPhrase("the", "house")
        theHouse.addComplement(born)
        clause = self.phraseFactory.createClause(theHouse, "be", \
                self.phraseFactory.createPrepositionPhrase("in", "Edinburgh"))
        sentence = self.docFactory.createSentence(clause)
        realised = self.realiser.realise(sentence)
        # Retrieve the realisation and dump it to the console
        self.assertEqual("The house which Dave Bus and Albert were born in is in Edinburgh.", \
                realised.getRealisation())

    # Test the use of the Progressive and Complementiser Features in future tense.
    def testProgressiveAndComplementiserFeatures_FutureTense(self):
        self.phraseFactory.setLexicon(self.lexicon)
        # Inner clause is 'I' 'make' 'sentence' 'for'.
        inner = self.phraseFactory.createClause("I","make", "sentence for")
        # Inner clause set to progressive.
        inner.setFeature(Feature.PROGRESSIVE,True)
        #Complementiser on inner clause is 'whom'
        inner.setFeature(Feature.COMPLEMENTISER, "whom")
        # create the engineer and add the inner clause as post modifier
        engineer = self.phraseFactory.createNounPhrase("the engineer")
        engineer.addComplement(inner)
        # Outer clause is: 'the engineer' 'go' (preposition 'to' 'holidays')
        outer = self.phraseFactory.createClause(engineer,"go", self.phraseFactory.createPrepositionPhrase("to","holidays"))
        # Outer clause tense is Future.
        outer.setFeature(Feature.TENSE, Tense.FUTURE)
        # Possibly progressive as well not sure.
        outer.setFeature(Feature.PROGRESSIVE,True)
        #Outer clause postmodifier would be 'tomorrow'
        outer.addPostModifier("tomorrow")
        sentence = self.docFactory.createSentence(outer)
        realised = self.realiser.realise(sentence)
        # Retrieve the realisation and dump it to the console
        self.assertEqual("The engineer whom I am making sentence for will be going to holidays tomorrow.", \
                realised.getRealisation())

    # Tests the use of the Complementiser, Passive, Perfect features in past tense.
    def testComplementiserPassivePerfectFeatures_PastTense(self):
        self.setUp()
        self.realiser.setLexicon(self.lexicon)
        inner = self.phraseFactory.createClause("I", "play", "poker")
        inner.setFeature(Feature.TENSE,Tense.PAST)
        inner.setFeature(Feature.COMPLEMENTISER, "where")
        house = self.phraseFactory.createNounPhrase("the", "house")
        house.addComplement(inner)
        outer = self.phraseFactory.createClause(None, "abandon", house)
        outer.addPostModifier("since 1986")
        outer.setFeature(Feature.PASSIVE, True)
        outer.setFeature(Feature.PERFECT, True)
        sentence = self.docFactory.createSentence(outer)
        realised = self.realiser.realise(sentence)
        # Retrieve the realisation and dump it to the console
        self.assertEqual("The house where I played poker has been abandoned since 1986.", \
                realised.getRealisation())

    # Tests the user of the progressive and complementiser featuers in past tense.
    def testProgressiveComplementiserFeatures_PastTense(self):
        self.phraseFactory.setLexicon(self.lexicon)
        sandwich = self.phraseFactory.createNounPhrase(LexicalCategory.NOUN, "sandwich")
        sandwich.setPlural(True)
        first = self.phraseFactory.createClause("I", "make", sandwich)
        first.setFeature(Feature.TENSE,Tense.PAST)
        first.setFeature(Feature.PROGRESSIVE,True)
        first.setPlural(False)
        second = self.phraseFactory.createClause("the mayonnaise", "run out")
        second.setFeature(Feature.TENSE,Tense.PAST)
        second.setFeature(Feature.COMPLEMENTISER, "when")
        first.addComplement(second)
        sentence = self.docFactory.createSentence(first)
        realised = self.realiser.realise(sentence)
        # Retrieve the realisation and dump it to the console
        self.assertEqual("I was making sandwiches when the mayonnaise ran out.", \
                realised.getRealisation())

   # Test the use of Passive in creating a Passive sentence structure: <Object> + [be] + <verb> + [by] + [Subject].
    def testPassiveFeature(self):
        self.realiser.setLexicon(self.lexicon)
        phrase = self.phraseFactory.createClause("recession", "affect", "value")
        phrase.setFeature(Feature.PASSIVE, True)
        sentence = self.docFactory.createSentence(phrase)
        realised = self.realiser.realise(sentence)
        self.assertEqual("Value is affected by recession.", realised.getRealisation())

    # Test for repetition of the future auxiliary "will", courtesy of Luxor Vlonjati
    def testFutureTense(self):
        test = self.phraseFactory.createClause()
        subj = self.phraseFactory.createNounPhrase("I")
        verb = self.phraseFactory.createVerbPhrase("go")
        adverb = self.phraseFactory.createAdverbPhrase("tomorrow")
        test.setSubject(subj)
        test.setVerbPhrase(verb)
        test.setFeature(Feature.TENSE, Tense.FUTURE)
        test.addPostModifier(adverb)
        sentence = self.realiser.realiseSentence(test)
        self.assertEqual("I will go tomorrow.", sentence)
        test2 = self.phraseFactory.createClause()
        vb = self.phraseFactory.createWord("go", LexicalCategory.VERB)
        test2.setSubject(subj)
        test2.setVerb(vb)
        test2.setFeature(Feature.TENSE, Tense.FUTURE)
        test2.addPostModifier(adverb)
        sentence2 = self.realiser.realiseSentence(test)
        self.assertEqual("I will go tomorrow.", sentence2)


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
