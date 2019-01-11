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

from ..features.ClauseStatus                import *
from ..features.Feature                     import *
from ..features.InternalFeature             import *
from ..features.LexicalFeature              import *
from ..framework.CoordinatedPhraseElement   import *
from ..framework.InflectedWordElement       import *
from ..framework.LexicalCategory            import *
from ..framework.NLGElement                 import *
from ..framework.PhraseCategory             import *
from ..framework.PhraseElement              import *
from ..framework.WordElement                import *
from .VPPhraseSpec                          import *
from .AdvPhraseSpec                         import *


# This class defines a clause (sentence-like phrase).
class SPhraseSpec(PhraseElement):
    vpFeatures = [Feature.MODAL, Feature.TENSE, Feature.NEGATED, Feature.NUMBER, Feature.PASSIVE, \
                  Feature.PERFECT, Feature.PARTICLE, Feature.PERSON, Feature.PROGRESSIVE, \
                  InternalFeature.REALISE_AUXILIARY, Feature.FORM, Feature.INTERROGATIVE_TYPE]

    def __init__(self, phraseFactory):
        super().__init__(PhraseCategory.CLAUSE)
        self.setFactory(phraseFactory)
        # create VP
        self.setVerbPhrase(phraseFactory.createVerbPhrase())
        # set default values
        self.setFeature(Feature.ELIDED, False)
        self.setFeature(InternalFeature.CLAUSE_STATUS, ClauseStatus.MATRIX)
        self.setFeature(Feature.SUPRESSED_COMPLEMENTISER, False)
        self.setFeature(LexicalFeature.EXPLETIVE_SUBJECT, False)
        self.setFeature(Feature.COMPLEMENTISER, phraseFactory.createWord( \
                "that", LexicalCategory.COMPLEMENTISER))

    # intercept and override setFeature, to set VP features as needed
    # adds a feature, possibly to the underlying VP as well as the SPhraseSpec itself
    # @Override
    def setFeature(self, featureName, featureValue):
        super().setFeature(featureName, featureValue)
        if featureName in self.vpFeatures:
            verbPhrase = self.getFeatureAsElement(InternalFeature.VERB_PHRASE)
            if isinstance(verbPhrase, VPPhraseSpec):
                verbPhrase.setFeature(featureName, featureValue)

    # adds a premodifier, if possible to the underlying VP
    # @Override
    def addPreModifier(self, newPreModifier):
        verbPhrase = self.getFeatureAsElement(InternalFeature.VERB_PHRASE)
        if verbPhrase is not None:
            if isinstance(verbPhrase, PhraseElement):
                verbPhrase.addPreModifier(newPreModifier)
            elif isinstance(verbPhrase, CoordinatedPhraseElement):
                verbPhrase.addPreModifier(newPreModifier)
            else:
                super().addPreModifier(newPreModifier)

    # adds a complement, if possible to the underlying VP
    # @Override
    def addComplement(self, newComplement):
        verbPhrase = self.getFeatureAsElement(InternalFeature.VERB_PHRASE)
        if isinstance(verbPhrase, VPPhraseSpec):
            verbPhrase.addComplement(newComplement)
        else:
            super().addComplement(newComplement)

    # @see simplenlg.framework.NLGElement#getFeature(java.lang.String)
    # @Override
    def getFeature(self, featureName):
        if super().getFeature(featureName) is not None:
            return super().getFeature(featureName)
        if  featureName in self.vpFeatures:
            verbPhrase = self.getFeatureAsElement(InternalFeature.VERB_PHRASE)
            if isinstance(verbPhrase, VPPhraseSpec):
                return verbPhrase.getFeature(featureName)
        return None

    # @return VP for this clause
    def getVerbPhrase(self):
        return self.getFeatureAsElement(InternalFeature.VERB_PHRASE)

    def setVerbPhrase(self, vp):
        self.setFeature(InternalFeature.VERB_PHRASE, vp)
        vp.setParent(self) # needed for syntactic processing

    # Set the verb of a clause
    def setVerb(self, verb):
        # get verb phrase element (create if necessary)
        verbPhraseElement = self.getVerbPhrase()
        # set head of VP to verb (if this is VPPhraseSpec, and not a coord)
        if isinstance(verbPhraseElement, VPPhraseSpec):
            verbPhraseElement.setVerb(verb)

    # Returns the verb of a clause
    def getVerb(self):
        # WARNING - I don't understand verb phrase, so this may not work!!
        verbPhrase = self.getFeatureAsElement(InternalFeature.VERB_PHRASE)
        if isinstance(verbPhrase, VPPhraseSpec):
            return verbPhrase.getHead()
        else:
            # return null if VP is coordinated phrase
            return None

    # Sets the subject of a clause (assumes this is the only subject)
    def setSubject(self, subject):
        if isinstance(subject, PhraseElement) or isinstance(subject, CoordinatedPhraseElement):
            subjectPhrase = subject
        else:
            subjectPhrase = self.getFactory().createNounPhrase(subject)
        subjects = [subjectPhrase]
        self.setFeature(InternalFeature.SUBJECTS, subjects)

    # Returns the subject of a clause (assumes there is only one)
    def getSubject(self):
        subjects = self.getFeatureAsElementList(InternalFeature.SUBJECTS)
        if not subjects:
            return None
        return subjects[0]

    # Sets the direct object of a clause (assumes this is the only direct object)
    def setObject(self, obj):
        # get verb phrase element (create if necessary)
        verbPhraseElement = self.getVerbPhrase()
        # set object of VP to verb (if this is VPPhraseSpec, and not a coord)
        if isinstance(verbPhraseElement, VPPhraseSpec):
            verbPhraseElement.setObject(obj)

    # Returns the direct object of a clause (assumes there is only one)
    def getObject(self):
        verbPhrase = self.getFeatureAsElement(InternalFeature.VERB_PHRASE)
        if isinstance(verbPhrase, VPPhraseSpec):
            return verbPhrase.getObject()
        else:
            # return null if VP is coordinated phrase
            return None

    # Set the indirect object of a clause (assumes this is the only direct
    # indirect object)
    def setIndirectObject(self, indirectObject):
        # get verb phrase element (create if necessary)
        verbPhraseElement = self.getVerbPhrase()
        # set head of VP to verb (if this is VPPhraseSpec, and not a coord)
        if isinstance(verbPhraseElement, VPPhraseSpec):
            verbPhraseElement.setIndirectObject(indirectObject)

    # Returns the indirect object of a clause (assumes there is only one)
    def getIndirectObject(self):
        verbPhrase = self.getFeatureAsElement(InternalFeature.VERB_PHRASE)
        if isinstance(verbPhrase, VPPhraseSpec):
            return verbPhrase.getIndirectObject()
        else:
            # return null if VP is coordinated phrase
            return None

    # Add a modifier to a clause Use heuristics to decide where it goes
    # @Override
    def addModifier(self, modifier):
        # adverb is frontModifier if sentenceModifier
        # otherwise adverb is preModifier
        # string which is one lexicographic word is looked up in lexicon,
        # above rules apply if adverb
        # Everything else is postModifier
        if modifier is None:
            return
        # get modifier as NLGElement if possible
        modifierElement = None
        if isinstance(modifier, NLGElement):
            modifierElement = modifier
        elif isinstance(modifier, str):
            modifierString = modifier
            if len(modifierString)>0 and not " " in modifierString:
                modifierElement = self.getFactory().createWord(modifier, LexicalCategory.ANY)
        # if no modifier element, must be a complex string
        if modifierElement is None:
            self.addPostModifier(str(modifier))
            return
        # AdvP is premodifer (probably should look at head to see if
        # sentenceModifier)
        if isinstance(modifierElement, AdvPhraseSpec):
            self.addPreModifier(modifierElement)
            return
        # extract WordElement if modifier is a single word
        if isinstance(modifierElement, WordElement):
            modifierWord = modifierElement
        elif isinstance(modifierElement, InflectedWordElement):
            modifierWord = modifierElement.getBaseWord()
        if modifierWord is not None and modifierWord.getCategory() == LexicalCategory.ADVERB:
            # adverb rules
            if modifierWord.getFeatureAsBoolean(LexicalFeature.SENTENCE_MODIFIER):
                self.addFrontModifier(modifierWord)
            else:
                self.addPreModifier(modifierWord)
            return
        # default case
        self.addPostModifier(modifierElement)
