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

from ...features.DiscourseFunction          import *
from ...features.Feature                    import *
from ...features.InternalFeature            import *
from ...framework.CoordinatedPhraseElement  import *
from ...framework.DocumentElement           import *
from ...framework.InflectedWordElement      import *
from ...framework.LexicalCategory           import *
from ...framework.ListElement               import *
from ...framework.NLGElement                import *
from ...framework.NLGModule                 import *
from ...framework.StringElement             import *
from ...framework.WordElement               import *
from .MorphologyRules                       import *


# This is the processor for handling morphology within the SimpleNLG.
class MorphologyProcessor(NLGModule):
    def __init__(self):
        super().__init__()

    # @Override
    def initialise(self):
        pass # Do nothing

    def realise(self, element):
        if isinstance(element, NLGElement):
            return self._realiseElement(element)
        elif isinstance(element, list):
            return self._realiseList(element)
        else:
            raise ValueError('Invalid element type: ' + str(type(element)))

    # @Override
    def _realiseElement(self, element):
        realisedElement = None
        if isinstance(element, InflectedWordElement):
            realisedElement = self.doMorphology(element)
        elif isinstance(element, StringElement):
            realisedElement = element
        elif isinstance(element, WordElement):
            # AG: now retrieves the default spelling variant, not the baseform
            # String baseForm = ((WordElement) element).getBaseForm();
            defaultSpell = element.getDefaultSpellingVariant()
            if defaultSpell is not None:
                realisedElement = StringElement(defaultSpell)
        elif isinstance(element, DocumentElement):
            children = element.getChildren()
            element.setComponents(self.realise(children))
            realisedElement = element
        elif isinstance(element, ListElement):
            realisedElement = ListElement()
            realisedElement.addComponents(self.realise(element.getChildren()))
        elif isinstance(element, CoordinatedPhraseElement):
            children = element.getChildren()
            element.clearCoordinates()
            if children:
                element.addCoordinate(self.realise(children[0]))
                for i, child in enumerate(children):
                    if 0==i: continue
                    element.addCoordinate(self.realise(child))
                realisedElement = element
        elif element is None:
            realisedElement = element
        return realisedElement

    # This is the main method for performing the morphology.
    def doMorphology(self, element):
        realisedElement = None
        if element.getFeatureAsBoolean(InternalFeature.NON_MORPH):
            realisedElement = StringElement(element.getBaseForm())
            realisedElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, \
                    element.getFeature(InternalFeature.DISCOURSE_FUNCTION))
        else:
            baseWord = element.getFeatureAsElement(InternalFeature.BASE_WORD)
            if baseWord is None and self.lexicon is not None:
                baseWord = self.lexicon.lookupWord(element.getBaseForm())
            category = element.getCategory()
            if isinstance(category, LexicalCategory):
                if category == LexicalCategory.PRONOUN:
                    realisedElement = MorphologyRules.doPronounMorphology(element)
                elif category == LexicalCategory.NOUN:
                    realisedElement = MorphologyRules.doNounMorphology(element, baseWord)
                elif category == LexicalCategory.VERB:
                    realisedElement = MorphologyRules.doVerbMorphology(element, baseWord)
                elif category == LexicalCategory.ADJECTIVE:
                    realisedElement = MorphologyRules.doAdjectiveMorphology(element, baseWord)
                elif category == LexicalCategory.ADVERB:
                    realisedElement = MorphologyRules.doAdverbMorphology(element, baseWord)
                else:
                    realisedElement = StringElement(element.getBaseForm())
                    realisedElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, \
                        element.getFeature(InternalFeature.DISCOURSE_FUNCTION))
        return realisedElement

    # @Override
    def _realiseList(self, elements):
        realisedElements = []
        currentElement = None
        determiner = None
        prevElement = None
        if elements is not None:
            for eachElement in elements:
                currentElement = self._realiseElement(eachElement)
                if currentElement is not None:
                    #pass the discourse function and appositive features -- important for orth processor
                    currentElement.setFeature(Feature.APPOSITIVE, eachElement.getFeature(Feature.APPOSITIVE))
                    function = eachElement.getFeature(InternalFeature.DISCOURSE_FUNCTION)
                    if function is not None:
                        currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, function)
                    if prevElement is not None and isinstance(prevElement, StringElement) and \
                            isinstance(eachElement, InflectedWordElement) and \
                            eachElement.getCategory() == LexicalCategory.NOUN:
                        prevString = prevElement.getRealisation()
                        prevElement.setRealisation(DeterminerAgrHelper.checkEndsWithIndefiniteArticle(\
                                prevString,currentElement.getRealisation()))
                    realisedElements.append(currentElement)
                    if determiner is None and DiscourseFunction.SPECIFIER == \
                            currentElement.getFeature(InternalFeature.DISCOURSE_FUNCTION):
                        determiner = currentElement
                        determiner.setFeature(Feature.NUMBER, eachElement.getFeature(Feature.NUMBER))
                    elif determiner is not None:
                        if isinstance(currentElement, ListElement):
                            # list elements: ensure det matches first element
                            children = currentElement.getChildren()
                            firstChild = None if not children else children[0]
                            if firstChild is not None:
                                #AG: need to check if child is a coordinate
                                if isinstance(firstChild, CoordinatedPhraseElement):
                                    MorphologyRules.doDeterminerMorphology(determiner, \
                                        firstChild.getChildren()[0].getRealisation())
                                else:
                                    MorphologyRules.doDeterminerMorphology(determiner, firstChild.getRealisation())
                        else:
                            # everything else: ensure det matches realisation
                            MorphologyRules.doDeterminerMorphology(determiner, currentElement.getRealisation())
                        determiner = None
                prevElement = eachElement
        return realisedElements
