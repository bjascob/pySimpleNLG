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

from ..features.DiscourseFunction   import *
from ..features.InternalFeature     import *
from ..framework.LexicalCategory    import *
from ..framework.NLGElement         import *
from ..framework.PhraseCategory     import *
from ..framework.PhraseElement      import *


# This class defines a prepositional phrase.  
class PPPhraseSpec(PhraseElement):
    def __init__(self, phraseFactory):
        super().__init__(PhraseCategory.PREPOSITIONAL_PHRASE)
        self.setFactory(phraseFactory)

    # sets the preposition (head) of a prepositional phrase
    def setPreposition(self, preposition):
        if isinstance(preposition, NLGElement):
            self.setHead(preposition)
        else:
            # create noun as word
            prepositionalElement = self.getFactory().createWord(preposition, LexicalCategory.PREPOSITION)
            # set head of NP to nounElement
            self.setHead(prepositionalElement)

    # @return preposition (head) of prepositional phrase
    def getPreposition(self):
        return self.getHead()

    # Sets the  object of a PP
    def setObject(self, obj):
        objectPhrase = self.getFactory().createNounPhrase(obj)
        objectPhrase.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.OBJECT)
        self.addComplement(objectPhrase)

    # @return object of PP (assume only one)
    def getObject(self):
        complements = self.getFeatureAsElementList(InternalFeature.COMPLEMENTS)
        for complement in complements:
            if complement.getFeature(InternalFeature.DISCOURSE_FUNCTION) == DiscourseFunction.OBJECT:
                return complement
        return None
