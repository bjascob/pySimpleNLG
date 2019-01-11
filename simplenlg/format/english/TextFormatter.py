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

from ...framework.CoordinatedPhraseElement   import *
from ...framework.DocumentCategory           import *
from ...framework.DocumentElement            import *
from ...framework.ListElement                import *
from ...framework.NLGElement                 import *
from ...framework.NLGModule                  import *
from ...framework.StringElement              import *
from .NumberedPrefix                         import *

# This processing module adds some simple plain text formatting to the
# SimpleNLG output.
class TextFormatter(NLGModule):
    def __init__(self):
        super().__init__()
        self.numberedPrefix = NumberedPrefix()

    # @Override
    def initialise(self):
        pass # Do nothing

    # @Override
    def realise(self, element):
        if isinstance(element, NLGElement):
            return self._realiseElement(element)
        elif isinstance(element, list):
            return [self._realiseElement(eachElement) for eachElement in element]
        else:
            raise ValueError('Invalid element type: ' + str(type(element)))

    # @Override
    def _realiseElement(self, element):
        realisation = ''
        category = element.getCategory()
        components = element.getChildren()
        #NB: The order of the if-statements below is important!
        # check if this is a canned text first
        if isinstance(element, StringElement):
            realisation += element.getRealisation()
        elif isinstance(category, DocumentCategory):
            title = None
            if isinstance(element, DocumentElement):
                title = element.getTitle()
            if category == DocumentCategory.DOCUMENT:
                realisation = self.appendTitle(realisation, title, 2)
                realisation = self.realiseSubComponents(realisation, components)
            elif category == DocumentCategory.SECTION:
                realisation = self.appendTitle(realisation, title, 1)
                realisation = self.realiseSubComponents(realisation, components)
            elif category == DocumentCategory.LIST:
                realisation = self.realiseSubComponents(realisation, components)
            elif category == DocumentCategory.ENUMERATED_LIST:
                self.numberedPrefix.upALevel()
                if title is not None:
                    realisation += title + '\n'
                if components:
                    realisedComponent = self.realise(components[0])
                    if realisedComponent is not None:
                        realisation += realisedComponent.getRealisation()
                    for i, component in enumerate(components):
                        if i==0: continue
                        if realisedComponent is not None and not realisedComponent.getRealisation().endswith("\n"):
                            realisation += ' '
                        if component.getParent().getCategory() == DocumentCategory.ENUMERATED_LIST:
                            self.numberedPrefix.increment()
                        realisedComponent = self.realise(component)
                        if realisedComponent is not None:
                            realisation += realisedComponent.getRealisation()
                self.numberedPrefix.downALevel()
            elif category == DocumentCategory.PARAGRAPH:
                if components:
                    realisedComponent = self.realise(components[0])
                    if realisedComponent is not None:
                        realisation += realisedComponent.getRealisation()
                    for i, component in enumerate(components):
                        if i==0: continue
                        if realisedComponent is not None:
                            realisation += ' '
                        realisedComponent = self.realise(component)
                        if realisedComponent is not None:
                            realisation += realisedComponent.getRealisation()
                realisation += "\n\n"
            elif category == DocumentCategory.SENTENCE:
                realisation += element.getRealisation()
            elif category == DocumentCategory.LIST_ITEM:
                if element.getParent() is not None:
                    if element.getParent().getCategory() == DocumentCategory.LIST:
                        realisation += " * "
                    elif element.getParent().getCategory() == DocumentCategory.ENUMERATED_LIST:
                        realisation += self.numberedPrefix.getPrefix() + " - "
                for eachComponent in components:
                    realisedComponent = self.realise(eachComponent)
                    if realisedComponent is not None:
                        realisation += realisedComponent.getRealisation()
                        if components.index(eachComponent) < len(components)-1:
                            realisation += ' '
                #finally, append newline
                realisation += "\n"
            # also need to check if element is a ListElement (items can
            # have embedded lists post-orthography) or a coordinate
        elif isinstance(element, ListElement) or isinstance(element, CoordinatedPhraseElement):
            for eachComponent in components:
                realisedComponent = self.realise(eachComponent)
                if realisedComponent is not None:
                    realisation += realisedComponent.getRealisation() + ' '
        return StringElement(realisation)

    # realiseSubComponents -- Realises subcomponents iteratively.
    def realiseSubComponents(self, realisation, components):
        for eachComponent in components:
            realisedComponent = self.realise(eachComponent)
            if realisedComponent is not None:
                realisation += realisedComponent.getRealisation()
        return realisation

    # appendTitle -- Appends document or section title to the realised document.
    def appendTitle(self, realisation, title, numberOfLineBreaksAfterTitle):
        if title:
            realisation += title
            for _ in range(numberOfLineBreaksAfterTitle):
                realisation += "\n"
        return realisation
