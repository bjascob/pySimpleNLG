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

from .NLGElement                import *
from ..features.InternalFeature import *
from ..features.LexicalFeature  import *
from .WordElement               import *


# This class defines the NLGElement that is used to represent an
# word that requires inflection by the morphology.
class InflectedWordElement(NLGElement):
    def __init__(self, word, category=None):
        super().__init__()
        if isinstance(word, WordElement):
            self.setFeature(InternalFeature.BASE_WORD, word)
            # AG: changed to use the default spelling variant
            # setFeature(LexicalFeature.BASE_FORM, word.getBaseForm());
            defaultSpelling = word.getDefaultSpellingVariant()
            self.setFeature(LexicalFeature.BASE_FORM, defaultSpelling)
            self.setCategory(word.getCategory())
        elif isinstance(word, str) and isinstance(category, LexicalCategory):
            self.setFeature(LexicalFeature.BASE_FORM, word)
            self.setCategory(category)
        else:
            raise ValueError('Invalid param types: ' + str(type(word)) + ', ' + str(type(category)))

    # This method returns null as the inflected word has no child components.
    # @Override
    def getChildren(self):
        return None

    # @Override
    def __str__(self):
        return "InflectedWordElement[" + self.getBaseForm() + ':' + str(self.getCategory()) + ']'

    # @Override
    def printTree(self, indent=None):
        pstr = "InflectedWordElement: base=" + self.getBaseForm() + ", category=" + \
               str(self.getCategory()) + ", " + super().__str__() + '\n'
        return pstr

    # Retrieves the base form for this element. The base form is the originally
    # supplied word.
    def getBaseForm(self):
        return self.getFeatureAsString(LexicalFeature.BASE_FORM)

    # Sets the base word for this element.
    def setBaseWord(self, word):
        self.setFeature(InternalFeature.BASE_WORD, word)

    # Retrieves the base word for this element.
    def getBaseWord(self):
        baseWord = self.getFeatureAsElement(InternalFeature.BASE_WORD)
        if isinstance(baseWord, WordElement):
            return baseWord
        return None
