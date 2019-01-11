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
from ...features.LexicalFeature             import *
from ...framework.CoordinatedPhraseElement  import *
from ...framework.InflectedWordElement      import *
from ...framework.LexicalCategory           import *
from ...framework.ListElement               import *
from ...framework.PhraseCategory            import *
from ...framework.WordElement               import *
from .PhraseHelper                          import *


# This class contains static methods to help the syntax processor realise
# coordinated phrases.
class CoordinatedPhraseHelper(object):
    # The main method for realising coordinated phrases.
    @classmethod
    def realise(cls, parent, phrase):
        realisedElement = None
        if phrase is not None:
            realisedElement = ListElement()
            PhraseHelper.realiseList(parent, realisedElement, phrase.getPreModifiers(), \
                    DiscourseFunction.PRE_MODIFIER)
            coordinated = CoordinatedPhraseElement()
            children = phrase.getChildren()
            conjunction = phrase.getFeatureAsString(Feature.CONJUNCTION)
            coordinated.setFeature(Feature.CONJUNCTION, conjunction)
            coordinated.setFeature(Feature.CONJUNCTION_TYPE, phrase.getFeature(Feature.CONJUNCTION_TYPE))
            conjunctionElement = None
            if children:
                if phrase.getFeatureAsBoolean(Feature.RAISE_SPECIFIER):
                    cls.raiseSpecifier(children)
                child = phrase.getLastCoordinate()
                child.setFeature(Feature.POSSESSIVE, phrase.getFeature(Feature.POSSESSIVE))
                child = children[0]
                cls.setChildFeatures(phrase, child)
                coordinated.addCoordinate(parent.realise(child))
                for index, child in enumerate(children):
                    if 0==index: continue
                    cls.setChildFeatures(phrase, child)
                    if phrase.getFeatureAsBoolean(Feature.AGGREGATE_AUXILIARY):
                        child.setFeature(InternalFeature.REALISE_AUXILIARY, False)
                    if child.isA(PhraseCategory.CLAUSE):
                        child.setFeature(Feature.SUPRESSED_COMPLEMENTISER, \
                                phrase.getFeature(Feature.SUPRESSED_COMPLEMENTISER))
                    #skip conjunction if it's null or empty string
                    if conjunction:
                        conjunctionElement = InflectedWordElement(conjunction, LexicalCategory.CONJUNCTION)
                        conjunctionElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.CONJUNCTION)
                        coordinated.addCoordinate(conjunctionElement)
                    coordinated.addCoordinate(parent.realise(child))
                realisedElement.addComponent(coordinated)
            PhraseHelper.realiseList(parent, realisedElement, phrase.getPostModifiers(), DiscourseFunction.POST_MODIFIER)
            PhraseHelper.realiseList(parent, realisedElement, phrase.getComplements(), DiscourseFunction.COMPLEMENT)
        return realisedElement

    # Sets the common features from the phrase to the child element.
    @classmethod
    def setChildFeatures(cls, phrase, child):
        if phrase.hasFeature(Feature.PROGRESSIVE):
            child.setFeature(Feature.PROGRESSIVE, phrase.getFeature(Feature.PROGRESSIVE))
        if phrase.hasFeature(Feature.PERFECT):
            child.setFeature(Feature.PERFECT, phrase.getFeature(Feature.PERFECT))
        if phrase.hasFeature(InternalFeature.SPECIFIER):
            child.setFeature(InternalFeature.SPECIFIER, phrase.getFeature(InternalFeature.SPECIFIER))
        if phrase.hasFeature(LexicalFeature.GENDER):
            child.setFeature(LexicalFeature.GENDER, phrase.getFeature(LexicalFeature.GENDER))
        if phrase.hasFeature(Feature.NUMBER):
            child.setFeature(Feature.NUMBER, phrase.getFeature(Feature.NUMBER))
        if phrase.hasFeature(Feature.TENSE):
            child.setFeature(Feature.TENSE, phrase.getFeature(Feature.TENSE))
        if phrase.hasFeature(Feature.PERSON):
            child.setFeature(Feature.PERSON, phrase.getFeature(Feature.PERSON))
        if phrase.hasFeature(Feature.NEGATED):
            child.setFeature(Feature.NEGATED, phrase.getFeature(Feature.NEGATED))
        if phrase.hasFeature(Feature.MODAL):
            child.setFeature(Feature.MODAL, phrase.getFeature(Feature.MODAL))
        if phrase.hasFeature(InternalFeature.DISCOURSE_FUNCTION):
            child.setFeature(InternalFeature.DISCOURSE_FUNCTION, phrase.getFeature(InternalFeature.DISCOURSE_FUNCTION))
        if phrase.hasFeature(Feature.FORM):
            child.setFeature(Feature.FORM, phrase.getFeature(Feature.FORM))
        if phrase.hasFeature(InternalFeature.CLAUSE_STATUS):
            child.setFeature(InternalFeature.CLAUSE_STATUS, phrase.getFeature(InternalFeature.CLAUSE_STATUS))
        if phrase.hasFeature(Feature.INTERROGATIVE_TYPE):
            child.setFeature(InternalFeature.IGNORE_MODAL, True)

    # Checks to see if the specifier can be raised and then raises it. In order
    # to be raised the specifier must be the same on all coordinates.
    @classmethod
    def raiseSpecifier(cls, children):
        allMatch = True
        child = None if not children else children[0]
        specifier = None
        test = None
        if child is not None:
            specifier = child.getFeatureAsElement(InternalFeature.SPECIFIER)
            if specifier is not None:
                # AG: this assumes the specifier is an InflectedWordElement or phrase.
                # it could be a Wordelement, in which case, we want the baseform
                if isinstance(specifier, WordElement):
                    test = specifier.getBaseForm()
                else:
                    specifier.getFeatureAsString(LexicalFeature.BASE_FORM)
            if test is not None:
                index = 1
                while index < len(children) and allMatch:
                    child = children[index]
                    if child is None:
                        allMatch = False
                    else:
                        specifier = child.getFeatureAsElement(InternalFeature.SPECIFIER)
                        if isinstance(specifier, WordElement):
                            childForm = specifier.getBaseForm()
                        else:
                            specifier.getFeatureAsString(LexicalFeature.BASE_FORM)
                        if not test == childForm:
                            allMatch = False
                    index += 1
                if allMatch:
                    for eachChild in range(1,len(children)):
                        child = children[eachChild]
                        child.setFeature(InternalFeature.RAISED, True)
