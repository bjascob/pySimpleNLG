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
from simplenlg.framework.CoordinatedPhraseElement    import *
from simplenlg.framework.LexicalCategory             import *
from simplenlg.framework.PhraseElement               import *
from simplenlg.framework.StringElement               import *


# This class incorporates a few tests for adjectival phrases. Also tests for
# adverbial phrase specs, which are very similar
class AdjectivePhraseTest(SimpleNLG4Test):
    def AdjectivePhraseTest(self, name):
        super().__init__(name)

    # @Override  @After
    def tearDown(self):
        super().tearDown()

    # Test premodification & coordination of Adjective Phrases
    def testAdj(self):
        # form the adjphrase "incredibly salacious"
        self.salacious.addPreModifier(self.phraseFactory.createAdverbPhrase("incredibly"))
        self.assertEqual("incredibly salacious", self.realiser.realise(self.salacious).getRealisation())

        # form the adjphrase "incredibly beautiful"
        self.beautiful.addPreModifier("amazingly")
        self.assertEqual("amazingly beautiful", self.realiser.realise(self.beautiful).getRealisation())

        # coordinate the two aps
        coordap = CoordinatedPhraseElement(self.salacious, self.beautiful)
        self.assertEqual("incredibly salacious and amazingly beautiful", \
                self.realiser.realise(coordap).getRealisation())

        # changing the inner conjunction
        coordap.setFeature(Feature.CONJUNCTION, "or")
        self.assertEqual("incredibly salacious or amazingly beautiful", \
                self.realiser.realise(coordap).getRealisation())

        # coordinate self with a new AdjPhraseSpec
        coord2 = CoordinatedPhraseElement(coordap, self.stunning)
        self.assertEqual("incredibly salacious or amazingly beautiful and stunning", \
                self.realiser.realise(coord2).getRealisation())

        # add a premodifier the coordinate phrase, yielding
        # "seriously and undeniably incredibly salacious or amazingly beautiful
        # and stunning"
        preMod = CoordinatedPhraseElement(StringElement("seriously"), StringElement("undeniably"))
        coord2.addPreModifier(preMod)
        self.assertEqual("seriously and undeniably incredibly salacious or amazingly beautiful and stunning", \
                self.realiser.realise(coord2).getRealisation())

        # adding a coordinate rather than coordinating should give a different
        # result
        coordap.addCoordinate(self.stunning)
        self.assertEqual("incredibly salacious, amazingly beautiful or stunning", \
                self.realiser.realise(coordap).getRealisation())

    # Simple test of adverbials
    def testAdv(self):
        sent = self.phraseFactory.createClause("John", "eat")
        adv = self.phraseFactory.createAdverbPhrase("quickly")
        sent.addPreModifier(adv)
        self.assertEqual("John quickly eats", self.realiser.realise(sent).getRealisation())
        adv.addPreModifier("very")
        self.assertEqual("John very quickly eats", self.realiser.realise(sent).getRealisation())

    # Test participles as adjectives
    def testParticipleAdj(self):
        ap = self.phraseFactory.createAdjectivePhrase(self.lexicon.getWord("associated", \
                        LexicalCategory.ADJECTIVE))
        self.assertEqual("associated", self.realiser.realise(ap).getRealisation())

    # Test for multiple adjective modifiers with comma-separation. Example courtesy of William Bradshaw (Data2Text Ltd).
    def testMultipleModifiers(self):
        np = self.phraseFactory.createNounPhrase(self.lexicon.getWord("message", \
                        LexicalCategory.NOUN))
        np.addPreModifier(self.lexicon.getWord("active", LexicalCategory.ADJECTIVE))
        np.addPreModifier(self.lexicon.getWord("temperature", LexicalCategory.ADJECTIVE))
        self.assertEqual("active, temperature message", self.realiser.realise(np).getRealisation())
        #now we set the realiser not to separate using commas
        self.realiser.setCommaSepPremodifiers(False)
        self.assertEqual("active temperature message", self.realiser.realise(np).getRealisation())


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
