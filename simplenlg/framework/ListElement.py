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
from ..features.InternalFeature import *


# ListElement is used to define elements that can be grouped
# together and treated in a similar manner.
class ListElement(NLGElement):
    def __init__(self, component=None):
        super().__init__()
        if component is None:
            return
        elif isinstance(component, list):
            self.addComponents(component)
        elif isinstance(component, NLGElement):
            self.addComponent(component)
        else:
            raise ValueError('Invalid component type: ' + str(type(component)))

    # @Override
    def getChildren(self):
        return self.getFeatureAsElementList(InternalFeature.COMPONENTS)

    # Adds the given component to the list element.
    def addComponent(self, newComponent):
        components = self.getFeatureAsElementList(InternalFeature.COMPONENTS)
        if components is None:
            components = []
        self.setFeature(InternalFeature.COMPONENTS, components)
        components.append(newComponent)

    # Adds the given components to the list element.
    def addComponents(self, newComponents):
        components = self.getFeatureAsElementList(InternalFeature.COMPONENTS)
        if components is None:
            components = []
        self.setFeature(InternalFeature.COMPONENTS, components)
        components.extend(newComponents)

    # Replaces the current components in the list element with the given list.
    def setComponents(self, newComponents):
        self.setFeature(InternalFeature.COMPONENTS, newComponents)

    # @Override
    def __str__(self):
        pstr = '['
        for child in self.getChildren():
            pstr += str(child) + ', '
        pstr = pstr[:-2] + ']'
        return pstr

    # @Override
    def printTree(self, indent=None):
        if indent is None:
            indent = ''
        thisIndent      = indent + " |-"
        childIndent     = indent + " | "
        lastIndent      =  indent + " \\-"
        lastChildIndent = indent + "   "
        pstr = "ListElement: features={"
        features = self.getAllFeatures()
        for feat, val in features.items():
            pstr += feat + '=' + str(val) + ' '
        pstr += "}\n"
        children = self.getChildren()
        for i, child in enumerate(children):
            if i<len(children)-1:
                pstr += thisIndent + child.printTree(childIndent)
            else:
                pstr += lastIndent + child.printTree(lastChildIndent)
        return pstr

    # Retrieves the number of components in this list element.
    # @return the number of components.
    def __len__(self):
        return len(self.getChildren())

    # Retrieves the first component in the list.
    # @return the NLGElement at the top of the list.
    def getFirst(self):
        children = self.getChildren()
        if not children:
            return None
        return children[0]
