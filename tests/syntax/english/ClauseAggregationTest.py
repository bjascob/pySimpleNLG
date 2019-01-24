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

from SimpleNLG4Test                                          import *
from simplenlg.aggregation.BackwardConjunctionReductionRule  import *
from simplenlg.aggregation.Aggregator                        import *
from simplenlg.aggregation.ClauseCoordinationRule            import *
from simplenlg.aggregation.ForwardConjunctionReductionRule   import *
from simplenlg.features.Feature                              import *
from simplenlg.framework.NLGElement                          import *
from simplenlg.phrasespec.SPhraseSpec                        import *


# Some tests for aggregation.
class ClauseAggregationTest(SimpleNLG4Test):

    # Instantiates a new clause aggregation test.
    def __init__(self, name):
        super().__init__(name)
        self.aggregator = Aggregator()
        self.aggregator.initialise()
        self.coord = ClauseCoordinationRule()
        self.fcr = ForwardConjunctionReductionRule()
        self.bcr = BackwardConjunctionReductionRule()

    # @Override  @Before
    def setUp(self):
        super().setUp()
        # the woman kissed the man behind the curtain
        self.s1 = self.phraseFactory.createClause()
        self.s1.setSubject(self.woman)
        self.s1.setVerbPhrase(self.phraseFactory.createVerbPhrase("kiss"))
        self.s1.setObject(self.man)
        self.s1.addPostModifier(self.phraseFactory.createPrepositionPhrase("behind", self.phraseFactory \
                .createNounPhrase("the", "curtain")))

        # the woman kicked the dog on the rock
        self.s2 = self.phraseFactory.createClause()
        self.s2.setSubject(self.phraseFactory.createNounPhrase("the", "woman"))
        self.s2.setVerbPhrase(self.phraseFactory.createVerbPhrase("kick"))
        self.s2.setObject(self.phraseFactory.createNounPhrase("the", "dog"))
        self.s2.addPostModifier(self.onTheRock)

        # the woman kicked the dog behind the curtain
        self.s3 = self.phraseFactory.createClause()
        self.s3.setSubject(self.phraseFactory.createNounPhrase("the", "woman"))
        self.s3.setVerbPhrase(self.phraseFactory.createVerbPhrase("kick"))
        self.s3.setObject(self.phraseFactory.createNounPhrase("the", "dog"))
        self.s3.addPostModifier(self.phraseFactory.createPrepositionPhrase("behind", self.phraseFactory \
                .createNounPhrase("the", "curtain")))

        # the man kicked the dog behind the curtain
        self.s4 = self.phraseFactory.createClause()
        self.s4.setSubject(self.man) #$NON-NLS-1$
        self.s4.setVerbPhrase(self.phraseFactory.createVerbPhrase("kick"))
        self.s4.setObject(self.phraseFactory.createNounPhrase("the", "dog"))
        self.s4.addPostModifier(self.behindTheCurtain)

        # the girl kicked the dog behind the curtain
        self.s5 = self.phraseFactory.createClause()
        self.s5.setSubject(self.phraseFactory.createNounPhrase("the", "girl"))
        self.s5.setVerbPhrase(self.phraseFactory.createVerbPhrase("kick"))
        self.s5.setObject(self.phraseFactory.createNounPhrase("the", "dog"))
        self.s5.addPostModifier(self.behindTheCurtain)

        # the woman kissed the dog behind the curtain
        self.s6 = self.phraseFactory.createClause()
        self.s6.setSubject(self.phraseFactory.createNounPhrase("the", "woman"))
        self.s6.setVerbPhrase(self.phraseFactory.createVerbPhrase("kiss"))
        self.s6.setObject(self.phraseFactory.createNounPhrase("the", "dog"))
        self.s6.addPostModifier(self.phraseFactory.createPrepositionPhrase("behind", self.phraseFactory \
                .createNounPhrase("the", "curtain")))

    # @After
    def tearDown(self):
        super().tearDown()
        self.s1 = None
        self.s2 = None
        self.s3 = None
        self.s4 = None
        self.s5 = None
        self.s6 = None
        self.aggregator = None
        self.coord = None
        self.fcr = None
        self.bcr = None

    # Test clause coordination with two sentences with same subject but
    # different postmodifiers: fails
    def testCoordinationSameSubjectFail(self):
        elements = [self.s1, self.s2]
        result = self.coord.apply(elements)
        self.assertEqual(2, len(result))

    # Test clause coordination with two sentences one of which is passive fails
    def testCoordinationPassiveFail(self):
        self.s1.setFeature(Feature.PASSIVE, true)
        elements = [self.s1, self.s2]
        result = self.coord.apply(elements)
        self.assertEqual(2, len(result))

    # Test clause coordination with 2 sentences with same VP: succeeds
    def testCoordinationSameVP(self):
        elements = [self.s3, self.s4]
        result = self.coord.apply(elements)
        self.assertTrue(len(result) == 1) # should only be one sentence
        aggregated = result[0]
        self.assertEqual("the woman and the man kick the dog behind the curtain", \
                self.realiser.realise(aggregated).getRealisation())

    # Coordination of sentences with front modifiers: should preserve the mods
    def testCoordinationWithModifiers(self):
        # now add a couple of front modifiers
        self.s3.addFrontModifier(self.phraseFactory.createAdverbPhrase("however"))
        self.s4.addFrontModifier(self.phraseFactory.createAdverbPhrase("however"))
        elements = [self.s3, self.s4]
        result = self.coord.apply(elements)
        self.assertTrue(len(result) == 1) # should only be one sentence
        aggregated = result[0]
        self.assertEqual("however the woman and the man kick the dog behind the curtain", \
                self.realiser.realise(aggregated).getRealisation())

    # Test coordination of 3 sentences with the same VP
    def testCoordinationSameVP2(self):
        elements = [self.s3, self.s4, self.s5]
        result = self.coord.apply(elements)
        self.assertTrue(len(result) == 1) # should only be one sentence
        aggregated = result[0]
        self.assertEqual("the woman and the man and the girl kick the dog behind the curtain", \
                self.realiser.realise(aggregated).getRealisation())

    # Forward conjunction reduction test
    def testForwardConjReduction(self):
        aggregated = self.fcr.apply(self.s2, self.s3)
        self.assertEqual("the woman kicks the dog on the rock and kicks the dog behind the curtain", \
                self.realiser.realise(aggregated).getRealisation())

    # Backward conjunction reduction test
    def testBackwardConjunctionReduction(self):
        aggregated = self.bcr.apply(self.s3, self.s6)
        self.assertEqual("the woman kicks and the woman kisses the dog behind the curtain", \
                self.realiser.realise(aggregated).getRealisation())


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
