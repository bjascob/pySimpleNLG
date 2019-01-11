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

# An enumeration representing the different types of number agreement.
class NumberAgreement(Enum):
    # This represents words that have the same form regardless of whether they
    # are singular or plural.
    BOTH = 0
    # This represents verbs and nouns that are written in the plural.
    PLURAL = 1
    # This represents verbs and nouns that are written in the singular. Fo
    SINGULAR  = 2

    def __str__(self):
        return self.name
