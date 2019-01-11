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

# An enumeration representing the different types of interrogatives or
# questions that SimpleNLG can realise. T
class InterrogativeType(Enum):
    # The type of interrogative relating to the manner in which an event
    # happened. For example, John kissed Mary becomes
    # How did John kiss Mary?
    HOW = 0
    # A how question related to a predicative sentence, such as John is fine, which becomes How is John?
    HOW_PREDICATE = 1
    # This type of interrogative is a question pertaining to the object of a
    # phrase. For example, John bought a horse becomes what did
    # John buy? while John gave Mary a flower becomes
    # What did
    # John give Mary?
    WHAT_OBJECT = 2
    # This type of interrogative is a question pertaining to the subject of a
    # phrase. For example, A hurricane destroyed the house becomes
    # what destroyed the house?
    WHAT_SUBJECT = 3
    # This type of interrogative concerns the object of a verb that is to do
    # with location. For example, John went to the beach becomes
    # Where did John go?
    WHERE = 4
    # This type of interrogative is a question pertaining to the indirect
    # object of a phrase when the indirect object is a person. For example,
    # John gave Mary a flower becomes
    # Who did John give a flower to?
    WHO_INDIRECT_OBJECT = 5
    # This type of interrogative is a question pertaining to the object of a
    # phrase when the object is a person. For example,
    # John kissed Mary becomes who did John kiss?
    WHO_OBJECT = 6
    # This type of interrogative is a question pertaining to the subject of a
    # phrase when the subject is a person. For example,
    # John kissed Mary becomes Who kissed Mary? while
    # John gave Mary a flower becomes Who gave Mary a flower?
    WHO_SUBJECT = 7
    # The type of interrogative relating to the reason for an event happening.
    # For example, John kissed Mary becomes Why did John kiss
    # Mary?
    WHY = 8
    # This represents a simple yes/no questions. So taking the example phrases
    # of John is a professor and John kissed Mary we can
    # construct the questions Is John a professor? and
    # Did John kiss Mary?
    YES_NO = 9
    # This represents a "how many" questions. For example of
    # dogs chased John/em> becomes How many dogs chased John
    HOW_MANY = 10

    # A method to determine if the {@code InterrogativeType} is a question
    # concerning an element with the discourse function of an object.
    @classmethod
    def isObject(cls, otype):
        return otype in [cls.WHO_OBJECT, cls.WHAT_OBJECT]

    # A method to determine if the {@code InterrogativeType} is a question
    # concerning an element with the discourse function of an indirect object.
    @classmethod
    def isIndirectObject(cls, otype):
        return cls.WHO_INDIRECT_OBJECT==otype

    # Convenience method to return the String corresponding to the question
    # word. Useful, since the types in this enum aren't all simply convertible
    # to strings (e.g. WHO_SUBJCT and WHO_OBJECT both
    # correspond to String Who)
    def getString(self):
        otype = self
        if otype in [self.HOW, self.HOW_PREDICATE]:
            return "how"
        elif otype in [self.WHAT_OBJECT, self.WHAT_SUBJECT]:
            return "what"
        elif otype == self.WHERE:
            return "where"
        elif otype in [self.WHO_INDIRECT_OBJECT, self.WHO_OBJECT, self.WHO_SUBJECT]:
            return "who"
        elif otype==self.WHY:
            return "why"
        elif otype==self.HOW_MANY:
            return "how many"
        elif otype==self.YES_NO:
            return "yes/no"
        return ''

    def __str__(self):
        return self.name
