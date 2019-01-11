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

# An enumeration representing the different types of morphology patterns used
# by the basic morphology processor included with SimpleNLG.
class Inflection(Enum):
    # The morphology processor has simple rules for pluralising Greek and Latin
    # nouns. The full list can be found in the explanation of the morphology
    # processor.
    GRECO_LATIN_REGULAR = 0
    # A word having an irregular pattern essentially means that none of the
    # supplied rules can be used to correctly inflect the word. The inflection
    # should be defined by the user or appear in the lexicon. sheep is
    #an example of an irregular noun.
    IRREGULAR = 1
    # Regular patterns represent the default rules when dealing with
    # inflections. A full list can be found in the explanation of the
    # morphology processor. An example would be adding -s to the end
    # of regular nouns to pluralise them.
    REGULAR = 2
    # Regular double patterns apply to verbs where the last consonant is
    # duplicated before applying the new suffix. For example, the verb
    # tag has a regular double pattern as its inflected forms include
    # tagged and tagging.
    REGULAR_DOUBLE = 3
    # The value for uncountable nouns, which are not inflected in their plural
    # form.
    UNCOUNT = 4
    # The value for words which are invariant, that is, are never inflected.
    INVARIANT = 5

    # convenience method: parses an inflectional code such as
    # "irreg|woman|women" to retrieve the first element, which is the code
    # itself, then maps it to the value of Inflection.
    @staticmethod
    def getInflCode(code):
        code = code.lower().strip()
        infl = None
        if code == "reg":
            infl = Inflection.REGULAR
        elif code == "irreg":
            infl = Inflection.IRREGULAR
        elif code == "regd":
            infl = Inflection.REGULAR_DOUBLE
        elif code == "glreg":
            infl = Inflection.GRECO_LATIN_REGULAR
        elif code in ["uncount", "noncount", "groupuncount"]:
            infl = Inflection.UNCOUNT
        elif code == "inv":
            infl = Inflection.INVARIANT
        return infl

    def __str__(self):
        return self.name
