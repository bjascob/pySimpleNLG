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

# This enumeration defines the different syntactical phrases.
class PhraseCategory(Enum):
    # A grammatical clause, the simplest form of which consists of a subject
    # (noun or noun phrase) and a verb (or verb phrase).
    CLAUSE = 0
    # A phrase relating to an adjective.
    ADJECTIVE_PHRASE = 1
    # A phrase relating to an adverb.
    ADVERB_PHRASE = 2
    # A phrase relating to a noun.
    NOUN_PHRASE = 3
    # A phrase relating to a preposition.
    PREPOSITIONAL_PHRASE = 4
    # A phrase relating to a verb.
    VERB_PHRASE = 5
    # A phrase relating to a pre-formed string that is not altered in anyway.#/
    CANNED_TEXT = 6

    # Checks to see if the given object is equal to this document category
    def equalTo(self, checkObject):
        match = False
        if checkObject is not None:
            if isinstance(checkObject, PhraseCategory):
                match = self==checkObject
            else:
                match = str(self.name).lower() == str(checkObject).lower()
        return match

    def __str__(self):
        return self.name
