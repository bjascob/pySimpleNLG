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

import re

# This class is used to parse numbers that are passed as figures, to determine
# whether they should take "a" or "an" as determiner.
class DeterminerAgrHelper(object):
    # An array of strings which are exceptions to the rule that "an" comes
    # before vowels
    AN_EXCEPTIONS = [ r"one", r"180", r"110" ]
    # Start of string involving vowels, for use of "an"
    AN_AGREEMENT = r"\A(a|e|i|o|u).*"

    # Check whether this string starts with a number that needs "an" (e.g.
    # "an 18% increase")
    @classmethod
    def requiresAn(cls, string):
        req = False
        lowercaseInput = string.lower()
        if re.fullmatch(cls.AN_AGREEMENT,lowercaseInput) and not cls.isAnException(lowercaseInput):
            req = True
        else:
            numPref = cls.getNumericPrefix(lowercaseInput)
            if numPref and re.fullmatch(r"^(8|11|18).*$", numPref):
                num = int(numPref)
                req = cls.checkNum(num)
        return req

    # check whether a string beginning with a vowel is an exception and doesn't
    # take "an" (e.g. "a one percent change")
    @classmethod
    def isAnException(cls, string):
        for ex in cls.AN_EXCEPTIONS:
            if re.fullmatch(r"^" + ex + r".*", string):
                return True
        return False

    # Returns true if the number starts with 8, 11 or 18 and is
    # either less than 100 or greater than 1000, but excluding 180,000 etc.
    @classmethod
    def checkNum(cls, num):
        needsAn = False
        # eight, eleven, eighty and eighteen
        if num in [11, 18, 8] or (num >= 80 and num < 90):
            needsAn = True
        elif num > 1000:
            num = int(round(num / 1000))
            needsAn = cls.checkNum(num)
        return needsAn

    # Retrieve the numeral prefix of a string.
    @classmethod
    def getNumericPrefix(cls, instr):
        numeric = ''
        if instr is not None:
            instr = instr.strip()
            if instr:
                first = instr[0]
                if first.isdigit():
                    numeric += first
                    for next_loc in instr[1:]:
                        if next_loc.isdigit():
                            numeric += next_loc
                        # skip commas within numbers
                        elif next_loc == ',':
                            continue
                        else:
                            break
        if numeric:
            return str(numeric)
        return None

    # Check to see if a string ends with the indefinite article "a" and it agrees with {@code np}.
    @classmethod
    def checkEndsWithIndefiniteArticle(cls, text, np):
        tokens = text.split(" ")
        lastToken = tokens[-1]
        if lastToken.lower()=="a" and cls.requiresAn(np):
            tokens = tokens[:-1]
            tokens.append("an")
            return cls.stringArrayToString(tokens)
        return text

    # Turns ["a","b","c"] into "a b c"
    @classmethod
    def stringArrayToString(cls, sArray):
        buf = ''
        for i, char in enumerate(sArray):
            buf += char
            if i != len(sArray)-1:
                buf += ' '
        return buf
