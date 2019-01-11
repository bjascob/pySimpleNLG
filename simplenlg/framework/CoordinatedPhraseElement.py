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
from ..features.Feature             import *
from ..features.InternalFeature     import *
from ..features.NumberAgreement     import *
from .PhraseCategory                import *
from .StringElement                 import *


# This class defines coordination between two or more phrases.
class CoordinatedPhraseElement(NLGElement):
    PLURAL_COORDINATORS = ["and"]

    # Creates a blank coordinated phrase ready for new coordinates to be added.
    def __init__(self, coordinate1=None, coordinate2=None):
        super().__init__()
        if coordinate1 is None and coordinate2 is None:
            self.setFeature(Feature.CONJUNCTION, "and")
        else:
            self.addCoordinate(coordinate1)
            self.addCoordinate(coordinate2)
            self.setFeature(Feature.CONJUNCTION, "and")

    # Adds a new coordinate to this coordination.
    def addCoordinate(self, newCoordinate):
        coordinates = self.getFeatureAsElementList(InternalFeature.COORDINATES)
        if not coordinates:
            coordinates = []
            self.setFeature(InternalFeature.COORDINATES, coordinates)
        if isinstance(newCoordinate, NLGElement):
            if newCoordinate.isA(PhraseCategory.CLAUSE) and len(coordinates)>0:
                newCoordinate.setFeature(Feature.SUPRESSED_COMPLEMENTISER, True)
            coordinates.append(newCoordinate)
        elif isinstance(newCoordinate, str):
            coordElement = StringElement(newCoordinate)
            coordElement.setFeature(Feature.SUPRESSED_COMPLEMENTISER, True)
            coordinates.append(coordElement)
        self.setFeature(InternalFeature.COORDINATES, coordinates)

    # @Override
    def getChildren(self):
        return self.getFeatureAsElementList(InternalFeature.COORDINATES)

    # Clears the existing coordinates in this coordination. It performs exactly
    # the same as removeFeature(Feature.COORDINATES).
    def clearCoordinates(self):
        self.removeFeature(InternalFeature.COORDINATES)

    # Adds a new pre-modifier to the phrase element. Pre-modifiers will be
    # realised in the syntax before the coordinates.
    def addPreModifier(self, newPreModifier):
        preModifiers = self.getFeatureAsElementList(InternalFeature.PREMODIFIERS)
        if preModifiers is None:
            preModifiers = []
        if isinstance(newPreModifier, NLGElement):
            preModifiers.append(newPreModifier)
        elif isinstance(newPreModifier, str):
            preModifiers.append(StringElement(newPreModifier))
        else:
            raise ValueError('Invalid newPreModifier type: ' + str(type(newPreModifier)))
        self.setFeature(InternalFeature.PREMODIFIERS, preModifiers)

    # Retrieves the list of pre-modifiers currently associated with this
    # coordination.
    def getPreModifiers(self):
        return self.getFeatureAsElementList(InternalFeature.PREMODIFIERS)

    # Retrieves the list of complements currently associated with this
    # coordination.
    def getComplements(self):
        return self.getFeatureAsElementList(InternalFeature.COMPLEMENTS)

    # Adds a new post-modifier to the phrase element. Post-modifiers will be
    # realised in the syntax after the coordinates.
    def addPostModifier(self, newPostModifier):
        postModifiers = self.getFeatureAsElementList(InternalFeature.POSTMODIFIERS)
        if postModifiers is None:
            postModifiers = []
        if isinstance(newPostModifier, NLGElement):
            postModifiers.append(newPostModifier)
        elif isinstance(newPostModifier, str):
            postModifiers.append(StringElement(newPostModifier))
        else:
            raise ValueError('Invalid newPostModifier type: ' + str(type(newPostModifier)))
        self.setFeature(InternalFeature.POSTMODIFIERS, postModifiers)

    # Retrieves the list of post-modifiers currently associated with this
    # coordination.
    def getPostModifiers(self):
        return self.getFeatureAsElementList(InternalFeature.POSTMODIFIERS)

    # @Override
    def printTree(self, indent=None):
        if indent is None:
            indent = ''
        thisIndent      = indent + " |-"
        childIndent     = indent + " | "
        lastIndent      = indent + " \\-"
        lastChildIndent = indent + "   "
        pstr = "CoordinatedPhraseElement:\n"
        children = self.getChildren()
        for i, child in enumerate(children):
            if i < len(children)-1:
                pstr += thisIndent + child.printTree(childIndent)
            else:
                pstr += lastIndent + child.printTree(lastChildIndent)
        return pstr

    # Adds a new complement to the phrase element.
    def addComplement(self, newComplement):
        complements = self.getFeatureAsElementList(InternalFeature.COMPLEMENTS)
        if complements is None:
            complements = []
        if isinstance(newComplement, NLGElement):
            complements.append(newComplement)
        elif isinstance(newComplement, str):
            complements.append(StringElement(newComplement))
        else:
            raise ValueError('Invalid newComplement type: ' + str(type(newComplement)))
        self.setFeature(InternalFeature.COMPLEMENTS, complements)

    # A convenience method for retrieving the last coordinate in this
    # coordination.
    def getLastCoordinate(self):
        children = self.getChildren()
        if not children:
            return None
        return children[-1]

    # set the conjunction to be used in a coordinatedphraseelement
    # @param conjunction
    def setConjunction(self, conjunction):
        self.setFeature(Feature.CONJUNCTION, conjunction)

    # @return  conjunction used in coordinatedPhraseElement
    def getConjunction(self):
        return self.getFeatureAsString(Feature.CONJUNCTION)

    # @return true if this coordinate is plural in a syntactic sense
    def checkIfPlural(self):
        # doing this right is quite complex, take simple approach for now
        if len(self.getChildren()) == 1:
            return (NumberAgreement.PLURAL == self.getLastCoordinate().getFeature(Feature.NUMBER))
        else:
            return self.getConjunction() in self.PLURAL_COORDINATORS
