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

import re
from .CoordinatedPhraseElement  import *
from .DocumentCategory          import *
from .DocumentElement           import *
from .InflectedWordElement      import *
from .NLGElement                import *
from .PhraseElement             import *
from .StringElement             import *
from .WordElement               import *
from ..features.Feature         import *
from ..features.Gender          import *
from ..features.InternalFeature import *
from ..features.LexicalFeature  import *
from ..features.NumberAgreement import *
from ..features.Person          import *
from ..lexicon.Lexicon          import *
from ..phrasespec               import *


# This class contains methods for creating syntactic phrases. These methods
# should be used instead of directly invoking new on SPhraseSpec, etc.
class NLGFactory(object):
    PRONOUNS = ["I", "you", "he", "she", "it", "me", "you", "him", "her", "it", \
                "myself", "yourself", "himself", "herself", "itself", "mine", \
                "yours", "his", "hers", "its", "we", "you", "they", "they", "they", \
                "us", "you", "them", "them", "them", "ourselves", "yourselves", \
                "themselves", "themselves", "themselves", "ours", "yours", "theirs", \
                "theirs", "theirs", "there"]
    FIRST_PRONOUNS = ["I", "me", "myself", "we", "us", "ourselves", "mine", "my", "ours", "our"]
    SECOND_PRONOUNS = ["you","yourself", "yourselves", "yours", "your"]
    REFLEXIVE_PRONOUNS = ["myself", "yourself", "himself", "herself", "itself", \
                          "ourselves", "yourselves", "themselves"]
    MASCULINE_PRONOUNS = ["he", "him", "himself", "his"]
    FEMININE_PRONOUNS = ["she", "her", "herself", "hers"]
    POSSESSIVE_PRONOUNS =["mine", "ours", "yours", "his", "hers", "its", "theirs", \
                          "my", "our", "your", "her", "their"]
    PLURAL_PRONOUNS = ["we", "us", "ourselves", "ours", "our", "they", "them", "theirs", "their"]
    EITHER_NUMBER_PRONOUNS = ["there"]
    EXPLETIVE_PRONOUNS = ["there"]
    WORD_REGEX = r"\w*" # regex for determining if a string is a single word or not

    # Creates a new phrase factory with the associated lexicon.
    def __init__(self, newLexicon=None):
        self.setLexicon(newLexicon)

    # Sets the lexicon to be used by this factory. Passing a parameter of
    # null will remove any existing lexicon from the factory.
    def setLexicon(self, newLexicon):
        self.lexicon = newLexicon

    # Creates a new element representing a word. If the word passed is already
    # an NLGElement then that is returned unchanged.
    def createWord(self, word, category):
        wordElement = None
        if isinstance(word, NLGElement):
            wordElement = word
        elif isinstance(word, str) and self.lexicon is not None:
            wordElement = self.lexicon.lookupWord(word, category)
            if word in self.PRONOUNS:
                self.setPronounFeatures(wordElement, word)
        return wordElement

    # Create an inflected word element.
    def createInflectedWord(self, word, category):
        inflElement = None
        if isinstance(word, WordElement):
            inflElement = InflectedWordElement(word)
        elif isinstance(word, str):
            baseword = self.createWord(word, category)
            if baseword is not None and isinstance(baseword, WordElement):
                inflElement = InflectedWordElement(baseword)
            else:
                inflElement = InflectedWordElement(word, category)
        elif isinstance(word, NLGElement):
            inflElement = word
        return inflElement

    # A helper method to set the features on newly created pronoun words.
    def setPronounFeatures(self, wordElement, word):
        wordElement.setCategory(LexicalCategory.PRONOUN)
        if word in self.FIRST_PRONOUNS:
            wordElement.setFeature(Feature.PERSON, Person.FIRST)
        elif word in self.SECOND_PRONOUNS:
            wordElement.setFeature(Feature.PERSON, Person.SECOND)
            if "yourself" == word.lower():
                wordElement.setPlural(False)
            elif "yourselves" == word.lower():
                wordElement.setPlural(True)
            else:
                wordElement.setFeature(Feature.NUMBER, NumberAgreement.BOTH)
        else:
            wordElement.setFeature(Feature.PERSON, Person.THIRD)
        if word in self.REFLEXIVE_PRONOUNS:
            wordElement.setFeature(LexicalFeature.REFLEXIVE, True)
        else:
            wordElement.setFeature(LexicalFeature.REFLEXIVE, False)
        if word in self.MASCULINE_PRONOUNS:
            wordElement.setFeature(LexicalFeature.GENDER, Gender.MASCULINE)
        elif word in self.FEMININE_PRONOUNS:
            wordElement.setFeature(LexicalFeature.GENDER, Gender.FEMININE)
        else:
            wordElement.setFeature(LexicalFeature.GENDER, Gender.NEUTER)
        if word in self.POSSESSIVE_PRONOUNS:
            wordElement.setFeature(Feature.POSSESSIVE, True)
        else:
            wordElement.setFeature(Feature.POSSESSIVE, False)
        if word in self.PLURAL_PRONOUNS and not word in self.SECOND_PRONOUNS:
            wordElement.setPlural(True)
        elif word not in self.EITHER_NUMBER_PRONOUNS:
            wordElement.setPlural(False)
        if word in self.EXPLETIVE_PRONOUNS:
            wordElement.setFeature(InternalFeature.NON_MORPH, True)
            wordElement.setFeature(LexicalFeature.EXPLETIVE_SUBJECT, True)

    # Creates a preposition phrase with the given preposition and complement.
    def createPrepositionPhrase(self, preposition=None, complement=None):
        phraseElement = PPPhraseSpec(self)
        prepositionalElement = self.createNLGElement(preposition, LexicalCategory.PREPOSITION)
        self.setPhraseHead(phraseElement, prepositionalElement)
        if complement is not None:
            self.setComplement(phraseElement, complement)
        return phraseElement

    # A helper method for setting the complement of a phrase.
    def setComplement(self, phraseElement, complement):
        complementElement = self.createNLGElement(complement)
        phraseElement.addComplement(complementElement)

    # this method creates an NLGElement from an object
    def createNLGElement(self, element, category=None):
        if element is None:
            return None
        if category is None:
            category = LexicalCategory.ANY
        # InflectedWordElement - return underlying word
        if isinstance(element, InflectedWordElement):
            return element.getBaseWord()
        # StringElement - look up in lexicon if it is a word otherwise return element
        elif isinstance(element, StringElement):
            if self.stringIsWord(element.getRealisation(), category):
                return self.createWord(element.getRealisation(), category)
            else:
                return element
        # other NLGElement - return element
        elif isinstance(element, NLGElement):
            return element
        # String - look up in lexicon if a word, otherwise return StringElement
        elif isinstance(element, str):
            if self.stringIsWord(element, category):
                return self.createWord(element, category)
            else:
                return StringElement(element)
        else:
            raise ValueError('Invalid element type: ' + str(type(element)))

    # return true if string is a word
    def stringIsWord(self, string, category):
        return self.lexicon is not None and \
               (self.lexicon.hasWord(string, category) or string in self.PRONOUNS or \
                re.fullmatch(self.WORD_REGEX, string))

    # Creates a noun phrase with the given specifier and subject.
    def createNounPhrase(self, ina=None, inb=None):
        # single paramter => createNounPhrase(noun)
        if ina is not None and inb is None:
            return self._createNP1(ina)
        # otherwise assume two paramters => createNounPhrase(specifier, noun)
        else:
            return self._createNP2(ina, inb)

    # createNounPhrase(noun)
    def _createNP1(self, noun):
        if isinstance(noun, NPPhraseSpec):
            return noun
        else:
            return self._createNP2(None, noun)

    # createNounPhrase(sepcifer, noun)
    def _createNP2(self, specifier, noun):
        if isinstance(noun, NPPhraseSpec):
            return noun
        phraseElement = NPPhraseSpec(self)
        nounElement = self.createNLGElement(noun, LexicalCategory.NOUN)
        self.setPhraseHead(phraseElement, nounElement)
        if specifier is not None:
            phraseElement.setSpecifier(specifier)
        return phraseElement

    # A helper method to set the head feature of the phrase.
    def setPhraseHead(self, phraseElement , headElement):
        if headElement is not None:
            phraseElement.setHead(headElement)
            headElement.setParent(phraseElement)

    # Creates an adjective phrase wrapping the given adjective.
    def createAdjectivePhrase(self, adjective=None):
        phraseElement = AdjPhraseSpec(self)
        adjectiveElement = self.createNLGElement(adjective, LexicalCategory.ADJECTIVE)
        self.setPhraseHead(phraseElement, adjectiveElement)
        return phraseElement

    # Creates a verb phrase wrapping the main verb given.
    def createVerbPhrase(self, verb=None):
        phraseElement = VPPhraseSpec(self)
        phraseElement.setVerb(verb)
        self.setPhraseHead(phraseElement, phraseElement.getVerb())
        return phraseElement

    # Creates an adverb phrase wrapping the given adverb.
    def createAdverbPhrase(self, adverb=None):
        phraseElement = AdvPhraseSpec(self)
        adverbElement = self.createNLGElement(adverb, LexicalCategory.ADVERB)
        self.setPhraseHead(phraseElement, adverbElement)
        return phraseElement

    # Creates a clause with the given subject, verb or verb phrase and direct
    # object but no indirect object.
    def createClause(self, subject=None, verb=None, directObject=None):
        phraseElement = SPhraseSpec(self)
        if verb is not None:
            # AG: fix here: check if "verb" is a VPPhraseSpec or a Verb
            if isinstance(verb, PhraseElement):
                phraseElement.setVerbPhrase(verb)
            else:
                phraseElement.setVerb(verb)
        if subject is not None:
            phraseElement.setSubject(subject)
        if directObject is not None:
            phraseElement.setObject(directObject)
        return phraseElement

    # Creates a canned text phrase with the given text.
    def createStringElement(self, text=None):
        return StringElement(text)

    # Creates a new coordinated phrase with two elements (initially)
    def createCoordinatedPhrase(self, coord1=None, coord2=None):
        return CoordinatedPhraseElement(coord1, coord2)

    #*********************************************************************************
    # Document level stuff
    #*********************************************************************************

    # Creates a new document element
    def createDocument(self, title=None, component=None):
        document = DocumentElement(DocumentCategory.DOCUMENT, title)
        if component is None:
            pass
        elif isinstance(component, list):
            document.addComponents(component)
        elif isinstance(component, NLGElement):
            document.addComponent(component)
        else:
            raise ValueError('Invalid component type: ' + str(type(component)))
        return document

    # Creates a new section element with the given title and adds the given
    # component.
    def createList(self, component=None):
        dlist = DocumentElement(DocumentCategory.LIST, None)
        if component is None:
            pass
        elif isinstance(component, list):
            dlist.addComponents(component)
        elif isinstance(component, NLGElement):
            dlist.addComponent(component)
        else:
            raise ValueError('Invalid component type: ' + str(type(component)))
        return dlist

    # Creates a new section element with the given title and adds the given
    # component.
    def createEnumeratedList(self, component=None):
        dlist = DocumentElement(DocumentCategory.ENUMERATED_LIST, None)
        if component is None:
            pass
        elif isinstance(component, list):
            dlist.addComponents(component)
        elif isinstance(component, NLGElement):
            dlist.addComponent(component)
        else:
            raise ValueError('Invalid component type: ' + str(type(component)))
        return dlist

    # Creates a list item for adding to a list element. The list item has the
    # given component.
    def createListItem(self, component=None):
        if component is None:
            return DocumentElement(DocumentCategory.LIST_ITEM, None)
        elif isinstance(component, NLGElement):
            listItem = DocumentElement(DocumentCategory.LIST_ITEM, None)
            listItem.addComponent(component)
            return listItem
        else:
            raise ValueError('Invalid component type: ' + str(type(component)))

    # Creates a new paragraph element and adds the given component
    def createParagraph(self, component=None):
        paragraph = DocumentElement(DocumentCategory.PARAGRAPH, None)
        if component is None:
            pass
        elif isinstance(component, list):
            paragraph.addComponents(component)
        elif isinstance(component, NLGElement):
            paragraph.addComponent(component)
        else:
            raise ValueError('Invalid component type: ' + str(type(component)))
        return paragraph

    # Creates a new section element.
    def createSection(self, title=None, component=None):
        if title is None and component is None:
            return DocumentElement(DocumentCategory.SECTION, None)
        if not isinstance(title, str):
            raise ValueError('Invalid title type: ' + str(type(title)))
        section = DocumentElement(DocumentCategory.SECTION, title)
        if component is None:
            pass
        elif isinstance(component, list):
            section.addComponents(component)
        elif isinstance(component, NLGElement):
            section.addComponent(component)
        else:
            raise ValueError('Invalid component type: ' + str(type(component)))
        return section

    # Creates a sentence
    def createSentence(self, a=None, b=None, c=None):
        sentence = DocumentElement(DocumentCategory.SENTENCE, None)
        if a is None and b is None and c is None:
            pass
        elif isinstance(a, list):
            sentence.addComponents(a)
        elif isinstance(a, NLGElement):
            sentence.addComponent(a)
        elif isinstance(a, str) and b is None and c is None:
            if a is not None:
                sentence.addComponent(self.createStringElement(a))
            return sentence
        else:
            sentence.addComponent(self.createClause(a, b, c))
        return sentence
