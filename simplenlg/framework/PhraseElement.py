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

from .NLGElement                    import *
from ..features.ClauseStatus        import *
from ..features.DiscourseFunction   import *
from ..features.Feature             import *
from ..features.InternalFeature     import *
from .CoordinatedPhraseElement      import *
from .StringElement                 import *
from .LexicalCategory               import *

# This class defines a phrase.
class PhraseElement(NLGElement):
    def __init__(self, newCategory):
        super().__init__()
        self.setCategory(newCategory)
        self.setFeature(Feature.ELIDED, False)

    # This method retrieves the child components of this phrase.
    # @Override
    def getChildren(self):
        children = []
        category = self.getCategory()
        currentElement = None
        if isinstance(category, PhraseCategory):
            if category == PhraseCategory.CLAUSE:
                currentElement = self.getFeatureAsElement(Feature.CUE_PHRASE)
                if currentElement is not None:
                    children.append(currentElement)
                children.extend(self.getFeatureAsElementList(InternalFeature.FRONT_MODIFIERS))
                children.extend(self.getFeatureAsElementList(InternalFeature.PREMODIFIERS))
                children.extend(self.getFeatureAsElementList(InternalFeature.SUBJECTS))
                children.extend(self.getFeatureAsElementList(InternalFeature.VERB_PHRASE))
                children.extend(self.getFeatureAsElementList(InternalFeature.COMPLEMENTS))
            elif category == PhraseCategory.NOUN_PHRASE:
                currentElement = self.getFeatureAsElement(InternalFeature.SPECIFIER)
                if currentElement is not None:
                    children.append(currentElement)
                children.extend(self.getFeatureAsElementList(InternalFeature.PREMODIFIERS))
                currentElement = self.getHead()
                if currentElement is not None:
                    children.append(currentElement)
                children.extend(self.getFeatureAsElementList(InternalFeature.COMPLEMENTS))
                children.extend(self.getFeatureAsElementList(InternalFeature.POSTMODIFIERS))
            elif category == PhraseCategory.VERB_PHRASE:
                children.extend(self.getFeatureAsElementList(InternalFeature.PREMODIFIERS))
                currentElement = self.getHead()
                if currentElement is not None:
                    children.append(currentElement)
                children.extend(self.getFeatureAsElementList(InternalFeature.COMPLEMENTS))
                children.extend(self.getFeatureAsElementList(InternalFeature.POSTMODIFIERS))
            elif category == PhraseCategory.CANNED_TEXT:
                pass # Do nothing
            else:
                children.extend(self.getFeatureAsElementList(InternalFeature.PREMODIFIERS))
                currentElement = self.getHead()
                if currentElement is not None:
                    children.append(currentElement)
                children.extend(self.getFeatureAsElementList(InternalFeature.COMPLEMENTS))
                children.extend(self.getFeatureAsElementList(InternalFeature.POSTMODIFIERS))
        return children

    # Sets the head, or main component, of this current phrase.
    def setHead(self, newHead):
        if newHead is None:
            self.removeFeature(InternalFeature.HEAD)
            return
        if isinstance(newHead, NLGElement):
            headElement = newHead
        else:
            headElement = StringElement(str(newHead))
        self.setFeature(InternalFeature.HEAD, headElement)

    # Retrieves the current head of this phrase.
    def getHead(self):
        return self.getFeatureAsElement(InternalFeature.HEAD)

    # Adds a new complement to the phrase element.
    def addComplement(self, newComplement):
        complements = self.getFeatureAsElementList(InternalFeature.COMPLEMENTS)
        if complements is None:
            complements = []
        if isinstance(newComplement, NLGElement):
            # check if the new complement has a discourse function; if not, assume object
            if not newComplement.hasFeature(InternalFeature.DISCOURSE_FUNCTION):
                newComplement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.OBJECT)
            complements.append(newComplement)
            self.setFeature(InternalFeature.COMPLEMENTS, complements)
            if newComplement.isA(PhraseCategory.CLAUSE) or isinstance(newComplement, CoordinatedPhraseElement):
                newComplement.setFeature(InternalFeature.CLAUSE_STATUS, ClauseStatus.SUBORDINATE)
                if not newComplement.hasFeature(InternalFeature.DISCOURSE_FUNCTION):
                    newComplement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.OBJECT)
        elif isinstance(newComplement, str):
            newElement = StringElement(newComplement)
            complements.append(newElement)
            self.setFeature(InternalFeature.COMPLEMENTS, complements)
        else:
            raise ValueError('Invalid newComplement type: ' + str(type(newComplement)))

    # Sets a complement of the phrase element.
    def setComplement(self, newComplement):
        if isinstance(newComplement, NLGElement):
            function = newComplement.getFeature(InternalFeature.DISCOURSE_FUNCTION)
            self.removeComplements(function)
            self.addComplement(newComplement)
        elif isinstance(newComplement, str):
            self.setFeature(InternalFeature.COMPLEMENTS, None)
            self.addComplement(newComplement)
        else:
            raise ValueError('Invalid newComplement type: ' + str(type(newComplement)))

    # remove complements of the specified DiscourseFunction
    def removeComplements(self, function):
        complements = self.getFeatureAsElementList(InternalFeature.COMPLEMENTS)
        if function is None or complements is None:
            return
        complementsToRemove = []
        for complement in complements:
            if function == complement.getFeature(InternalFeature.DISCOURSE_FUNCTION):
                complementsToRemove.append(complement)
        if complementsToRemove:
            for compl in complementsToRemove:
                complements.remove(compl)
            self.setFeature(InternalFeature.COMPLEMENTS, complements)

    # Adds a new post-modifier to the phrase element.
    def addPostModifier(self, newPostModifier):
        postModifiers = self.getFeatureAsElementList(InternalFeature.POSTMODIFIERS)
        if postModifiers is None:
            postModifiers = []
        if isinstance(newPostModifier, NLGElement):
            newPostModifier.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.POST_MODIFIER)
            postModifiers.append(newPostModifier)
            self.setFeature(InternalFeature.POSTMODIFIERS, postModifiers)
        elif isinstance(newPostModifier, str):
            postModifiers.append(StringElement(newPostModifier))
            self.setFeature(InternalFeature.POSTMODIFIERS, postModifiers)
        else:
            raise ValueError('Invalid newPostModifier type: ' + str(type(newPostModifier)))

    # Set the postmodifier for this phrase.
    def setPostModifier(self, newPostModifier):
        if isinstance(newPostModifier, str) or isinstance(newPostModifier, NLGElement):
            self.setFeature(InternalFeature.POSTMODIFIERS, None)
            self.addPostModifier(newPostModifier)
        else:
            raise ValueError('Invalid newPostModifier type: ' + str(type(newPostModifier)))

    # Adds a new front modifier to the phrase element.
    def addFrontModifier(self, newFrontModifier):
        frontModifiers = self.getFeatureAsElementList(InternalFeature.FRONT_MODIFIERS)
        if frontModifiers is None:
            frontModifiers = []
        if isinstance(newFrontModifier, NLGElement):
            frontModifiers.append(newFrontModifier)
            self.setFeature(InternalFeature.FRONT_MODIFIERS, frontModifiers)
        elif isinstance(newFrontModifier, str):
            frontModifiers.append(StringElement(newFrontModifier))
            self.setFeature(InternalFeature.FRONT_MODIFIERS, frontModifiers)
        else:
            raise ValueError('Invalid newFrontModifier type: ' + str(type(newFrontModifier)))

    # Set the frontmodifier for this phrase. T
    def setFrontModifier(self, newFrontModifier):
        self.setFeature(InternalFeature.FRONT_MODIFIERS, None)
        self.addFrontModifier(newFrontModifier)

    # Adds a new pre-modifier to the phrase element.
    def addPreModifier(self, newPreModifier):
        if isinstance(newPreModifier, str):
            newPreModifier = StringElement(newPreModifier)
        preModifiers = self.getFeatureAsElementList(InternalFeature.PREMODIFIERS)
        if preModifiers is None:
            preModifiers = []
        preModifiers.append(newPreModifier)
        self.setFeature(InternalFeature.PREMODIFIERS, preModifiers)

    # Set the premodifier for this phrase.
    def setPreModifier(self, newPreModifier):
        self.setFeature(InternalFeature.PREMODIFIERS, None)
        self.addPreModifier(newPreModifier)

    # Add a modifier to a phrase Use heuristics to decide where it goes
    def addModifier(self, modifier):
        # default addModifier - always make modifier a preModifier
        if modifier is None:
            return
        # assume is preModifier, add in appropriate form
        self.addPreModifier(modifier)

    # Retrieves the current list of pre-modifiers for the phrase.
    def getPreModifiers(self):
        return self.getFeatureAsElementList(InternalFeature.PREMODIFIERS)

    # Retrieves the current list of post modifiers for the phrase.
    def getPostModifiers(self):
        return self.getFeatureAsElementList(InternalFeature.POSTMODIFIERS)

    # Retrieves the current list of frony modifiers for the phrase.
    def getFrontModifiers(self):
        return self.getFeatureAsElementList(InternalFeature.FRONT_MODIFIERS)

    # @Override
    def printTree(self, indent=None):
        if indent is None:
            indent = ''
        thisIndent      = indent + " |-"
        childIndent     = indent + " | "
        lastIndent      = indent + " \\-"
        lastChildIndent = indent + "   "
        pstr = "PhraseElement: category=" + str(self.getCategory()) + ", features={"
        features = self.getAllFeatures()
        for feat, val in features.items():
            pstr += feat + '=' + str(val) + ', '
        pstr = pstr[:-2]
        pstr += "}\n"
        children = self.getChildren()
        for i, child in enumerate(children):
            if i<len(children)-1:
                pstr += thisIndent + child.printTree(childIndent)
            else:
                pstr += lastIndent + child.printTree(lastChildIndent)
        return pstr

    # Removes all existing complements on the phrase.
    def clearComplements(self):
        self.removeFeature(InternalFeature.COMPLEMENTS)

    # Sets the determiner for the phrase.
    # @Deprecated
    def setDeterminer(self, newDeterminer):
        from .NLGFactory  import NLGFactory     # prevent circular imports
        factory = NLGFactory()
        determinerElement = factory.createWord(newDeterminer, LexicalCategory.DETERMINER)
        if determinerElement is not None:
            determinerElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.SPECIFIER)
            self.setFeature(InternalFeature.SPECIFIER, determinerElement)
            determinerElement.setParent(self)
