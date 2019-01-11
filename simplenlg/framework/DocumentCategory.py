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

from enum import Enum

# This enumerated type defines the different types of components found
# in the structure of text.
class DocumentCategory(Enum):
    # Definition for a document.
    DOCUMENT = 0
    # Definition for a section within a document.
    SECTION = 1
    # Definition for a paragraph.
    PARAGRAPH = 2
    # Definition for a sentence.
    SENTENCE = 3
    # Definition for creating a list of items.
    LIST = 4
    # Definition for creating a list of enumerated items.
    ENUMERATED_LIST = 5
    # Definition for an item in a list.
    LIST_ITEM = 6

    # Checks to see if the given object is equal to this document category
    def equalTo(self, checkObject):
        match = False
        if checkObject is not None:
            if isinstance(checkObject, DocumentCategory):
                match = self==checkObject
            else:
                match = str(self.name).lower() == str(checkObject).lower()
        return match

    # This method determines if the supplied ElementCategory (ecat) forms an immediate
    # sub-part of DocumentCategory (dcat)
    def hasSubPart(self, ecat):
        if isinstance(ecat, DocumentCategory):
            if self == DocumentCategory.DOCUMENT:
                return not (ecat==DocumentCategory.DOCUMENT) and not (ecat==DocumentCategory.LIST_ITEM)
            elif self == DocumentCategory.SECTION:
                return ecat==DocumentCategory.PARAGRAPH or ecat==DocumentCategory.SECTION
            elif self == DocumentCategory.PARAGRAPH:
                return ecat==DocumentCategory.SENTENCE or ecat==DocumentCategory.LIST
            elif self == DocumentCategory.LIST:
                return ecat==DocumentCategory.LIST_ITEM
            elif self == DocumentCategory.ENUMERATED_LIST:
                return ecat==DocumentCategory.LIST_ITEM
        else:
            return self==DocumentCategory.SENTENCE or self==DocumentCategory.LIST_ITEM
        return False
