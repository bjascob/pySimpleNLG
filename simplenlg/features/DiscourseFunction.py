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

# An enumeration representing the grammatical function that an element might
# take. class DiscourseFunction(Enum):
class DiscourseFunction(Enum):
    # Auxiliaries are the additional verbs added to a verb phrase to alter the
    # meaning being described.
    AUXILIARY = 0
    # Complements are additional components that are required to complement the
    # meaning of a sentence.
    COMPLEMENT = 1
    # A conjunction is a word that links items together in a coordinated
    # phrase. The most common conjunctions are and and but.
    CONJUNCTION = 2
    # Cue phrases are added to sentence to indicate document structure or flow.
    # They normally do not add any semantic information to the phrase.
    CUE_PHRASE = 3
    # Front modifiers are modifiers that apply to clauses. They are placed in
    # the syntactical structure after the cue phrase but before the subject.
    FRONT_MODIFIER = 4
    # This represents the main item of the phrase. For verb phrases, the head
    # will be the main verb. For noun phrases, the head will be the subject
    # noun. For adjective, adverb and prepositional phrases, the head will be
    # the adjective, adverb and preposition respectively.
    HEAD = 5
    # This is the indirect object of a verb phrase or an additional object that
    # is affected by the action performed. This is typically the recipient of
    # give.
    INDIRECT_OBJECT = 6
    # This is the object of a verb phrase and represents the item that the
    # action is performed upon.
    OBJECT = 7
    # Pre-modifiers, typically adjectives and adverbs, appear before the head
    # of a phrase. They can apply to noun phrases and verb phrases.
    PRE_MODIFIER = 8
     # Post-modifiers, typically adjectives and adverbs, are added after the
     # head of the phrase.
    POST_MODIFIER = 9
    # The specifier, otherwise known as the determiner, is a word that can be
    # placed before a noun in a noun phrase.
    SPECIFIER = 10
    # This is the subject of a verb phrase and represents the entity performing
    # the action.
    SUBJECT = 11
    # The verb phrase highlights the part of a clause that forms the verb
    # phrase. Verb phrases can be formed of a single verb or from a verb with a
    # particle, such as kiss, talk, bark,
    # fall down, pick up.
    VERB_PHRASE = 12

    def __str__(self):
        return self.name
