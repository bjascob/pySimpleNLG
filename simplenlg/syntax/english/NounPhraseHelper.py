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

from copy import deepcopy
from ...features.DiscourseFunction      import *
from ...features.Feature                import *
from ...features.Gender                 import *
from ...features.InternalFeature        import *
from ...features.LexicalFeature         import *
from ...features.Person                 import *
from ...framework.InflectedWordElement  import *
from ...framework.LexicalCategory       import *
from ...framework.ListElement           import *
from ...framework.NLGElement            import *
from ...framework.PhraseCategory        import *
from ...framework.PhraseElement         import *
from ...framework.WordElement           import *
from .PhraseHelper                      import *


# This class contains static methods to help the syntax processor realise noun
# phrases.
class NounPhraseHelper(object):
    QUALITATIVE_POSITION = 1
    COLOUR_POSITION      = 2
    CLASSIFYING_POSITION = 3
    NOUN_POSITION        = 4

    # The main method for realising noun phrases.
    @classmethod
    def realise(cls, parent, phrase):
        realisedElement = ListElement()
        if phrase is not None and not phrase.getFeatureAsBoolean(Feature.ELIDED):
            realisedElement = ListElement()
            if phrase.getFeatureAsBoolean(Feature.PRONOMINAL):
                realisedElement.addComponent(cls.createPronoun(parent, phrase))
            else:
                cls.realiseSpecifier(phrase, parent, realisedElement)
                cls.realisePreModifiers(phrase, parent, realisedElement)
                cls.realiseHeadNoun(phrase, parent, realisedElement)
                PhraseHelper.realiseList(parent, realisedElement, \
                        phrase.getFeatureAsElementList(InternalFeature.COMPLEMENTS), \
                        DiscourseFunction.COMPLEMENT)
                PhraseHelper.realiseList(parent, realisedElement, phrase.getPostModifiers(), \
                        DiscourseFunction.POST_MODIFIER)
        return realisedElement

    # Realises the head noun of the noun phrase.
    @classmethod
    def realiseHeadNoun(cls, phrase, parent, realisedElement):
        headElement = phrase.getHead()
        if headElement is not None:
            headElement.setFeature(Feature.ELIDED, phrase.getFeature(Feature.ELIDED))
            headElement.setFeature(LexicalFeature.GENDER, phrase.getFeature(LexicalFeature.GENDER))
            headElement.setFeature(InternalFeature.ACRONYM, phrase.getFeature(InternalFeature.ACRONYM))
            headElement.setFeature(Feature.NUMBER, phrase.getFeature(Feature.NUMBER))
            headElement.setFeature(Feature.PERSON, phrase.getFeature(Feature.PERSON))
            headElement.setFeature(Feature.POSSESSIVE, phrase.getFeature(Feature.POSSESSIVE))
            headElement.setFeature(Feature.PASSIVE, phrase.getFeature(Feature.PASSIVE))
            currentElement = parent.realise(headElement)
            currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.SUBJECT)
            realisedElement.addComponent(currentElement)

    # Realises the pre-modifiers of the noun phrase. Before being realised,
    # pre-modifiers undergo some basic sorting based on adjective ordering.
    @classmethod
    def realisePreModifiers(cls, phrase,  parent, realisedElement):
        preModifiers = phrase.getPreModifiers()
        if phrase.getFeatureAsBoolean(Feature.ADJECTIVE_ORDERING):
            preModifiers = cls.sortNPPreModifiers(preModifiers)
        PhraseHelper.realiseList(parent, realisedElement, preModifiers, DiscourseFunction.PRE_MODIFIER)

    # Realises the specifier of the noun phrase.
    @classmethod
    def realiseSpecifier(cls, phrase, parent, realisedElement):
        specifierElement = phrase.getFeatureAsElement(InternalFeature.SPECIFIER)
        if specifierElement is not None and not phrase.getFeatureAsBoolean(InternalFeature.RAISED) and not \
                phrase.getFeatureAsBoolean(Feature.ELIDED):
            if not specifierElement.isA(LexicalCategory.PRONOUN) and \
                    specifierElement.getCategory() != PhraseCategory.NOUN_PHRASE:
                specifierElement.setFeature(Feature.NUMBER, phrase.getFeature(Feature.NUMBER))
            currentElement = parent.realise(specifierElement)
            if currentElement is not None:
                currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.SPECIFIER)
                realisedElement.addComponent(currentElement)

    # Sort the list of premodifiers for this noun phrase using adjective
    # ordering (ie, "big" comes before "red")
    @classmethod
    def sortNPPreModifiers(cls, originalModifiers):
        if originalModifiers is None or len(originalModifiers)<=1:
            orderedModifiers = originalModifiers
        else:
            orderedModifiers = deepcopy(originalModifiers)
            changesMade = True
            while changesMade:
                changesMade = False
                for i in range(len(orderedModifiers)-1):
                    if cls.getMinPos(orderedModifiers[i]) > cls.getMaxPos(orderedModifiers[i+1]):
                        temp = orderedModifiers[i]
                        orderedModifiers[i] = orderedModifiers[i+1]
                        orderedModifiers[i+1] = temp
                        changesMade = True
        return orderedModifiers


    # Determines the minimim position at which this modifier can occur.
    @classmethod
    def getMinPos(cls, modifier):
        position = cls.QUALITATIVE_POSITION
        if modifier.isA(LexicalCategory.NOUN) or modifier.isA(PhraseCategory.NOUN_PHRASE):
            position = cls.NOUN_POSITION
        elif modifier.isA(LexicalCategory.ADJECTIVE) or modifier.isA(PhraseCategory.ADJECTIVE_PHRASE):
            adjective = cls.getHeadWordElement(modifier)
            if adjective.getFeatureAsBoolean(LexicalFeature.QUALITATIVE):
                position = cls.QUALITATIVE_POSITION
            elif adjective.getFeatureAsBoolean(LexicalFeature.COLOUR):
                position = cls.COLOUR_POSITION
            elif adjective.getFeatureAsBoolean(LexicalFeature.CLASSIFYING):
                position = cls.CLASSIFYING_POSITION
        return position

    # Determines the maximim position at which this modifier can occur.
    @classmethod
    def getMaxPos(cls, modifier):
        position = cls.NOUN_POSITION
        if modifier.isA(LexicalCategory.ADJECTIVE) or modifier.isA(PhraseCategory.ADJECTIVE_PHRASE):
            adjective = cls.getHeadWordElement(modifier)
            if adjective.getFeatureAsBoolean(LexicalFeature.CLASSIFYING):
                position = cls.CLASSIFYING_POSITION
            elif adjective.getFeatureAsBoolean(LexicalFeature.COLOUR):
                position = cls.COLOUR_POSITION
            elif adjective.getFeatureAsBoolean(LexicalFeature.QUALITATIVE):
                position = cls.QUALITATIVE_POSITION
            else:
                position = cls.CLASSIFYING_POSITION
        return position

    # Retrieves the correct representation of the word from the element.
    @classmethod
    def getHeadWordElement(cls, element):
        head = None
        if isinstance(element, WordElement):
            head =  element
        elif isinstance(element, InflectedWordElement):
            head = element.getFeature(InternalFeature.BASE_WORD)
        elif isinstance(element, PhraseElement):
            head = cls.getHeadWordElement(element.getHead())
        return head

    # Creates the appropriate pronoun if the subject of the noun phrase is
    # pronominal.
    @classmethod
    def createPronoun(cls, parent, phrase):
        pronoun = "it"
        phraseFactory = phrase.getFactory()
        personValue = phrase.getFeature(Feature.PERSON)
        if Person.FIRST == personValue:
            pronoun = "I"
        elif Person.SECOND == personValue:
            pronoun = "you"
        else:
            genderValue = phrase.getFeature(LexicalFeature.GENDER)
            if Gender.FEMININE == genderValue:
                pronoun = "she"
            elif Gender.MASCULINE == genderValue:
                pronoun = "he"
        # AG: createWord now returns WordElement; so we embed it in an
        # inflected word element here
        proElement = phraseFactory.createWord(pronoun, LexicalCategory.PRONOUN)
        if isinstance(proElement, WordElement):
            element = InflectedWordElement(proElement)
            element.setFeature(LexicalFeature.GENDER, proElement.getFeature(LexicalFeature.GENDER))
            element.setFeature(Feature.PERSON, proElement.getFeature(Feature.PERSON))
        else:
            element = proElement
        element.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.SPECIFIER)
        element.setFeature(Feature.POSSESSIVE, phrase.getFeature(Feature.POSSESSIVE))
        element.setFeature(Feature.NUMBER, phrase.getFeature(Feature.NUMBER))
        if phrase.hasFeature(InternalFeature.DISCOURSE_FUNCTION):
            element.setFeature(InternalFeature.DISCOURSE_FUNCTION, \
                phrase.getFeature(InternalFeature.DISCOURSE_FUNCTION))
        return element
