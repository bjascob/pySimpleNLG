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
from simplenlg.framework.DocumentElement import *
from simplenlg.framework.NLGFactory      import *
from simplenlg.lexicon.Lexicon           import *
from simplenlg.realiser.english.Realiser import *


# TextFormatterTest -- Test's the TextFormatter.
class TextFormatterTest(unittest.TestCase):

    def testEnumeratedList(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory(lexicon)
        realiser = Realiser(lexicon)
        realiser.setFormatter(TextFormatter())
        document = nlgFactory.createDocument("Document")
        paragraph = nlgFactory.createParagraph()

        subListItem1 = nlgFactory.createListItem()
        subListSentence1 = nlgFactory.createSentence("this", "be", "sub-list sentence 1")
        subListItem1.addComponent(subListSentence1)

        subListItem2 = nlgFactory.createListItem()
        subListSentence2 = nlgFactory.createSentence("this", "be", "sub-list sentence 2")
        subListItem2.addComponent(subListSentence2)

        subList = nlgFactory.createEnumeratedList()
        subList.addComponent(subListItem1)
        subList.addComponent(subListItem2)

        item1 = nlgFactory.createListItem()
        sentence1 = nlgFactory.createSentence("this", "be", "the first sentence")
        item1.addComponent(sentence1)

        item2 = nlgFactory.createListItem()
        sentence2 = nlgFactory.createSentence("this", "be", "the second sentence")
        item2.addComponent(sentence2)

        list_1 = nlgFactory.createEnumeratedList()
        list_1.addComponent(subList)
        list_1.addComponent(item1)
        list_1.addComponent(item2)
        paragraph.addComponent(list_1)
        document.addComponent(paragraph)
        expectedOutput = "Document\n" + \
                         "\n" + \
                         "1.1 - This is sub-list sentence 1.\n" + \
                         "1.2 - This is sub-list sentence 2.\n"+ \
                         "2 - This is the first sentence.\n" + \
                         "3 - This is the second sentence.\n" + \
                         "\n\n" # for the end of a paragraph

        realisedOutput = realiser.realise(document).getRealisation()
        self.assertEquals(expectedOutput, realisedOutput)


    def testEnumeratedListWithSeveralLevelsOfNesting(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory(lexicon)
        realiser = Realiser(lexicon)
        realiser.setFormatter(TextFormatter())
        document = nlgFactory.createDocument("Document")
        paragraph = nlgFactory.createParagraph()

        # sub item 1
        subList1Item1 = nlgFactory.createListItem()
        subList1Sentence1 = nlgFactory.createSentence("sub-list item 1")
        subList1Item1.addComponent(subList1Sentence1)

        # sub sub item 1
        subSubList1Item1 = nlgFactory.createListItem()
        subSubList1Sentence1 = nlgFactory.createSentence("sub-sub-list item 1")
        subSubList1Item1.addComponent(subSubList1Sentence1)

        # sub sub item 2
        subSubList1Item2 = nlgFactory.createListItem()
        subSubList1Sentence2 = nlgFactory.createSentence("sub-sub-list item 2")
        subSubList1Item2.addComponent(subSubList1Sentence2)

        # sub sub list
        subSubList1 = nlgFactory.createEnumeratedList()
        subSubList1.addComponent(subSubList1Item1)
        subSubList1.addComponent(subSubList1Item2)

        # sub item 2
        subList1Item2 = nlgFactory.createListItem()
        subList1Sentence2 = nlgFactory.createSentence("sub-list item 3")
        subList1Item2.addComponent(subList1Sentence2)

        # sub list 1
        subList1 = nlgFactory.createEnumeratedList()
        subList1.addComponent(subList1Item1)
        subList1.addComponent(subSubList1)
        subList1.addComponent(subList1Item2)

        # item 2
        item2 = nlgFactory.createListItem()
        sentence2 = nlgFactory.createSentence("item 2")
        item2.addComponent(sentence2)

        # item 3
        item3 = nlgFactory.createListItem()
        sentence3 = nlgFactory.createSentence("item 3")
        item3.addComponent(sentence3)

        # list
        list_1 = nlgFactory.createEnumeratedList()
        list_1.addComponent(subList1)
        list_1.addComponent(item2)
        list_1.addComponent(item3)

        paragraph.addComponent(list_1)

        document.addComponent(paragraph)

        expectedOutput = "Document\n" + \
                         "\n" + \
                         "1.1 - Sub-list item 1.\n" + \
                         "1.2.1 - Sub-sub-list item 1.\n" + \
                         "1.2.2 - Sub-sub-list item 2.\n" + \
                         "1.3 - Sub-list item 3.\n"+ \
                         "2 - Item 2.\n" + \
                         "3 - Item 3.\n" + \
                         "\n\n"

        realisedOutput = realiser.realise(document).getRealisation()
        self.assertEquals(expectedOutput, realisedOutput)


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
