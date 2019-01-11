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

#!/usr/bin/python3
from SimpleNLG4Test                                  import *
from simplenlg.features.Feature                      import *
from simplenlg.features.Tense                        import *
from simplenlg.framework.CoordinatedPhraseElement    import *
from simplenlg.framework.LexicalCategory             import *
from simplenlg.phrasespec                            import *


# Some tests for coordination, especially of coordinated VPs with modifiers.
class CoordinationTest(SimpleNLG4Test):
    # Check that empty coordinate phrases are not realised as "None"
    def testEmptyCoordination(self):
        # first a simple phrase with no coordinates
        coord = self.phraseFactory.createCoordinatedPhrase()
        self.assertEqual("", self.realiser.realise(coord).getRealisation())
        # now one with a premodifier and nothing else
        coord.addPreModifier(self.phraseFactory.createAdjectivePhrase("nice"))
        self.assertEqual("nice", self.realiser.realise(coord).getRealisation())
    # Test pre and post-modification of coordinate VPs inside a sentence.

    def testModifiedCoordVP(self):
        coord = self.phraseFactory.createCoordinatedPhrase(self.getUp, self.fallDown)
        coord.setFeature(Feature.TENSE, Tense.PAST)
        self.assertEqual("got up and fell down", self.realiser.realise(coord).getRealisation())
        # add a premodifier
        coord.addPreModifier("slowly")
        self.assertEqual("slowly got up and fell down", self.realiser.realise(coord).getRealisation())
        # adda postmodifier
        coord.addPostModifier(self.behindTheCurtain)
        self.assertEqual("slowly got up and fell down behind the curtain", \
                self.realiser.realise(coord).getRealisation())
        # put within the context of a sentence
        s = self.phraseFactory.createClause("Jake", coord)
        s.setFeature(Feature.TENSE, Tense.PAST)
        self.assertEqual("Jake slowly got up and fell down behind the curtain", \
                self.realiser.realise(s).getRealisation())
        # add premod to the sentence
        s.addPreModifier(self.lexicon.getWord("however", LexicalCategory.ADVERB))
        self.assertEqual("Jake however slowly got up and fell down behind the curtain", \
                self.realiser.realise(s).getRealisation())
        # add postmod to the sentence
        s.addPostModifier(self.inTheRoom)
        self.assertEqual("Jake however slowly got up and fell down behind the curtain in the room", \
                self.realiser.realise(s).getRealisation())

    # Test due to Chris Howell -- create a complex sentence with front modifier
    # and coordinateVP. This is a version in which we create the coordinate
    # phrase directly.
    def testCoordinateVPComplexSubject(self):
        # "As a result of the procedure the patient had an adverse contrast media reaction and went into cardiogenic shock."
        s = self.phraseFactory.createClause()
        s.setSubject(self.phraseFactory.createNounPhrase("the", "patient"))
        # first VP
        vp1 = self.phraseFactory.createVerbPhrase(self.lexicon.getWord("have", LexicalCategory.VERB))
        np1 = self.phraseFactory.createNounPhrase("a", \
                self.lexicon.getWord("contrast media reaction", LexicalCategory.NOUN))
        np1.addPreModifier(self.lexicon.getWord("adverse", LexicalCategory.ADJECTIVE))
        vp1.addComplement(np1)
        # second VP
        vp2 = self.phraseFactory.createVerbPhrase(self.lexicon.getWord("go", LexicalCategory.VERB))
        pp = self.phraseFactory.createPrepositionPhrase("into", \
                self.lexicon.getWord("cardiogenic shock", LexicalCategory.NOUN))
        vp2.addComplement(pp)
        # coordinate
        coord = self.phraseFactory.createCoordinatedPhrase(vp1, vp2)
        coord.setFeature(Feature.TENSE, Tense.PAST)
        self.assertEqual("had an adverse contrast media reaction and went into cardiogenic shock", \
                self.realiser.realise(coord).getRealisation())
        # now put self in the sentence
        s.setVerbPhrase(coord)
        s.addFrontModifier("As a result of the procedure")
        self.assertEqual(\
            "As a result of the procedure the patient had an adverse contrast media reaction and went into cardiogenic shock", \
            self.realiser.realise(s).getRealisation())

    # Test setting a conjunction to None
    def testNullConjunction(self):
        p = self.phraseFactory.createClause("I", "be", "happy")
        q = self.phraseFactory.createClause("I", "eat", "fish")
        pq = self.phraseFactory.createCoordinatedPhrase()
        pq.addCoordinate(p)
        pq.addCoordinate(q)
        pq.setFeature(Feature.CONJUNCTION, "")
        # should come out without conjunction
        self.assertEqual("I am happy I eat fish", self.realiser.realise(pq).getRealisation())
        # should come out without conjunction
        pq.setFeature(Feature.CONJUNCTION, None)
        self.assertEqual("I am happy I eat fish", self.realiser.realise(pq).getRealisation())

    # Check that the negation feature on a child of a coordinate phrase remains
    # as set, unless explicitly set otherwise at the parent level.
    def testNegationFeature(self):
        s1 = self.phraseFactory.createClause("he", "have", "asthma")
        s2 = self.phraseFactory.createClause("he", "have", "diabetes")
        s1.setFeature(Feature.NEGATED, True)
        coord = self.phraseFactory.createCoordinatedPhrase(s1, s2)
        realisation = self.realiser.realise(coord).getRealisation()
        self.assertEqual("he does not have asthma and he has diabetes", realisation)


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
