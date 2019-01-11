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

from ...features.Feature                    import *
from ...framework.CoordinatedPhraseElement  import *
from ...framework.DocumentElement           import *
from ...framework.InflectedWordElement      import *
from ...framework.LexicalCategory           import *
from ...framework.ListElement               import *
from ...framework.NLGElement                import *
from ...framework.NLGModule                 import *
from ...framework.PhraseCategory            import *
from ...framework.PhraseElement             import *
from ...framework.WordElement               import *
from .ClauseHelper                          import *
from .CoordinatedPhraseHelper               import *
from .NounPhraseHelper                      import *
from .PhraseHelper                          import *
from .VerbPhraseHelper                      import *

# This is the processor for handling syntax within the SimpleNLG. The processor
# translates phrases into lists of words.
class SyntaxProcessor(NLGModule):
    def __init__(self):
        super().__init__()

    # @Override
    def initialise(self):
        pass

    # @Override
    def realise(self, element):
        if element is None or element.getFeatureAsBoolean(Feature.ELIDED):
            return None
        elif isinstance(element, NLGElement):
            return self._realiseElement(element)
        elif isinstance(element, list):
            return self._realiseElementList(element)
        else:
            raise ValueError('Invalid element type: ' + str(type(element)))

    def _realiseElement(self, element):
        realisedElement = None
        if element is not None and not element.getFeatureAsBoolean(Feature.ELIDED):
            if isinstance(element, DocumentElement):
                children = element.getChildren()
                element.setComponents(self._realiseElementList(children))
                realisedElement = element
            elif isinstance(element, PhraseElement):
                realisedElement = self.realisePhraseElement(element)
            elif isinstance(element, ListElement):
                realisedElement = ListElement()
                realisedElement.addComponents(self._realiseElementList(element.getChildren()))
            elif isinstance(element, InflectedWordElement):
                baseForm = element.getBaseForm()
                category = element.getCategory()
                if self.lexicon is not None and baseForm is not None:
                    word = element.getBaseWord()
                    if word is None:
                        if isinstance(category, LexicalCategory):
                            word = self.lexicon.lookupWord(baseForm, category)
                        else:
                            word = self.lexicon.lookupWord(baseForm)
                    if word is not None:
                        element.setBaseWord(word)
                realisedElement = element
            elif isinstance(element, WordElement):
                # AG: need to check if it's a word element, in which case it
                # needs to be marked for inflection
                infl = InflectedWordElement(element)
                # # the inflected word inherits all features from the base word
                for feature in element.getAllFeatureNames():
                    infl.setFeature(feature, element.getFeature(feature))
                realisedElement = self._realiseElement(infl)
            elif isinstance(element, CoordinatedPhraseElement):
                realisedElement = CoordinatedPhraseHelper.realise(self, element)
            else:
                realisedElement = element
        # Remove the spurious ListElements that have only one element.
        if isinstance(realisedElement, ListElement):
            if len(realisedElement) == 1:
                realisedElement = realisedElement.getFirst()
        return realisedElement

    # @Override
    def _realiseElementList(self, elements):
        realisedList = []
        childRealisation = None
        if elements is not None:
            for eachElement in elements:
                if eachElement is not None:
                    childRealisation = self._realiseElement(eachElement)
                    if childRealisation is not None:
                        if isinstance(childRealisation, ListElement):
                            realisedList.extend(childRealisation.getChildren())
                        else:
                            realisedList.append(childRealisation)
        return realisedList

    # Realises a phrase element.
    def realisePhraseElement(self, phrase):
        realisedElement = None
        if phrase is not None:
            category = phrase.getCategory()
            if isinstance(category, PhraseCategory):
                if category == PhraseCategory.CLAUSE:
                    realisedElement = ClauseHelper.realise(self, phrase)
                elif category == PhraseCategory.NOUN_PHRASE:
                    realisedElement = NounPhraseHelper.realise(self, phrase)
                elif category == PhraseCategory.VERB_PHRASE:
                    realisedElement = VerbPhraseHelper.realise(self, phrase)
                elif category in [PhraseCategory.PREPOSITIONAL_PHRASE, PhraseCategory.ADJECTIVE_PHRASE, \
                        PhraseCategory.ADVERB_PHRASE]:
                    realisedElement = PhraseHelper.realise(self, phrase)
                else:
                    realisedElement = phrase
        return realisedElement
