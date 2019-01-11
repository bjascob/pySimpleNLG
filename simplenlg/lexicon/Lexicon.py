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

from abc            import ABC
from ..framework.LexicalCategory    import *
from ..framework.WordElement        import *


# This is the generic abstract class for a Lexicon.
class Lexicon(ABC):
    def __init__(self):
        pass

    # Return an instance of the default lexicon
    @staticmethod
    def getDefaultLexicon():
        from .XMLLexicon import XMLLexicon  #import here to prevent circular import
        return XMLLexicon()

    # create a default WordElement. May be overridden by specific types of lexicon
    def createWord(self, baseForm, category=None):
        return WordElement(baseForm, category)

    # General word lookup method, tries base form, variant, ID (in this order)
    # Creates new word if can't find existing word
    def lookupWord(self, baseForm, category=None):
        if not category:
            category = LexicalCategory.ANY
        if self.hasWord(baseForm, category):
            return self.getWord(baseForm, category)
        elif self.hasWordFromVariant(baseForm, category):
            return self.getWordFromVariant(baseForm, category)
        elif self.hasWordByID(baseForm):
            return self.getWordByID(baseForm)
        else:
            return self.createWord(baseForm, category)


    # returns all Words which have the specified base form and category
    def getWords(self, baseForm, category):
        assert False, 'Not implemented in base.'

    # get a WordElement which has the specified base form and category
    def getWord(self, baseForm, category=None):
        wordElements = self.getWords(baseForm, category)
        if not wordElements:
            return self.createWord(baseForm, category)
        else:
            return self.selectMatchingWord(wordElements, baseForm)

    # choose a single WordElement from a list of WordElements.  Prefer one
    # which exactly matches the baseForm
    def selectMatchingWord(self, wordElements, baseForm):
        # EHUD REITER  - this method added because some DBs are case-insensitive,
        # so a query on "man" returns both "man" and "MAN".  In such cases, the
        # exact match (eg, "man") should be returned
        # below check is redundant, since caller should check this
        if not wordElements:
            return self.createWord(baseForm)
        # look for exact match in base form
        for wordElement in wordElements:
            if wordElement.getBaseForm()==baseForm:
                return wordElement
        # Roman Kutlak: I don't think it is a good idea to return a word whose
        # case does not match because if a word appears in the lexicon
        # as an acronym only, it will be replaced as such. For example,
        # "foo" will return as the acronym "FOO". This does not seem desirable.
        # else return first element in list
        if wordElements[0].getBaseForm().lower() == baseForm.lower():
            return self.createWord(baseForm, LexicalCategory.ANY)
        return wordElements[0]

    # return true if the lexicon contains a WordElement which has
    # the specified base form and category
    def hasWord(self, baseForm, category=None):
        return len(self.getWords(baseForm, category))>0

    # returns a List of WordElement which have this ID.
    def getWordsByID(self, wid):
        assert False, 'Not implemented in base.'

    # get a WordElement with the specified ID
    def getWordByID(self, wid):
        wordElements = self.getWordsByID(wid)
        if not wordElements:
            return self.createWord(wid)
        else:
            return wordElements[0]

    # return true if the lexicon contains a WordElement which the specified ID
    def hasWordByID(self, wid):
        return len(self.getWordsByID(wid))>0


    # returns Words which have an inflected form and/or spelling variant that
    # matches the specified variant, and are in the specified category.
    def getWordsFromVariant(self, variant, category):
        assert False, 'Not implemented in base.'

    # returns a WordElement which has the specified inflected form and/or
    # spelling variant that matches the specified variant, of the specified
    # category
    def getWordFromVariant(self, variant, category=None):
        wordElements = self.getWordsFromVariant(variant, category)
        if not wordElements:
            return self.createWord(variant, category)
        if category is not None:
            return self.selectMatchingWord(wordElements, variant)
        else:
            return wordElements[0]

    # return true if the lexicon contains a WordElement which
    # matches the specified variant form and category
    def hasWordFromVariant(self, variant, category=None):
        return len(self.getWordsFromVariant(variant, category))>0

    #close the lexicon (if necessary) if lexicon does not need to be closed, this does nothing
    def close(self):
        pass
