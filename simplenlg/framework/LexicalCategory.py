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

# This enumeration defines the different lexical components.
class LexicalCategory(Enum):
    ANY             =  0    # A default value, indicating an unspecified category.
    SYMBOL          =  1    # The element represents a symbol.
    NOUN            =  2    # A noun element.
    ADJECTIVE       =  3    # An adjective element.
    ADVERB          =  4    # An adverb element.
    VERB            =  5    # A verb element.
    DETERMINER      =  6    # A determiner element often referred to as a specifier.
    PRONOUN         =  7    # A pronoun element.
    CONJUNCTION     =  8    # A conjunction element.
    PREPOSITION     =  9    # A preposition element.
    COMPLEMENTISER  = 10    # A complementiser element.
    MODAL           = 11    #  A modal element.
    AUXILIARY       = 12    # An auxiliary verb element.

    # Checks to see if the given object is equal to this document category
    def equalTo(self, checkObject):
        match = False
        if checkObject is not None:
            if isinstance(checkObject, LexicalCategory):
                match = self==checkObject
            else:
                match = str(self.name).lower() == str(checkObject).lower()
        return match

    def __str__(self):
        return self.name
