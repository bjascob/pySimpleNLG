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

from ..features.DiscourseFunction           import *
from ..features.Feature                     import *
from ..features.Form                        import *
from ..features.InternalFeature             import *
from ..features.Person                      import *
from ..features.Tense                       import *
from ..framework.CoordinatedPhraseElement   import *
from ..framework.InflectedWordElement       import *
from ..framework.LexicalCategory            import *
from ..framework.NLGElement                 import *
from ..framework.PhraseCategory             import *
from ..framework.PhraseElement              import *
from ..framework.WordElement                import *


# This class defines a verb phrase.
class VPPhraseSpec(PhraseElement):
    def __init__(self, phraseFactory):
        super().__init__(PhraseCategory.VERB_PHRASE)
        self.setFactory(phraseFactory)
        # set default feature values
        self.setFeature(Feature.PERFECT, False)
        self.setFeature(Feature.PROGRESSIVE, False)
        self.setFeature(Feature.PASSIVE, False)
        self.setFeature(Feature.NEGATED, False)
        self.setFeature(Feature.TENSE, Tense.PRESENT)
        self.setFeature(Feature.PERSON, Person.THIRD)
        self.setPlural(False)
        self.setFeature(Feature.FORM, Form.NORMAL)
        self.setFeature(InternalFeature.REALISE_AUXILIARY, True)

    # sets the verb (head) of a verb phrase.
    def setVerb(self, verb):
        if isinstance(verb, str):
            try:
                space = verb.index(' ')
            except ValueError:
                space = -1
            if space < 0: # no space, so no particle
                verbElement = self.getFactory().createWord(verb, LexicalCategory.VERB)
            else: # space, so break up into verb and particle
                verbElement = self.getFactory().createWord(verb[:space], LexicalCategory.VERB)
                self.setFeature(Feature.PARTICLE, verb[space+1:])
        else:  # Object is not a String
            verbElement = self.getFactory().createNLGElement(verb,LexicalCategory.VERB)
        self.setHead(verbElement)

    # @return verb (head) of verb phrase
    def getVerb(self):
        return self.getHead()

    # Sets the direct object of a clause  (assumes this is the only direct object)
    def setObject(self, obj):
        if isinstance(obj, PhraseElement) or isinstance(obj, CoordinatedPhraseElement):
            objectPhrase = obj
        else:
            objectPhrase = self.getFactory().createNounPhrase(obj)
        objectPhrase.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.OBJECT)
        self.setComplement(objectPhrase)

    # Returns the direct object of a clause (assumes there is only one)
    def getObject(self):
        complements = self.getFeatureAsElementList(InternalFeature.COMPLEMENTS)
        for complement in complements:
            if complement.getFeature(InternalFeature.DISCOURSE_FUNCTION) == DiscourseFunction.OBJECT:
                return complement
        return None

    # Set the indirect object of a clause (assumes this is the only direct indirect object)
    def setIndirectObject(self, indirectObject):
        if isinstance(indirectObject, PhraseElement) or isinstance(indirectObject, CoordinatedPhraseElement):
            indirectObjectPhrase = indirectObject
        else:
            indirectObjectPhrase = self.getFactory().createNounPhrase(indirectObject)
        indirectObjectPhrase.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.INDIRECT_OBJECT)
        self.setComplement(indirectObjectPhrase)

    # Returns the indirect object of a clause (assumes there is only one)
    def getIndirectObject(self):
        complements = self.getFeatureAsElementList(InternalFeature.COMPLEMENTS)
        for complement in complements:
            if complement.getFeature(InternalFeature.DISCOURSE_FUNCTION) == DiscourseFunction.INDIRECT_OBJECT:
                return complement
        return None

    # Add a modifier to a verb phrase
    # @Override
    def addModifier(self, modifier):
        # adverb is preModifier
        # string which is one lexicographic word is looked up in lexicon,
        # if it is an adverb than it becomes a preModifier
        # Everything else is postModifier
        if modifier is None:
            return
        # get modifier as NLGElement if possible
        if isinstance(modifier, NLGElement):
            modifierElement = modifier
        elif isinstance(modifier, str):
            modifierString = modifier
            if len(modifierString)>0 and " " not in modifierString:
                modifierElement = self.getFactory().createWord(modifier, LexicalCategory.ANY)
        # if no modifier element, must be a complex string
        if modifierElement is None:
            self.addPostModifier(modifier)
            return
        # extract WordElement if modifier is a single word
        if isinstance(modifierElement, WordElement):
            modifierWord = modifierElement
        elif isinstance(modifierElement, InflectedWordElement):
            modifierWord = modifierElement.getBaseWord()
        if modifierWord is not None and modifierWord.getCategory() == LexicalCategory.ADVERB:
            self.addPreModifier(modifierWord)
            return
        # default case
        self.addPostModifier(modifierElement)
