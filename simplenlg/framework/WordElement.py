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

from .NLGElement                import *
from .LexicalCategory           import *
from ..features.Inflection      import *
from ..features.LexicalFeature  import *


# Internal class. This maintains inflectional variants of the word, which
# may be available in the lexicon.
class InflectionSet(object):
    def __init__(self, infl):
        self.infl  = infl   # Inflection
        self.forms = {}     # {str:str}  mapping values of LexicalFeature to actual word forms

    # set an inflectional form
    def addForm(self, feature, form):
        self.forms[feature] =  form

    # get an inflectional form
    def getForm(self, feature):
        return self.forms.get(feature, None)


# This is the class for a lexical entry (ie, a word).
class WordElement(NLGElement):
    # Words have baseForm, category, id, and features
    # features are inherited from NLGElement
    def __init__(self, baseForm=None, category=None, wid=None):
        super().__init__()
        if category is None:
            category = LexicalCategory.ANY
        self.setCategory(category)
        self.baseForm    = baseForm     # str
        self.id          = wid          # str (id in lexicon)
        self.inflVars    = {}           # {Inflection, InflectionSet} the inflectional variants
        self.defaultInfl = None         # Inflection # the default inflectional variant

    # Copy Constructor
    @staticmethod
    def fromWE(currentWord):
        we = WordElement(currentWord.getBaseForm(), currentWord.getCategory(), currentWord.getId())
        we.inflVars = currentWord.getInflectionalVariants()
        we.defaultInfl = currentWord.getDefaultInflectionalVariant()
        we.setFeatures(currentWord)
        return we

    #**********************************************************
    # getters and setters
    #**********************************************************
    def getBaseForm(self):
        return self.baseForm

    def getId(self):
        return self.id

    def setBaseForm(self, baseForm):
        self.baseForm = baseForm

    def setId(self, wid):
        self.id = wid

    # Set the default inflectional variant of a word.
    def setDefaultInflectionalVariant(self, variant):
        self.setFeature(LexicalFeature.DEFAULT_INFL, variant)
        self.defaultInfl = variant
        if variant in self.inflVars:
            infl_set = self.inflVars[variant]
            forms = LexicalFeature.getInflectionalFeatures(self.getCategory())
            if forms is not None:
                for f in forms:
                    self.setFeature(f, infl_set.getForm(f))

    # @return the default inflectional variant
    def getDefaultInflectionalVariant(self):
        return self.defaultInfl

    # Convenience method to get all the inflectional forms of the word.
    def getInflectionalVariants(self):
        return self.inflVars

    # Convenience method to set the default spelling variant of a word.
    def setDefaultSpellingVariant(self, variant):
        self.setFeature(LexicalFeature.DEFAULT_SPELL, variant)

    # Convenience method, equivalent to
    def getDefaultSpellingVariant(self):
        defSpell = self.getFeatureAsString(LexicalFeature.DEFAULT_SPELL)
        if defSpell is None:
            return self.getBaseForm()
        return defSpell

    # Add an inflectional variant to this word element.
    def addInflectionalVariant(self, infl, lexicalFeature=None, form=None):
        if lexicalFeature is None and form is None:
            self.inflVars[infl] = InflectionSet(infl)
        elif infl in self.inflVars:
            self.inflVars[infl].addForm(lexicalFeature, form)
        else:
            infl_set = InflectionSet(infl)
            infl_set.addForm(lexicalFeature, form)
            self.inflVars[infl] = infl_set

    # Check whether this word has a particular inflectional variant
    def hasInflectionalVariant(self, infl):
        return infl in self.inflVars

    # Sets Features from another existing WordElement into this WordElement.
    def setFeatures(self, currentWord):
        if currentWord is not None and currentWord.getAllfeatures():
            for feature in currentWord.getAllFeatureNames():
                self.setFeature(feature, currentWord.getFeature(feature))

    #**********************************************************
    # other methods
    #**********************************************************
    def __str__(self):
        buffer = 'WordElement[' + self.getBaseForm() + ':'
        category = self.getCategory()
        if category:
            buffer += str(category)
        else:
            buffer += "no category"
        buffer += ']'
        return buffer

    # This method returns an empty List as words do not have child elements.
    def getChildren(self):
        return []

    def printTree(self, indent=None):
        pstr = "WordElement: base=" + self.getBaseForm() + ", category=" + str(self.getCategory()) + ", " \
             + super().__str__() + '\n'
        return pstr

    # Check if this WordElement is equal to an object.
    def __eq__(self, we):
        if isinstance(we, WordElement):
            return self.baseForm==we.baseForm and self.id==we.id and self.features==we.features
        return False
    def __ne__(self, we):
        return not self.__eq__(we)

    # Defining __eq__ removes the default hash
    def __hash__(self):
        items = [self.baseForm, self.id]
        for key, value in self.features.items():
            items.append( (key, value) )
        return hash( tuple(items) )
