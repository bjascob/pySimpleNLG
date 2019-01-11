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
from ...features.DiscourseFunction          import *
from ...features.Feature                    import *
from ...features.InternalFeature            import *
from ...framework.CoordinatedPhraseElement  import *
from ...framework.DocumentCategory          import *
from ...framework.DocumentElement           import *
from ...framework.ListElement               import *
from ...framework.NLGElement                import *
from ...framework.NLGModule                 import *
from ...framework.StringElement             import *


# This processing module deals with punctuation when applied to
# DocumentElements.
class OrthographyProcessor(NLGModule):
    def __init__(self):
        super().__init__()
        self.commaSepPremodifiers = None # set whether to separate premodifiers using commas
        self.commaSepCuephrase    = None # set whether to include a comma after a cue

    # @Override
    def initialise(self):
        self.commaSepPremodifiers = True
        self.commaSepCuephrase    = False

    # Check whether this processor separates premodifiers using a comma.
    def isCommaSepPremodifiers(self):
        return self.commaSepPremodifiers

    # Set whether to separate premodifiers using a comma. I
    def setCommaSepPremodifiers(self, commaSepPremodifiers):
        self.commaSepPremodifiers = commaSepPremodifiers

    # Check whether this processor separates cue phrases from a matrix phrase
    # using a comma.
    def isCommaSepCuephrase(self):
        return self.commaSepCuephrase

    # If set to true, separates a cue phrase from the matrix
    # phrase using a comma.
    def setCommaSepCuephrase(self, commaSepCuephrase):
        self.commaSepCuephrase = commaSepCuephrase

    # @Override
    def realise(self, element):
        if isinstance(element, NLGElement):
            return self._realiseElement(element)
        elif isinstance(element, list):
            return self._realiseElementList(element)
        else:
            raise ValueError('Invalid element type: ' + str(type(element)))

    def _realiseElement(self, element):
        realisedElement = None
        function = None #the element's discourse function
        #get the element's function first
        if isinstance(element, ListElement):
            children = element.getChildren()
            if children:
                firstChild = children[0]
                function = firstChild.getFeature(InternalFeature.DISCOURSE_FUNCTION)
        elif element is not None:
            function = element.getFeature(InternalFeature.DISCOURSE_FUNCTION)
        if element is not None:
            category = element.getCategory()
            if isinstance(category, DocumentCategory) and isinstance(element, DocumentElement):
                components = element.getComponents()
                if category == DocumentCategory.SENTENCE:
                    realisedElement = self.realiseSentence(components, element)
                if category == DocumentCategory.LIST_ITEM:
                    if components:
                        # recursively realise whatever is in the list item
                        # NB: this will realise embedded lists within list items
                        realisedElement = ListElement(self.realise(components))
                        realisedElement.setParent(element.getParent())
                else:
                    element.setComponents(self.realise(components))
                    realisedElement = element
            elif isinstance(element, ListElement):
                # AG: changes here: if we have a premodifier, then we ask the
                # realiseList method to separate with a comma.
                # if it's a postmod, we need commas at the start and end only
                # if it's appositive
                buffer = ''
                if DiscourseFunction.PRE_MODIFIER == function:
                    all_appositives = True
                    for child in element.getChildren():
                        all_appositives = all_appositives and child.getFeatureAsBoolean(Feature.APPOSITIVE)
                    if all_appositives:
                        buffer += ", "
                    sep = "," if self.commaSepPremodifiers else ''
                    buffer = self.realiseList(buffer, element.getChildren(), sep)
                    if all_appositives:
                        buffer += ", "
                elif DiscourseFunction.POST_MODIFIER == function:
                    postmods = element.getChildren()
                    # bug fix due to Owen Bennett
                    length = len(postmods)
                    for i in range(length):
                        postmod = postmods[i]
                        # if the postmod is appositive, it's sandwiched in commas
                        if postmod.getFeatureAsBoolean(Feature.APPOSITIVE):
                            buffer += ", "
                            buffer += str(self._realiseElement(postmod))
                            if i < length-1:
                                buffer += ", "
                        else:
                            buffer += str(self._realiseElement(postmod))
                            if isinstance(postmod, ListElement) or \
                               (postmod.getRealisation() is not None and not postmod.getRealisation()==""):
                                buffer  += " "
                elif (DiscourseFunction.CUE_PHRASE==function or DiscourseFunction.FRONT_MODIFIER==function) and \
                    self.commaSepCuephrase:
                    sep = ',' if self.commaSepCuephrase else ''
                    buffer = self.realiseList(buffer, element.getChildren(), sep)
                else:
                    buffer = self.realiseList(buffer, element.getChildren(), "")
                realisedElement = StringElement(buffer)
            elif isinstance(element, CoordinatedPhraseElement):
                realisedElement = self.realiseCoordinatedPhrase(element.getChildren())
            else:
                realisedElement = element
            # make the realised element inherit the original category
            # essential if list items are to be properly formatted later
            if realisedElement is not None:
                realisedElement.setCategory(category)
            #check if this is a cue phrase; if param is set, postfix a comma
            if (DiscourseFunction.CUE_PHRASE==function or DiscourseFunction.FRONT_MODIFIER==function) and \
                    self.commaSepCuephrase:
                realisation = realisedElement.getRealisation()
                if not realisation.endswith(","):
                    realisation = realisation + ","
                realisedElement.setRealisation(realisation)
        #remove preceding and trailing whitespace from internal punctuation
        self.removePunctSpace(realisedElement)
        return realisedElement

    # removes extra spaces preceding punctuation from a realised element
    def removePunctSpace(self, realisedElement):
        if realisedElement is not None:
            realisation = realisedElement.getRealisation()
            if realisation is not None:
                realisation = re.sub(" ,", ",",  realisation)
                realisation = re.sub(",,+", ",", realisation)
                realisedElement.setRealisation(realisation)

    # Performs the realisation on a sentence. This includes adding the
    # terminator and capitalising the first letter.
    def realiseSentence(self, components, element):
        realisedElement = None
        if components:
            realisation = ''
            realisation = self.realiseList(realisation, components, "")
            realisation = self.stripLeadingCommas(realisation)
            realisation = self.capitaliseFirstLetter(realisation)
            realisation = self.terminateSentence(realisation, element.getFeatureAsBoolean(InternalFeature.INTERROGATIVE))
            element.clearComponents()
            element.setRealisation(realisation)
            realisedElement = element
        return realisedElement

    # Adds the sentence terminator to the sentence. This is a period ('.') for
    # normal sentences or a question mark ('?') for interrogatives.
    def terminateSentence(self, realisation, interrogative):
        character = realisation[-1]
        if character != '.' and character != '?':
            if interrogative:
                realisation += '?'
            else:
                realisation += '.'
        return realisation

    # Remove recursively any leading spaces or commas at the start
    # of a sentence.
    def stripLeadingCommas(self, realisation):
        character = realisation[0]
        if character == ' ' or character == ',':
            realisation =  realisation[1:]
            realisation = self.stripLeadingCommas(realisation)
        return realisation

    # Capitalises the first character of a sentence if it is a lower case letter.
    def capitaliseFirstLetter(self, realisation):
        character = realisation[0]
        if character.islower():
            realisation = realisation[0].upper() + realisation[1:]
        return realisation

    # @Override
    def _realiseElementList(self, elements):
        realisedList = []
        if elements:
            for eachElement in elements:
                if isinstance(eachElement, DocumentElement):
                    realisedList.append(self.realise(eachElement))
                else:
                    realisedList.append(eachElement)
        return realisedList

    # Realises a list of elements appending the result to the on-going
    # realisation.
    def realiseList(self, realisation, components, listSeparator):
        realisedChild = None
        for i, thisElement in enumerate(components):
            realisedChild = self.realise(thisElement)
            childRealisation = realisedChild.getRealisation()
            # check that the child realisation is non-empty
            if childRealisation and not re.fullmatch(r"^[\s\n]+$", childRealisation):
                realisation += realisedChild.getRealisation()
                if len(components)>1 and i<len(components)-1:
                    realisation += listSeparator
                realisation += ' '
        if len(realisation) > 0:
            realisation = realisation[:-1]
        return realisation

    # Realises coordinated phrases.
    def realiseCoordinatedPhrase(self, components):
        realisation = ''
        realisedChild = None
        length = len(components)
        for index in range(length):
            realisedChild = components[index]
            if index < length - 2 and \
                    DiscourseFunction.CONJUNCTION==realisedChild.getFeature(InternalFeature.DISCOURSE_FUNCTION):
                realisation += ", "
            else:
                realisedChild = self.realise(realisedChild)
                realisation += realisedChild.getRealisation() + ' '
        realisation = realisation[:-1]
        realisation = realisation.replace(" ,", ",")
        return StringElement(realisation)
