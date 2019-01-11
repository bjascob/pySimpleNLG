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
sys.path.append('../../..')
from simplenlg.framework.DocumentElement   import *
from simplenlg.framework.NLGFactory        import *
from simplenlg.lexicon.Lexicon             import *
from simplenlg.realiser.english.Realiser   import *


# This tests that two sentences are realised as a list.
class EnumeratedListTest(unittest.TestCase):

    @unittest.skip("HTMLFormatter not implemented - revise to use TextFormatter")
    def testBulletList(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory(lexicon)
        realiser = Realiser(lexicon)
        realiser.setFormatter(HTMLFormatter())
        document = nlgFactory.createDocument("Document")
        paragraph = nlgFactory.createParagraph()
        list_1 = nlgFactory.createList()
        item1 = nlgFactory.createListItem()
        item2 = nlgFactory.createListItem()
        # NB: a list item employs orthographical operations only until sentence level;
        # nest clauses within a sentence to generate more than 1 clause per list item.
        sentence1 = nlgFactory.createSentence("this", "be", "the first sentence")
        sentence2 = nlgFactory.createSentence("this", "be", "the second sentence")
        item1.addComponent(sentence1)
        item2.addComponent(sentence2)
        list_1.addComponent(item1)
        list_1.addComponent(item2)
        paragraph.addComponent(list_1)
        document.addComponent(paragraph)
        expectedOutput = "<h1>Document</h1>" + "<p>" + "<ul>" + "This is the first sentence." \
                       + "This is the second sentence." + "</ul>" + "</p>";
        realisedOutput = realiser.realise(document).getRealisation()
        self.assertEqual(expectedOutput, realisedOutput);

    @unittest.skip("HTMLFormatter not implemented - revise to use TextFormatter")
    def testEnumeratedList(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory(lexicon)
        realiser = Realiser(lexicon)
        realiser.setFormatter(HTMLFormatter())
        document = nlgFactory.createDocument("Document")
        paragraph = nlgFactory.createParagraph()
        list_1 = nlgFactory.createEnumeratedList()
        item1 = nlgFactory.createListItem()
        item2 = nlgFactory.createListItem()
        # NB: a list item employs orthographical operations only until sentence level;
        # nest clauses within a sentence to generate more than 1 clause per list item.
        sentence1 = nlgFactory.createSentence("this", "be", "the first sentence")
        sentence2 = nlgFactory.createSentence("this", "be", "the second sentence")
        item1.addComponent(sentence1)
        item2.addComponent(sentence2)
        list_1.addComponent(item1)
        list_1.addComponent(item2)
        paragraph.addComponent(list_1)
        document.addComponent(paragraph)
        expectedOutput = "<h1>Document</h1>" + "<p>" + "<ol>" + "This is the first sentence." \
                       + "This is the second sentence." + "</ol>" + "</p>"
        realisedOutput = realiser.realise(document).getRealisation()
        self.assertEqual(expectedOutput, realisedOutput)

if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
