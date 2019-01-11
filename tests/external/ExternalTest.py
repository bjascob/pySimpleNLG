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
sys.path.append('../..')
#from simplenlg.aggregation.ClauseCoordinationRule  import *
from simplenlg.features.Feature                    import *
from simplenlg.features.Form                       import *
from simplenlg.features.Gender                     import *
from simplenlg.features.InterrogativeType          import *
from simplenlg.features.LexicalFeature             import *
from simplenlg.features.NumberAgreement            import *
from simplenlg.features.Person                     import *
from simplenlg.features.Tense                      import *
from simplenlg.framework.CoordinatedPhraseElement  import *
from simplenlg.framework.DocumentElement           import *
from simplenlg.framework.InflectedWordElement      import *
from simplenlg.framework.LexicalCategory           import *
from simplenlg.framework.NLGElement                import *
from simplenlg.framework.NLGFactory                import *
from simplenlg.framework.PhraseElement             import *
from simplenlg.framework.WordElement               import *
from simplenlg.lexicon.Lexicon                     import *
from simplenlg.phrasespec.NPPhraseSpec             import *
from simplenlg.phrasespec.SPhraseSpec              import *
from simplenlg.phrasespec.VPPhraseSpec             import *
from simplenlg.realiser.english.Realiser           import *


# Tests from third parties
class ExternalTest(unittest.TestCase):

    # called before each test
    def setUp(self):
        self.lexicon       = Lexicon.getDefaultLexicon()
        self.phraseFactory = NLGFactory(self.lexicon)
        self.realiser      = Realiser(self.lexicon)

    # Basic tests
    def testForcher(self):
        # Bjorn Forcher's tests
        self.phraseFactory.setLexicon(self.lexicon)
        s1 = self.phraseFactory.createClause(None, "associate", "Marie")
        s1.setFeature(Feature.PASSIVE, True)
        pp1 = self.phraseFactory.createPrepositionPhrase("with")
        pp1.addComplement("Peter")
        pp1.addComplement("Paul")
        s1.addPostModifier(pp1)
        self.assertEqual("Marie is associated with Peter and Paul", self.realiser.realise(s1).getRealisation())
        s2 = self.phraseFactory.createClause()
        s2.setSubject(self.phraseFactory.createNounPhrase("Peter"))
        s2.setVerb("have")
        s2.setObject("something to do")
        s2.addPostModifier(self.phraseFactory.createPrepositionPhrase("with", "Paul"))
        self.assertEqual("Peter has something to do with Paul", self.realiser.realise(s2).getRealisation())

    def testLu(self):
        # Xin Lu's test
        self.phraseFactory.setLexicon(self.lexicon)
        s1 = self.phraseFactory.createClause("we", "consider", "John")
        s1.addPostModifier("a friend")
        self.assertEqual("we consider John a friend", self.realiser.realise(s1).getRealisation())

    def testDwight(self):
        # Rachel Dwight's test
        self.phraseFactory.setLexicon(self.lexicon)
        noun4 = self.phraseFactory.createNounPhrase("FGFR3 gene in every cell")
        noun4.setSpecifier("the")
        prep1 = self.phraseFactory.createPrepositionPhrase("of", noun4)
        noun1 = self.phraseFactory.createNounPhrase("the", "patient's mother")
        noun2 = self.phraseFactory.createNounPhrase("the", "patient's father")
        noun3 = self.phraseFactory.createNounPhrase("changed copy")
        noun3.addPreModifier("one")
        noun3.addComplement(prep1)
        coordNoun1 = CoordinatedPhraseElement(noun1, noun2)
        coordNoun1.setConjunction( "or")
        verbPhrase1 = self.phraseFactory.createVerbPhrase("have")
        verbPhrase1.setFeature(Feature.TENSE,Tense.PRESENT)
        sentence1 = self.phraseFactory.createClause(coordNoun1, verbPhrase1, noun3)
        #realiser.setDebugMode(True)
        string = "the patient's mother or the patient's father has one changed copy of the FGFR3 gene in every cell"
        self.assertEqual(string, self.realiser.realise(sentence1).getRealisation())
        # Rachel's second test
        noun3 = self.phraseFactory.createNounPhrase("a", "gene test")
        noun2 = self.phraseFactory.createNounPhrase("an", "LDL test")
        noun1 = self.phraseFactory.createNounPhrase("the", "clinic")
        verbPhrase1 = self.phraseFactory.createVerbPhrase("perform")
        coord1 = CoordinatedPhraseElement(noun2, noun3)
        sentence1 = self.phraseFactory.createClause(noun1, verbPhrase1, coord1)
        sentence1.setFeature(Feature.TENSE,Tense.PAST)
        self.assertEqual("the clinic performed an LDL test and a gene test", \
                self.realiser.realise(sentence1).getRealisation())

    def testNovelli(self):
        # Nicole Novelli's test
        p = self.phraseFactory.createClause("Mary", "chase", "George")
        pp = self.phraseFactory.createPrepositionPhrase("in", "the park")
        p.addPostModifier(pp)
        self.assertEqual("Mary chases George in the park", self.realiser.realise(p).getRealisation())
        # another question from Nicole
        run = self.phraseFactory.createClause( "you", "go", "running")
        run.setFeature(Feature.MODAL, "should")
        run.addPreModifier("really")
        think = self.phraseFactory.createClause("I", "think")
        think.setObject(run)
        run.setFeature(Feature.SUPRESSED_COMPLEMENTISER, True)
        text = self.realiser.realise(think).getRealisation()
        self.assertEqual("I think you should really go running", text)

    def testPiotrek(self):
        # Piotrek Smulikowski's test
        self.phraseFactory.setLexicon(self.lexicon)
        sent = self.phraseFactory.createClause("I", "shoot", "the duck")
        sent.setFeature(Feature.TENSE,Tense.PAST)
        loc = self.phraseFactory.createPrepositionPhrase("at", "the Shooting Range")
        sent.addPostModifier(loc)
        sent.setFeature(Feature.CUE_PHRASE, "then")
        self.assertEqual("then I shot the duck at the Shooting Range", \
                self.realiser.realise(sent).getRealisation())

    def testPrescott(self):
        # Michael Prescott's test
        self.phraseFactory.setLexicon(self.lexicon)
        embedded = self.phraseFactory.createClause("Jill", "prod", "Spot")
        sent = self.phraseFactory.createClause("Jack", "see", embedded)
        embedded.setFeature(Feature.SUPRESSED_COMPLEMENTISER, True)
        embedded.setFeature(Feature.FORM, Form.BARE_INFINITIVE)
        self.assertEqual("Jack sees Jill prod Spot", self.realiser.realise(sent).getRealisation())

    def testWissner(self):
        # Michael Wissner's text
        p = self.phraseFactory.createClause("a wolf", "eat")
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        self.assertEqual("what does a wolf eat", self.realiser.realise(p).getRealisation())

    def testPhan(self):
        # Thomas Phan's text
          subjectElement = self.phraseFactory.createNounPhrase("I")
          verbElement = self.phraseFactory.createVerbPhrase("run")
          prepPhrase = self.phraseFactory.createPrepositionPhrase("from")
          prepPhrase.addComplement("home")
          verbElement.addComplement(prepPhrase)
          newSentence = self.phraseFactory.createClause()
          newSentence.setSubject(subjectElement)
          newSentence.setVerbPhrase(verbElement)
          self.assertEqual("I run from home", self.realiser.realise(newSentence).getRealisation())

    def testKerber(self):
        # Frederic Kerber's tests
        sp =  self.phraseFactory.createClause("he", "need")
        secondSp = self.phraseFactory.createClause()
        secondSp.setVerb("build")
        secondSp.setObject("a house")
        secondSp.setFeature(Feature.FORM,Form.INFINITIVE)
        sp.setObject("stone")
        sp.addComplement(secondSp)
        self.assertEqual("he needs stone to build a house", self.realiser.realise(sp).getRealisation())
        sp2 =  self.phraseFactory.createClause("he", "give")
        sp2.setIndirectObject("I")
        sp2.setObject("the book")
        self.assertEqual("he gives me the book", self.realiser.realise(sp2).getRealisation())

    def testStephenson(self):
        # Bruce Stephenson's test
        qs2 = self.phraseFactory.createClause()
        qs2.setSubject("moles of Gold")
        qs2.setVerb("are")
        qs2.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        qs2.setFeature(Feature.PASSIVE, False)
        qs2.setFeature(Feature.INTERROGATIVE_TYPE,InterrogativeType.HOW_MANY)
        qs2.setObject("in a 2.50 g sample of pure Gold")
        sentence = self.phraseFactory.createSentence(qs2)
        self.assertEqual("How many moles of Gold are in a 2.50 g sample of pure Gold?", \
                self.realiser.realise(sentence).getRealisation())

    def testPierre(self):
        # John Pierre's test
        p = self.phraseFactory.createClause("Mary", "chase", "George")
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_OBJECT)
        self.assertEqual("What does Mary chase?", self.realiser.realiseSentence(p))
        p = self.phraseFactory.createClause("Mary", "chase", "George")
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        self.assertEqual("Does Mary chase George?", self.realiser.realiseSentence(p))
        p = self.phraseFactory.createClause("Mary", "chase", "George")
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHERE)
        self.assertEqual("Where does Mary chase George?", self.realiser.realiseSentence(p))
        p = self.phraseFactory.createClause("Mary", "chase", "George")
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHY)
        self.assertEqual("Why does Mary chase George?", self.realiser.realiseSentence(p))
        p = self.phraseFactory.createClause("Mary", "chase", "George")
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.HOW)
        self.assertEqual("How does Mary chase George?", self.realiser.realiseSentence(p))

    def testData2TextTest(self):
        # Data2Text tests
        # test OK to have number at end of sentence
        p = self.phraseFactory.createClause("the dog", "weigh", "12")
        self.assertEqual("The dog weighes 12.", self.realiser.realiseSentence(p))
        # test OK to have "there be" sentence with "there" as a StringElement
        dataDropout2 = self.phraseFactory.createNLGElement("data dropouts")
        dataDropout2.setPlural(True)
        sentence2 = self.phraseFactory.createClause()
        sentence2.setSubject(self.phraseFactory.createStringElement("there"))
        sentence2.setVerb("be")
        sentence2.setObject(dataDropout2)
        self.assertEqual("There are data dropouts.", self.realiser.realiseSentence(sentence2))
        # test OK to have gerund form verb
        weather1 = self.phraseFactory.createClause("SE 10-15", "veer", "S 15-20")
        weather1.setFeature(Feature.FORM, Form.GERUND)
        self.assertEqual("SE 10-15 veering S 15-20.", self.realiser.realiseSentence(weather1))
        # test OK to have subject only
        weather2 = self.phraseFactory.createClause("cloudy and misty", "be", "XXX")
        weather2.getVerbPhrase().setFeature(Feature.ELIDED, True)
        self.assertEqual("Cloudy and misty.", self.realiser.realiseSentence(weather2))
        # test OK to have VP only
        weather3 = self.phraseFactory.createClause("S 15-20", "increase", "20-25")
        weather3.setFeature(Feature.FORM, Form.GERUND)
        weather3.getSubject().setFeature(Feature.ELIDED, True)
        self.assertEqual("Increasing 20-25.", self.realiser.realiseSentence(weather3))
        # conjoined test
        weather4 = self.phraseFactory.createClause("S 20-25", "back", "SSE")
        weather4.setFeature(Feature.FORM, Form.GERUND)
        weather4.getSubject().setFeature(Feature.ELIDED, True)
        coord = CoordinatedPhraseElement()
        coord.addCoordinate(weather1)
        coord.addCoordinate(weather3)
        coord.addCoordinate(weather4)
        coord.setConjunction("then")
        self.assertEqual("SE 10-15 veering S 15-20, increasing 20-25 then backing SSE.", self.realiser.realiseSentence(coord))
        # no verb
        weather5 = self.phraseFactory.createClause("rain", None, "likely")
        self.assertEqual("Rain likely.", self.realiser.realiseSentence(weather5))

    @unittest.skip('aggregation not implemented')
    def testRafael(self):
        # Rafael Valle's tests
        ss = []
        coord = ClauseCoordinationRule()
        coord.setFactory(self.phraseFactory)

        ss.add(self.agreePhrase("John Lennon")) # john lennon agreed with it
        ss.add(self.disagreePhrase("Geri Halliwell")) # Geri Halliwell disagreed with it
        ss.add(self.commentPhrase("Melanie B")) # Mealnie B commented on it
        ss.add(self.agreePhrase("you")) # you agreed with it
        ss.add(self.commentPhrase("Emma Bunton")) #Emma Bunton commented on it

        results = coord.apply(ss)
        ret = [self.realiser.realise(e).getRealisation() for e in results]
        string = "[John Lennon and you agreed with it, Geri Halliwell disagreed with it, Melanie B and Emma Bunton commented on it]"
        self.assertEqual(string, ret.toString())

    def commentPhrase(self, name):  # used by testRafael
        s = self.phraseFactory.createClause()
        s.setSubject(self.phraseFactory.createNounPhrase(name))
        s.setVerbPhrase(self.phraseFactory.createVerbPhrase("comment on"))
        s.setObject("it")
        s.setFeature(Feature.TENSE, Tense.PAST)
        return s

    def agreePhrase(self, name):  # used by testRafael
        s = self.phraseFactory.createClause()
        s.setSubject(self.phraseFactory.createNounPhrase(name))
        s.setVerbPhrase(self.phraseFactory.createVerbPhrase("agree with"))
        s.setObject("it")
        s.setFeature(Feature.TENSE, Tense.PAST)
        return s

    def disagreePhrase(self, name):  # used by testRafael
        s = self.phraseFactory.createClause()
        s.setSubject(self.phraseFactory.createNounPhrase(name))
        s.setVerbPhrase(self.phraseFactory.createVerbPhrase("disagree with"))
        s.setObject("it")
        s.setFeature(Feature.TENSE, Tense.PAST)
        return s


    @unittest.skip('aggregation not implemented')
    def testWkipedia(self):
        # test code fragments in wikipedia realisation
        subject = self.phraseFactory.createNounPhrase("the", "woman")
        subject.setPlural(True)
        sentence = self.phraseFactory.createClause(subject, "smoke")
        sentence.setFeature(Feature.NEGATED, True)
        self.assertEqual("The women do not smoke.", realiser.realiseSentence(sentence))
        # aggregation
        s1 = self.phraseFactory.createClause("the man", "be", "hungry")
        s2 = self.phraseFactory.createClause("the man", "buy", "an apple")
        result = ClauseCoordinationRule().apply(s1, s2)
        self.assertEqual("The man is hungry and buys an apple.", realiser.realiseSentence(result))


    def testLean(self):
        # A Lean's test
        sentence = self.phraseFactory.createClause()
        sentence.setVerb("be")
        sentence.setObject("a ball")
        sentence.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_SUBJECT)
        self.assertEqual("What is a ball?", self.realiser.realiseSentence(sentence))
        sentence = self.phraseFactory.createClause()
        sentence.setVerb("be")
        object = self.phraseFactory.createNounPhrase("example")
        object.setPlural(True)
        object.addModifier("of jobs")
        sentence.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHAT_SUBJECT)
        sentence.setObject(object)
        self.assertEqual("What are examples of jobs?", self.realiser.realiseSentence(sentence))
        p = self.phraseFactory.createClause()
        sub1 = self.phraseFactory.createNounPhrase("Mary")
        sub1.setFeature(LexicalFeature.GENDER, Gender.FEMININE)
        sub1.setFeature(Feature.PRONOMINAL, True)
        sub1.setFeature(Feature.PERSON, Person.FIRST)
        p.setSubject(sub1)
        p.setVerb("chase")
        p.setObject("the monkey")
        output2 = self.realiser.realiseSentence(p)
        self.assertEqual("I chase the monkey.", output2)
        test = self.phraseFactory.createClause()
        subject = self.phraseFactory.createNounPhrase("Mary")
        subject.setFeature(Feature.PRONOMINAL, True)
        subject.setFeature(Feature.PERSON, Person.SECOND)
        test.setSubject(subject)
        test.setVerb("cry")
        test.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHY)
        test.setFeature(Feature.TENSE, Tense.PRESENT)
        self.assertEqual("Why do you cry?", self.realiser.realiseSentence(test))
        test = self.phraseFactory.createClause()
        subject = self.phraseFactory.createNounPhrase("Mary")
        subject.setFeature(Feature.PRONOMINAL, True)
        subject.setFeature(Feature.PERSON, Person.SECOND)
        test.setSubject(subject)
        test.setVerb("be")
        test.setObject("crying")
        test.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHY)
        test.setFeature(Feature.TENSE, Tense.PRESENT)
        self.assertEqual("Why are you crying?", self.realiser.realiseSentence(test))

    def testKalijurand(self):
        # K Kalijurand's test
        lemma = "walk"
        word = self.lexicon.lookupWord(lemma,  LexicalCategory.VERB)
        inflectedWord = InflectedWordElement(word)
        inflectedWord.setFeature(Feature.FORM, Form.PAST_PARTICIPLE)
        form = self.realiser.realise(inflectedWord).getRealisation()
        self.assertEqual("walked", form)
        inflectedWord = InflectedWordElement(word)
        inflectedWord.setFeature(Feature.PERSON, Person.THIRD)
        form = self.realiser.realise(inflectedWord).getRealisation()
        self.assertEqual("walks", form)

    def testLay(self):
        # Richard Lay's test
        lemma = "slap"
        word = self.lexicon.lookupWord(lemma,  LexicalCategory.VERB)
        inflectedWord = InflectedWordElement(word)
        inflectedWord.setFeature(Feature.FORM, Form.PRESENT_PARTICIPLE)
        form = self.realiser.realise(inflectedWord).getRealisation()
        self.assertEqual("slapping", form)
        v = self.phraseFactory.createVerbPhrase("slap")
        v.setFeature(Feature.PROGRESSIVE, True)
        progressive = self.realiser.realise(v).getRealisation()
        self.assertEqual("is slapping", progressive)


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
