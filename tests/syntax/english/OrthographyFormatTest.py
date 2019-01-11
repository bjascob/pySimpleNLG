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

from SimpleNLG4Test              import *
from simplenlg.format.english    import TextFormatter
from simplenlg.framework         import DocumentElement, NLGElement
from simplenlg.phrasespec        import NPPhraseSpec, PPPhraseSpec, SPhraseSpec
from simplenlg.features          import Feature


class OrthographyFormatTest(SimpleNLG4Test):
    def __init__(self, name):
        super().__init__(name)
        self.list1Realisation = "* in the room" + "\n* " + "behind the curtain" + "\n"
        self.list2Realisation = "* on the rock" + "\n* " + self.list1Realisation + "\n"


    def setUp(self):
        super().setUp()
        # need to set formatter for realiser (set to None in the test superclass)
        self.realiser.setFormatter(TextFormatter())
        # a couple phrases as list items
        self.listItem1 = self.phraseFactory.createListItem(self.inTheRoom)
        self.listItem2 = self.phraseFactory.createListItem(self.behindTheCurtain)
        self.listItem3 = self.phraseFactory.createListItem(self.onTheRock)
        # a simple depth-1 list of phrases
        self.list1 = self.phraseFactory.createList([self.listItem1, self.listItem2])
        # a list consisting of one phrase (depth-1) + a list )(depth-2)
        self.list2 = self.phraseFactory.createList([self.listItem3, \
                self.phraseFactory.createListItem(self.list1)])

    def tearDown(self):
        super().tearDown()
        self.list1 = None
        self.list2 = None
        self.listItem1 = None
        self.listItem2 = None
        self.listItem3 = None
        self.list1Realisation = None
        self.list2Realisation = None

    # Test the realisation of a simple list
    def testSimpleListOrthography(self):
        realised = self.realiser.realise(self.list1)
        self.assertEqual(self.list1Realisation, realised.getRealisation())

    # Test the realisation of a list with an embedded list
    def testEmbeddedListOrthography(self):
        realised = self.realiser.realise(self.list2)
        self.assertEqual(self.list2Realisation, realised.getRealisation())

    # Test the realisation of appositive pre-modifiers with commas around them.
    def testAppositivePreModifiers(self):
        subject = self.phraseFactory.createNounPhrase("I")
        object = self.phraseFactory.createNounPhrase("a bag")
        _s1 = self.phraseFactory.createClause(subject,  "carry", object)
        # add a PP complement
        pp = self.phraseFactory.createPrepositionPhrase("on", \
                self.phraseFactory.createNounPhrase("most", "Tuesdays"))
        _s1.addPreModifier(pp)
        #without appositive feature on pp
        self.assertEqual("I on most Tuesdays carry a bag", \
                self.realiser.realise(_s1).getRealisation())
        #with appositive feature
        pp.setFeature(Feature.APPOSITIVE, True)
        self.assertEqual("I, on most Tuesdays, carry a bag", \
                self.realiser.realise(_s1).getRealisation())

    # Test the realisation of appositive pre-modifiers with commas around them.
    def testCommaSeparatedFrontModifiers(self):
        subject = self.phraseFactory.createNounPhrase("I")
        object = self.phraseFactory.createNounPhrase("a bag")
        _s1 = self.phraseFactory.createClause(subject, "carry", object)
        # add a PP complement
        pp1 = self.phraseFactory.createPrepositionPhrase("on", \
                self.phraseFactory.createNounPhrase("most", "Tuesdays"))
        _s1.addFrontModifier(pp1)
        pp2 = self.phraseFactory.createPrepositionPhrase("since", \
                self.phraseFactory.createNounPhrase("1991"))
        _s1.addFrontModifier(pp2)
        pp1.setFeature(Feature.APPOSITIVE, True)
        pp2.setFeature(Feature.APPOSITIVE, True)
        #without setCommaSepCuephrase
        self.assertEqual("on most Tuesdays since 1991 I carry a bag", \
                self.realiser.realise(_s1).getRealisation())
        #with setCommaSepCuephrase
        self.realiser.setCommaSepCuephrase(True)
        self.assertEqual("on most Tuesdays, since 1991, I carry a bag", \
                self.realiser.realise(_s1).getRealisation())

    # Ensure we don't end up with doubled commas.
    def testNoDoubledCommas(self):
        subject = self.phraseFactory.createNounPhrase("I")
        object = self.phraseFactory.createNounPhrase("a bag")
        _s1 = self.phraseFactory.createClause(subject, "carry", object)
        pp1 = self.phraseFactory.createPrepositionPhrase("on", \
                self.phraseFactory.createNounPhrase("most", "Tuesdays"))
        _s1.addFrontModifier(pp1)
        pp2 = self.phraseFactory.createPrepositionPhrase("since", \
                self.phraseFactory.createNounPhrase("1991"))
        pp3 = self.phraseFactory.createPrepositionPhrase("except", \
                self.phraseFactory.createNounPhrase("yesterday"))
        pp2.setFeature(Feature.APPOSITIVE, True)
        pp3.setFeature(Feature.APPOSITIVE, True)
        pp1.addPostModifier(pp2)
        pp1.addPostModifier(pp3)
        self.realiser.setCommaSepCuephrase(True)
        self.assertEqual("on most Tuesdays, since 1991, except yesterday, I carry a bag", \
            self.realiser.realise(_s1).getRealisation())

if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
