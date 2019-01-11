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

from .NLGElement        import *
from .PhraseCategory    import *
from ..features.Feature import *


# This class defines an element for representing canned text within the
# SimpleNLG library. Once assigned a value, the string element should not be
# changed by any other processors.
class StringElement(NLGElement):
    def __init__(self, value):
        super().__init__()
        self.setCategory(PhraseCategory.CANNED_TEXT)
        self.setFeature(Feature.ELIDED, False)
        self.setRealisation(value)

    # The string element contains no children so this method will always return
    # an empty list.
    # @Override
    def getChildren(self):
        return []

    #@Override
    def __str__(self):
        return self.getRealisation()

    # @see simplenlg.framework.NLGElement#equals(java.lang.Object)
    # @Override
    def __eq__(self, obj):
        return super()==obj and isinstance(obj, StringElement) and self.realisationsMatch(obj)
    def _ne__(self, obj):
        return not self.__eq__(obj)
    def __hash__(self):
        return hash( super() )

    def realisationsMatch(self, obj):
        if  self.getRealisation() == None:
            return obj.getRealisation() == None
        else:
            return self.getRealisation() == obj.getRealisation()

    # @Override
    def printTree(self, indent=None):
        pstr = "StringElement: content=\"" + self.getRealisation() + '\"'
        features = self.getAllFeatures()
        if features is not None:
            pstr += ", features=" + str(features)
        pstr += '\n'
        return pstr
