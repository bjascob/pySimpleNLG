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
from simplenlg.features.Feature          import *
from simplenlg.phrasespec.SPhraseSpec    import *


# Tests for elision of phrases and words
class ElisionTest(SimpleNLG4Test):
    # Test for elision of specific words rather than phrases
    def testWordElision1(self):
        s1 = self.phraseFactory.createClause()
        s1.setSubject(self.np4) #the rock
        self.kiss.setComplement(self.np5)#kiss the curtain
        s1.setVerbPhrase(self.kiss)
        self.np5.setFeature(Feature.ELIDED, True)
        self.assertEqual("the rock kisses", self.realiser.realise(s1).getRealisation())

    # Test for elision of specific words rather than phrases
    def testWordElision2(self):
        s1 = self.phraseFactory.createClause()
        s1.setSubject(self.np4) #the rock
        self.kiss.setComplement(self.np5)#kiss the curtain
        s1.setVerbPhrase(self.kiss)
        self.kiss.getHead().setFeature(Feature.ELIDED, True)
        self.assertEqual("the rock kisses the curtain", self.realiser.realise(s1).getRealisation())


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
