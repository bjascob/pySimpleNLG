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

from .DocumentCategory  import *
from .NLGElement        import *

# DocumentElement is a convenient extension of the base NLGElement class.
class DocumentElement(NLGElement):
    FEATURE_TITLE       = "textTitle"
    FEATURE_COMPONENTS  = "textComponents"

    def __init__(self, category=None, textTitle=None):
        super().__init__()
        if category is not None:
            self.setCategory(category)
        if textTitle is not None:
            self.setTitle(textTitle)

    # Sets the title of this element. Titles are specifically used with
    # documents (the document name) and sections (headings).
    def setTitle(self, textTitle):
        self.setFeature(self.FEATURE_TITLE, textTitle)

    # Retrieves the title of this element.
    def getTitle(self):
        return self.getFeatureAsString(self.FEATURE_TITLE)

    # Retrieves the child components of this element.
    def getComponents(self):
        return self.getFeatureAsElementList(self.FEATURE_COMPONENTS)

    # Add a single child component to the current list of child components. If
    # there are no existing child components a new list is created.
    def addComponent(self, element):
        if element is None:
            return
        thisCategory = self.getCategory()
        category = element.getCategory()
        if category is not None and isinstance(thisCategory, DocumentCategory):
            if thisCategory.hasSubPart(category):
                self.addElementToComponents(element)
            else:
                promotedElement = self.promote(element)
                if promotedElement is not None:
                    self.addElementToComponents(promotedElement)
                else: # error condition - add original element so something is visible
                    self.addElementToComponents(element)
        else:
            self.addElementToComponents(element)

    # add an element to a components list
    def addElementToComponents(self, element):
        components = self.getComponents()
        components.append(element)
        element.setParent(self)
        self.setComponents(components)

    # promote an NLGElement so that it is at the right level to be added to a DocumentElement/
    # Promotion means adding surrounding nodes at higher doc levels
    def promote(self, element):
        # check if promotion needed
        if self.getCategory().hasSubPart(element.getCategory()):
            return element
        # if element is not a DocumentElement, embed it in a sentence and recurse
        if not isinstance(element, DocumentElement):
            sentence = DocumentElement(DocumentCategory.SENTENCE, None)
            sentence.addElementToComponents(element)
            return self.promote(sentence)
        # if element is a Sentence, promote it to a paragraph
        if element.getCategory() == DocumentCategory.SENTENCE:
            paragraph = DocumentElement(DocumentCategory.PARAGRAPH, None)
            paragraph.addElementToComponents(element)
            return self.promote(paragraph)
        return None

    # Adds a collection of NLGElements to the list of child
    # components. If there are no existing child components, then a new list is
    # created.
    def addComponents(self, textComponents):
        if textComponents is None:
            return
        thisCategory = self.getCategory()
        elementsToAdd = []
        category = None
        for eachElement in textComponents:
            if isinstance(eachElement, NLGElement):
                category = eachElement.getCategory()
                if category is not None and isinstance(thisCategory, DocumentCategory):
                    if thisCategory.hasSubPart(category):
                        elementsToAdd.append(eachElement)
                        eachElement.setParent(self)
        if len(elementsToAdd)> 0:
            components = self.getComponents()
            if components is None:
                components = []
            components.extend(elementsToAdd)
            self.setFeature(self.FEATURE_COMPONENTS, components)

    # Removes the specified component from the list of child components.
    def removeComponent(self, textComponent):
        components = self.getComponents()
        if components:
            if textComponent in components:
                components.remove(textComponent)
                return True
        return False

    # Removes all the child components from this element.
    def clearComponents(self):
        components = self.getComponents()
        if components is not None:
            components.clear()

    # Child elements of a DocumentElement are the components.
    # @Override
    def getChildren(self):
        return self.getComponents()

    # Replaces the existing components with the supplied list of components.
    # This is identical to calling:
    def setComponents(self, components):
        self.setFeature(self.FEATURE_COMPONENTS, components)

    # @Override
    def printTree(self, indent=None):
        if indent is None:
            indent = ''
        thisIndent      = indent + " |-"
        childIndent     = indent + " | "
        lastIndent      = indent + " \\-"
        lastChildIndent = indent + "   "
        pstr = "DocumentElement: category=" + str(self.getCategory())
        realisation = self.getRealisation()
        if realisation:
            pstr += " realisation=" + realisation
        pstr += '\n'
        children = self.getChildren()
        for i, child in enumerate(children):
            if i < len(children)-1:
                pstr += thisIndent + child.printTree(childIndent)
            else:
                pstr += lastIndent + child.printTree(lastChildIndent)
        return pstr
