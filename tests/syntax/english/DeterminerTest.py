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

from SimpleNLG4Test                     import *
from simplenlg.phrasespec.NPPhraseSpec  import *
from simplenlg.phrasespec.SPhraseSpec   import *


# Some determiner tests -- in particular for indefinite articles like "a" or "an".
class DeterminerTest(SimpleNLG4Test):
    # testLowercaseConstant - Test for when there is a lower case constant
    def testLowercaseConstant(self):
        sentence = self.phraseFactory.createClause()
        subject = self.phraseFactory.createNounPhrase("a", "dog")
        sentence.setSubject(subject)
        output = self.realiser.realiseSentence(sentence)
        self.assertEqual("A dog.", output)

    # testLowercaseVowel - Test for "an" as a specifier.
    def testLowercaseVowel(self):
        sentence = self.phraseFactory.createClause()
        subject = self.phraseFactory.createNounPhrase("a", "owl")
        sentence.setSubject(subject)
        output = self.realiser.realiseSentence(sentence)
        self.assertEqual("An owl.", output)

    # testUppercaseConstant - Test for when there is a upper case constant
    def testUppercaseConstant(self):
        sentence = self.phraseFactory.createClause()
        subject = self.phraseFactory.createNounPhrase("a", "Cat")
        sentence.setSubject(subject)
        output = self.realiser.realiseSentence(sentence)
        self.assertEqual("A Cat.", output)

    # testUppercaseVowel - Test for "an" as a specifier for upper subjects.
    def testUppercaseVowel(self):
        sentence = self.phraseFactory.createClause()
        subject = self.phraseFactory.createNounPhrase("a", "Emu")
        sentence.setSubject(subject)
        output = self.realiser.realiseSentence(sentence)
        self.assertEqual("An Emu.", output)

    # testNumericA - Test for "a" specifier with a numeric subject
    def testNumericA(self):
        sentence = self.phraseFactory.createClause()
        subject = self.phraseFactory.createNounPhrase("a", "7")
        sentence.setSubject(subject)
        output = self.realiser.realiseSentence(sentence)
        self.assertEqual("A 7.", output)

    # testNumericAn - Test for "an" specifier with a numeric subject
    def testNumericAn(self):
        sentence = self.phraseFactory.createClause()
        subject = self.phraseFactory.createNounPhrase("a", "11")
        sentence.setSubject(subject)
        output = self.realiser.realiseSentence(sentence)
        self.assertEqual("An 11.", output)

    # testIrregularSubjects - Test irregular subjects that don't conform to the
    # vowel vs. constant divide.
    def testIrregularSubjects(self):
        sentence = self.phraseFactory.createClause()
        subject = self.phraseFactory.createNounPhrase("a", "one")
        sentence.setSubject(subject)
        output = self.realiser.realiseSentence(sentence)
        self.assertEqual("A one.", output)


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
