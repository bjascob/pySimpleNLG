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

from ..features.DiscourseFunction       import *
from ..features.Feature                 import *
from ..features.Gender                  import *
from ..features.InternalFeature         import *
from ..features.LexicalFeature          import *
from ..features.Person                  import *
from ..framework.InflectedWordElement   import *
from ..framework.LexicalCategory        import *
from ..framework.NLGElement             import *
from ..framework.PhraseCategory         import *
from ..framework.PhraseElement          import *
from ..framework.WordElement            import *
from .AdjPhraseSpec                     import *


# This class defines a noun phrase. 
class NPPhraseSpec(PhraseElement):
    def __init__(self, phraseFactory):
        super().__init__(PhraseCategory.NOUN_PHRASE)
        self.setFactory(phraseFactory)

    # @see simplenlg.framework.PhraseElement#setHead(java.lang.Object) This
    # version sets NP default features from the head
    # @Override
    def setHead(self, newHead):
        super().setHead(newHead)
        self.setNounPhraseFeatures(self.getFeatureAsElement(InternalFeature.HEAD))

    # A helper method to set the features required for noun phrases, from the
    # head noun
    def setNounPhraseFeatures(self, nounElement):
        if nounElement is None:
            return
        self.setFeature(Feature.POSSESSIVE, nounElement.getFeatureAsBoolean(Feature.POSSESSIVE))
        self.setFeature(InternalFeature.RAISED, False)
        self.setFeature(InternalFeature.ACRONYM, False)
        if nounElement.hasFeature(Feature.NUMBER):
            self.setFeature(Feature.NUMBER, nounElement.getFeature(Feature.NUMBER))
        else:
            self.setPlural(False)
        if nounElement.hasFeature(Feature.PERSON):
            self.setFeature(Feature.PERSON, nounElement.getFeature(Feature.PERSON))
        else:
            self.setFeature(Feature.PERSON, Person.THIRD)
        if nounElement.hasFeature(LexicalFeature.GENDER):
            self.setFeature(LexicalFeature.GENDER, nounElement.getFeature(LexicalFeature.GENDER))
        else:
            self.setFeature(LexicalFeature.GENDER, Gender.NEUTER)
        if nounElement.hasFeature(LexicalFeature.EXPLETIVE_SUBJECT):
            self.setFeature(LexicalFeature.EXPLETIVE_SUBJECT, nounElement.getFeature(LexicalFeature.EXPLETIVE_SUBJECT))
        self.setFeature(Feature.ADJECTIVE_ORDERING, True)

    # sets the noun (head) of a noun phrase
    def setNoun(self, noun):
        nounElement = self.getFactory().createNLGElement(noun, LexicalCategory.NOUN)
        self.setHead(nounElement)

    # @return noun (head) of noun phrase
    def getNoun(self):
        return self.getHead()

    # setDeterminer - Convenience method for when a person tries to set
    #                 a determiner (e.g. "the") to a NPPhraseSpec.
    def setDeterminer(self, determiner):
        self.setSpecifier(determiner)

    # getDeterminer - Convenience method for when a person tries to get a
    #                 determiner (e.g. "the") from a NPPhraseSpec.
    def getDeterminer(self):
        return self.getSpecifier()

    # sets the specifier of a noun phrase. Can be determiner (eg "the"),
    # possessive (eg, "John's")
    def setSpecifier(self, specifier):
        if isinstance(specifier, NLGElement):
            self.setFeature(InternalFeature.SPECIFIER, specifier)
            specifier.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.SPECIFIER)
        else:
            # create specifier as word (assume determiner)
            specifierElement = self.getFactory().createWord(specifier, LexicalCategory.DETERMINER)
            # set specifier feature
            if specifierElement is not None:
                self.setFeature(InternalFeature.SPECIFIER, specifierElement)
                specifierElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.SPECIFIER)

    # @return specifier (eg, determiner) of noun phrase
    def getSpecifier(self):
        return self.getFeatureAsElement(InternalFeature.SPECIFIER)

    # Add a modifier to an NP Use heuristics to decide where it goes
    # @Override
    def addModifier(self, modifier):
        # string which is one lexicographic word is looked up in lexicon,
        # adjective is preModifier
        # Everything else is postModifier
        if modifier is None:
            return
        # get modifier as NLGElement if possible
        modifierElement = None
        if isinstance(modifier, NLGElement):
            modifierElement = modifier
        elif isinstance(modifier, str):
            modifierString = modifier
            if len(modifierString) > 0 and not " " in modifierString:
                modifierElement = self.getFactory().createWord(modifier, LexicalCategory.ANY)
        # if no modifier element, must be a complex string, add as postModifier
        if modifierElement is None:
            self.addPostModifier(modifier)
            return
        # AdjP is premodifer
        if isinstance(modifierElement, AdjPhraseSpec):
            self.addPreModifier(modifierElement)
            return
        # else extract WordElement if modifier is a single word
        modifierWord = None
        if modifierElement is not None and isinstance(modifierElement, WordElement):
            modifierWord = modifierElement
        elif modifierElement is not None and isinstance(modifierElement, InflectedWordElement):
            modifierWord = modifierElement.getBaseWord()
        # check if modifier is an adjective
        if modifierWord is not None and modifierWord.getCategory() == LexicalCategory.ADJECTIVE:
            self.addPreModifier(modifierWord)
            return
        # default case
        self.addPostModifier(modifierElement)
