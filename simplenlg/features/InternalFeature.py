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


# This class defines a list of features internally used within the SimpleNLG
# system.
class InternalFeature(object):
    # This feature determines if the element is an acronym.
    ACRONYM = "acronym"
    # This feature is used to reference the base word element as created by the
    # lexicon.
    BASE_WORD = "base_word"
    # This feature determines the status of a sentence
    CLAUSE_STATUS = "clause_status"
    # This feature refers to the list of complements for the phrase.
    COMPLEMENTS = "complements"
    # This feature refers to the list of components in a list
    COMPONENTS = "components"
    # This feature is the list of coordinated phrases in a
    # CoordinatedPhraseElement.
    COORDINATES = "coordinates"
    # This feature defines the role each element plays in the structure of the
    # text. For example, the phrase John played football has
    # John as the subject, play as the base verb and
    # football as the complement.
    DISCOURSE_FUNCTION = "discourse_function"
    NON_MORPH = "non_morph"
    # This feature tracks any front modifiers in sentences. Front modifiers are
    # placed after the cue phrase but before the subject.
    FRONT_MODIFIERS = "front_modifiers"
    # This feature points to the head element in a phrase. The head element is
    # deemed to be the subject in a noun phrase, the verb in a verb phrase, the
    # adjective in an adjective phrase, the adverb in an adverb phrase or the
    # preposition in a preposition phrase. The PhraseElement has a
    # convenience method for getting and setting the head feature.
    HEAD = "head"
    # This flag is used to determine if the modal should be included in the
    # verb phrase.
    IGNORE_MODAL = "ignore_modal"
    # This flag determines if the sentence is interrogative or not.
    INTERROGATIVE = "interrogative"
    # This feature represents the list of post-modifier elements.
    # Post-modifiers are added to the end of phrases and coordinated phrases.
    POSTMODIFIERS = "postmodifiers"
    # This feature represents the list of premodifier elements. Premodifiers
    # are added to phrases before the head of the phrase, and to coordinated
    # phrases before the coordinates.
    PREMODIFIERS = "premodifiers"
    # This flag is used to define whether a noun phrase has had its specifier
    # raised. It is used in conjunction with the RAISE_SECIFIER
    # feature.
    RAISED = "raised"
    # This flag determines if auxiliary verbs should be realised in coordinated
    # verb phrases.
    REALISE_AUXILIARY = "realise_auxiliary"
    # This feature contains the specifier for a noun phrase. For example
    # the and my.
    SPECIFIER = "specifier"
    # This feature represents the list of subjects in a clause.
    SUBJECTS = "subjects"
    # This feature represents the verb phrase in a clause.
    VERB_PHRASE = "verb_phrase"
