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
from simplenlg.features      import Feature, Tense
from simplenlg.framework     import InflectedWordElement, NLGElement
from simplenlg.framework     import PhraseElement, StringElement, WordElement
from simplenlg.phrasespec    import SPhraseSpec


class PhraseSpecTest(SimpleNLG4Test):
    # Check that empty phrases are not realised as "None"
    def testEmptyPhraseRealisation(self):
        emptyClause = self.phraseFactory.createClause()
        self.assertEqual("", self.realiser.realise(emptyClause).getRealisation())

    # Test SPhraseSpec
    def testSPhraseSpec(self):
        # simple test of methods
        c1 = self.phraseFactory.createClause()
        c1.setVerb("give")
        c1.setSubject("John")
        c1.setObject("an apple")
        c1.setIndirectObject("Mary")
        c1.setFeature(Feature.TENSE, Tense.PAST)
        c1.setFeature(Feature.NEGATED, True)
        # check getXXX methods
        self.assertEqual("give",  self.getBaseForm(c1.getVerb()))
        self.assertEqual("John", self.getBaseForm(c1.getSubject()))
        self.assertEqual("an apple", self.getBaseForm(c1.getObject()))
        self.assertEqual("Mary", self.getBaseForm(c1.getIndirectObject()))
        self.assertEqual("John did not give Mary an apple", \
                self.realiser.realise(c1).getRealisation())
        # test modifier placement
        c2 = self.phraseFactory.createClause()
        c2.setVerb("see")
        c2.setSubject("the man")
        c2.setObject("me")
        c2.addModifier("fortunately")
        c2.addModifier("quickly")
        c2.addModifier("in the park")
        # try setting tense directly as a feature
        c2.setFeature(Feature.TENSE, Tense.PAST)
        self.assertEqual("fortunately the man quickly saw me in the park", \
                self.realiser.realise(c2).getRealisation())

    # get string for head of constituent
    @classmethod
    def getBaseForm(cls, constituent):
        if isinstance(constituent, StringElement):
            return constituent.getRealisation()
        elif isinstance(constituent, WordElement):
            return constituent.getBaseForm()
        elif isinstance(constituent, InflectedWordElement):
            return cls.getBaseForm(constituent.getBaseWord())
        elif isinstance(constituent, PhraseElement):
            return cls.getBaseForm(constituent.getHead())
        else:
            return None

if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
