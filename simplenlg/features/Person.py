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

# This is an enumeration used to represent the point of view of the narrative.
class Person(Enum):
    # The enumeration to show that the narration is written in the first
    # person. First person narrative uses the personal pronouns of I
    # and we.
    FIRST = 0
    # The enumeration to show that the narration is written in the second
    # person. Second person narrative uses the personal pronoun of you.
    SECOND = 1
    # The enumeration to show that the narration is written in the third
    # person. Third person narrative uses the personal pronouns of he,
    # her and they.
    THIRD = 2

    def __str__(self):
        return self.name
