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
from ..lexicon.Lexicon  import *


# NLGModule is the base class that all processing modules extend
# from.
class NLGModule(ABC):
    def __init__(self):
        self.lexicon = None    #Lexicon

    # Performs one-time initialisation of the module.
    def initialise(self):
        assert False, 'Not implemented in base.'

    # Realises the given element.
    def realise(self, element):
        assert False, 'Not implemented in base.'

    # Sets the lexicon to be used by this module. Passing in null
    # will remove the existing lexicon and no lexicon will be used.
    def setLexicon(self, newLexicon):
        self.lexicon = newLexicon

    # Retrieves the lexicon currently being used by this module.
    def getLexicon(self):
        return self.lexicon
