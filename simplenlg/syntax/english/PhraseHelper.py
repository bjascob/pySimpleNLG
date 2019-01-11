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

from ...features.DiscourseFunction      import *
from ...features.Feature                import *
from ...features.InternalFeature        import *
from ...features.LexicalFeature         import *
from ...framework.InflectedWordElement  import *
from ...framework.LexicalCategory       import *
from ...framework.ListElement           import *
from ...framework.PhraseCategory        import *
from ...framework.PhraseElement         import *


# This class contains static methods to help the syntax processor realise
# phrases.
class PhraseHelper(object):
    # The main method for realising phrases.
    @classmethod
    def realise(cls, parent, phrase):
        realisedElement = ListElement()
        if phrase is not None:
            realisedElement = ListElement()
            cls.realiseList(parent, realisedElement, phrase.getPreModifiers(), \
                    DiscourseFunction.PRE_MODIFIER)
            cls.realiseHead(parent, phrase, realisedElement)
            cls.realiseComplements(parent, phrase, realisedElement)
            PhraseHelper.realiseList(parent, realisedElement, \
                    phrase.getPostModifiers(), DiscourseFunction.POST_MODIFIER)
        return realisedElement

    # Realises the complements of the phrase adding and where
    # appropriate.
    @classmethod
    def realiseComplements(cls, parent, phrase, realisedElement):
        firstProcessed = False
        for complement in phrase.getFeatureAsElementList(InternalFeature.COMPLEMENTS):
            currentElement = parent.realise(complement)
            if currentElement is not None:
                currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.COMPLEMENT)
                if firstProcessed:
                    realisedElement.addComponent(InflectedWordElement("and", LexicalCategory.CONJUNCTION))
                else:
                    firstProcessed = True
                realisedElement.addComponent(currentElement)

    # Realises the head element of the phrase.
    @classmethod
    def realiseHead(cls, parent, phrase, realisedElement):
        head = phrase.getHead()
        if head is not None:
            if phrase.hasFeature(Feature.IS_COMPARATIVE):
                head.setFeature(Feature.IS_COMPARATIVE, phrase.getFeature(Feature.IS_COMPARATIVE))
            elif phrase.hasFeature(Feature.IS_SUPERLATIVE):
                head.setFeature(Feature.IS_SUPERLATIVE, phrase.getFeature(Feature.IS_SUPERLATIVE))
            head = parent.realise(head)
            head.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.HEAD)
            realisedElement.addComponent(head)

    # Iterates through a List of NLGElements
    # realisation each element and adding it to the on-going realisation of
    # this clause.
    @classmethod
    def realiseList(cls, parent, realisedElement, elementList, function):
        # AG: Change here: the original list structure is kept, i.e. rather
        # than taking the elements of the list and putting them in the realised
        # element, we now add the realised elements to a new list and put that
        # in the realised element list. This preserves constituency for
        # orthography and morphology processing later.
        realisedList = ListElement()
        for eachElement in elementList:
            currentElement = parent.realise(eachElement)
            if currentElement is not None:
                currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, function)
                if eachElement.getFeatureAsBoolean(Feature.APPOSITIVE):
                    currentElement.setFeature(Feature.APPOSITIVE, True)
                realisedList.addComponent(currentElement)
        if realisedList.getChildren():
            realisedElement.addComponent(realisedList)

    # Determines if the given phrase has an expletive as a subject.
    @classmethod
    def isExpletiveSubject(cls, phrase):
        subjects = phrase.getFeatureAsElementList(InternalFeature.SUBJECTS)
        expletive = False
        if len(subjects) == 1:
            subjectNP = subjects[0]
            if subjectNP.isA(PhraseCategory.NOUN_PHRASE):
                expletive = subjectNP.getFeatureAsBoolean(LexicalFeature.EXPLETIVE_SUBJECT)
            elif subjectNP.isA(PhraseCategory.CANNED_TEXT):
                expletive = "there" == subjectNP.getRealisation().lower()
        return expletive
