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

from SimpleNLG4Test                      import *
from simplenlg.framework.DocumentElement import *
from simplenlg.phrasespec.NPPhraseSpec   import *
from simplenlg.phrasespec.SPhraseSpec    import *


# Tests for the DocumentElement class.
class DocumentElementTest(SimpleNLG4Test):

    def setUp(self):
        super().setUp()
        self.p1 = self.phraseFactory.createClause("you", "be", "happy")
        self.p2 = self.phraseFactory.createClause("I", "be", "sad")
        self.p3 = self.phraseFactory.createClause("they", "be", "nervous")

    def tearDown(self):
        super().tearDown()
        self.p1 = None
        self.p2 = None
        self.p3 = None

    # Basic tests.
    def testBasics(self):
        s1 = self.phraseFactory.createSentence(self.p1)
        s2 = self.phraseFactory.createSentence(self.p2)
        s3 = self.phraseFactory.createSentence(self.p3)
        par1 = self.phraseFactory.createParagraph([s1, s2, s3])
        self.assertEqual("You are happy. I am sad. They are nervous.\n\n", \
                self.realiser.realise(par1).getRealisation())

    # Ensure that no extra whitespace is inserted into a realisation if a
    # constituent is empty. (This is to check for a bug fix for addition of
    # spurious whitespace).
    def testExtraWhitespace(self):
        np1 = self.phraseFactory.createNounPhrase("a", "vessel")
        # empty coordinate as premod
        np1.setPreModifier(self.phraseFactory.createCoordinatedPhrase())
        self.assertEqual("a vessel", self.realiser.realise(np1).getRealisation())
        # empty adjP as premod
        np1.setPreModifier(self.phraseFactory.createAdjectivePhrase())
        self.assertEqual("a vessel", self.realiser.realise(np1).getRealisation())
        # empty string
        np1.setPreModifier("")
        self.assertEqual("a vessel", self.realiser.realise(np1).getRealisation())

    # test whether sents can be embedded in a section without intervening paras
    def testEmbedding(self):
        sent = self.phraseFactory.createSentence("This is a test")
        sent2 = self.phraseFactory.createSentence(self.phraseFactory.createClause("John", "be", "missing"))
        section = self.phraseFactory.createSection("SECTION TITLE")
        section.addComponent(sent)
        section.addComponent(sent2)
        self.assertEqual("SECTION TITLE\nThis is a test.\n\nJohn is missing.\n\n", \
                self.realiser.realise(section).getRealisation())

    def testSections(self):
        # doc which contains a section, and two paras
        doc = self.phraseFactory.createDocument("Test Document")
        section = self.phraseFactory.createSection("Test Section")
        doc.addComponent(section)
        para1 = self.phraseFactory.createParagraph()
        sent1 = self.phraseFactory.createSentence("This is the first test paragraph")
        para1.addComponent(sent1)
        section.addComponent(para1)
        para2 = self.phraseFactory.createParagraph()
        sent2 = self.phraseFactory.createSentence("This is the second test paragraph")
        para2.addComponent(sent2)
        section.addComponent(para2)
        self.assertEqual(\
            "Test Document\n\nTest Section\nThis is the first test paragraph.\n\nThis is the second test paragraph.\n\n", \
            self.realiser.realise(doc).getRealisation())

    def testListItems(self):
        list = self.phraseFactory.createList()
        list.addComponent(self.phraseFactory.createListItem(self.p1))
        list.addComponent(self.phraseFactory.createListItem(self.p2))
        list.addComponent(self.phraseFactory.createListItem( \
            self.phraseFactory.createCoordinatedPhrase(self.p1, self.p2)))
        realisation = self.realiser.realise(list).getRealisation()
        self.assertEqual("* you are happy\n* I am sad\n* you are happy and I am sad\n", realisation)

if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
