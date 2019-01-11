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

from abc import ABC
from ..features.Feature             import *
from ..features.NumberAgreement     import *
from ..features.Tense               import *


# NLGElement is the base class that all elements extend from.
class NLGElement(ABC):
    def __init__(self):
        self.category    = None    # ElementCategory
        self.features    = {}      # {string, object}
        self.parent      = None    # NLGElement
        self.realisation = None    # string
        self.factory     = None    # NLGFactory

    # Sets the category of this element.
    def setCategory(self, new_category):
        self.category = new_category

    # Retrieves the category for this element.
    def getCategory(self):
        return self.category

    # Adds a feature to the feature map.
    def setFeature(self, featureName, featureValue):
        if not featureName:
            return
        if featureValue is None:
            if featureName in self.features:
                del self.features[featureName]
        else:
            self.features[featureName] = featureValue

    # Retrieves the value of the feature.
    def getFeature(self, featureName):
        return self.features.get(featureName, None)

    # Retrieves the value of the feature as a string. If the feature doesn't
    # exist then null is returned.
    def getFeatureAsString(self, featureName):
        return self.getFeature(featureName)

    # Retrieves the value of the feature as a list of elements.
    def getFeatureAsElementList(self, featureName):
        value = self.getFeature(featureName)
        if isinstance(value, NLGElement):
            return [value]
        elif isinstance(value, list):
            elist = []
            for item in value:
                if isinstance(item, NLGElement):
                    elist.append(item)
            return elist
        return []

    # Retrieves the value of the feature as a list of java objects. If the feature
    def getFeatureAsList(self, featureName):
        value = self.getFeature(featureName)
        if isinstance(value, list):
            return value
        return [value]

    # Retrieves the value of the feature as a list of strings.
    def getFeatureAsStringList(self, featureName):
        value = self.getFeature(featureName)
        if value is None:
            return []
        elif isinstance(value, list):
            values = []
            for item in value:
                values.append(str(item))
            return values
        return [str(value)]

    # Retrieves the value of the feature as an Integer.
    def getFeatureAsInteger(self, featureName):
        value = self.getFeature(featureName)
        if isinstance(value, int):
            return value
        elif isinstance(value, float):
            return int(value)
        elif isinstance(value, str):
            try:
                val = int(str)
                return val
            except ValueError:
                return None

    # Retrieves the value of the feature as a Long.
    def getFeatureAsLong(self, featureName):
        return self.getFeatureAsInteger(featureName)

    # Retrieves the value of the feature as a Float.
    def getFeatureAsFloat(self, featureName):
        value = self.getFeature(featureName)
        if isinstance(value, float):
            return value
        elif isinstance(value, int):
            return float(value)
        elif isinstance(value, str):
            try:
                val = float(str)
                return val
            except ValueError:
                return None

    # Retrieves the value of the feature as a Double.
    def getFeatureAsDouble(self, featureName):
        return self.getFeatureAsFloat(featureName)

    # Retrieves the value of the feature as a Boolean.
    def getFeatureAsBoolean(self, featureName):
        value = self.getFeature(featureName)
        if isinstance(value, bool):
            return value
        return False

    # Retrieves the value of the feature as a NLGElement.
    def getFeatureAsElement(self, featureName):
        value = self.getFeature(featureName)
        if isinstance(value, NLGElement):
            return value
        elif isinstance(value, str):
            from .StringElement import StringElement    #prevent circular import
            return StringElement(value)
        return None

    # Retrieves the map containing all the features for this element.
    def getAllFeatures(self):
        return self.features

    # Checks the feature map to see if the named feature is present in the map.
    def hasFeature(self, featureName):
        return featureName in self.features

    # Deletes the named feature from the map.
    def removeFeature(self, featureName):
        if featureName in self.features:
            del self.features[featureName]

    # Deletes all the features in the map.
    def clearAllFeatures(self):
        self.features = {}

    # Sets the parent element of this element.
    def setParent(self, new_parent):
        self.parent = new_parent

    # Retrieves the parent of this element.
    def getParent(self):
        return self.parent

    # Sets the realisation of this element.
    def setRealisation(self, realised):
        self.realisation = realised

    # Retrieves the final realisation of this element.
    def getRealisation(self):
        start = 0
        end   = 0
        if self.realisation is not None:
            end = len(self.realisation)
            while start<len(self.realisation) and ' '==self.realisation[start]:
                start += 1
            if start == len(self.realisation):
                self.realisation = None
            else:
                while end>0 and ' '==self.realisation[end - 1]:
                    end -= 1
        # AG: changed this to return the empty string if the realisation is null
        # avoids spurious nulls appearing in output for empty phrases
        if self.realisation is None:
            return ''
        return self.realisation[start:end]

    def __str__(self):
        buffer = '{realisation='
        if self.realisation is not None:
            buffer += '"' + self.realisation + '"'
        else:
            buffer += '""'
        if self.category is not None:
            buffer += ", category=" + str(self.category)
        if self.features is not None:
            buffer += ", features={"
            for key, value in self.features.items():
                buffer += '%s:%s, ' % (key, str(value))
            buffer = buffer[:-2]
            buffer += '}'
        buffer += '}'
        return buffer

    # This makes the xxPhraseSpec(s) print correctly.  They inherit from PhraseSpec
    # which inherits from NLGElement.
    def __repr__(self):
        return self.__str__()

    def isA(self, checkCategory):
        if self.category is not None:
            return self.category.equalTo(checkCategory)
        elif checkCategory is None:
            return True

    # Retrieves the children for this element. This method needs to be
    # overridden for each specific type of element. Each type of element will
    # have its own way of determining the child elements.
    # return list of NGElement
    def getChildren(self):
        assert False, 'Not implemented in base.'

    # Retrieves the set of features currently contained in the feature map.
    def getAllFeatureNames(self):
        return self.features.keys()

    def printTree(self, indent=None):
        if indent is None:
            indent = ''
        this_indent  = indent + " |-"
        child_indent = indent + " |-"
        pstr = "NLGElement: " + str(self) + '\n'
        for child in self.getChildren():
            pstr += this_indent + child.printTree(child_indent)
        return pstr

    # Sets the number agreement on this element.
    def setPlural(self, isPlural):
        if isPlural:
            self.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
        else:
            self.setFeature(Feature.NUMBER, NumberAgreement.SINGULAR)

    # Determines if this element is to be treated as a plural. This is a
    # convenience method and not all element types make use of number
    # agreement.
    def isPlural(self):
        return NumberAgreement.PLURAL == self.getFeature(Feature.NUMBER)

    # Retrieves the tense for this element.
    def getTense(self):   # deprecated
        value = self.getFeature(Feature.TENSE)
        if isinstance(value, Tense):
            return value
        return Tense.PRESENT

    # Sets the tense on this element.
    def setTense(self, new_tense):
        self.setFeature(Feature.TENSE, new_tense)

    # Sets the negation on this element.
    def setNegated(self, is_negated):      # deprecated
        self.setFeature(Feature.NEGATED, is_negated)

    # Determines if this element is to be treated as a negation.
    def isNegated(self):    # deprecated
        return self.getFeature(Feature.NEGATED)

    # @return the NLG factory
    def getFactory(self):
        return self.factory

    # @param factory
    def setFactory(self, factory):
        self.factory = factory

    # An NLG element is equal to some object if the object is an NLGElement,
    # they have the same category and the same features.
    def __eq__(self, obj):
        if isinstance(obj, str):
            if obj is None and self.realisation is None:
                return True
            else:
                return obj == self.realisation
        elif isinstance(obj, NLGElement):
            return self.category == obj.category and self.features == obj.features
        return False

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        objects = []
        if self.features:
            objects.extend(self.features)
        if self.category:
            objects.append(self.category)
        return hash(tuple(objects))
