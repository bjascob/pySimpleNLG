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

# This class defines a list of features which can be set up users of SimpleNLG.
# Note that there are three feature classes in SimpleNLG.
class Feature(object):
    # This feature determines if the adjectives should be reordered. Some
    # lexicons might support the positioning of adjectives and by default, this
    # order will be used. The user can override the ordering of adjectives by
    # setting this
    ADJECTIVE_ORDERING = "adjective_ordering"
    # This feature determines if the auxiliary verbs in a clause should be
    # aggregated.
    AGGREGATE_AUXILIARY = "aggregate_auxiliary"
    # The complementiser is the word that joins a subordinate clause to the
    # parent clause.
    COMPLEMENTISER = "complementiser"
    # This feature represents the word (or phrase) used for linking coordinated
    # phrases together.
    CONJUNCTION = "conjunction"
    # This feature represents the type of conjunction this coordination
    # represents.
    CONJUNCTION_TYPE = "conjunction_type"
    # An appositive is a type of postmodifying phrase which is quasi-synonymous
    # with, or a possible replacement of, the phrase it modifies. A typical
    # example occurs with NPs
    APPOSITIVE = "appositive"
    # This feature represents the cue phrase of a sentence. Cue phrases
    # sometimes appear at the start of sentences.
    CUE_PHRASE = "cue_phrase"
    # This features determines if the phrase is elided. Elided phrases are
    # omitted from the final realisation.
    ELIDED = "elided"
    # This feature dictates the form that a verb takes.
    FORM = "form"
    # This feature determines the type of interrogative (question) used for the
    # clause.
    INTERROGATIVE_TYPE = "interrogative_type"
    # This flag determines if the Adjective or Adverb should be inflected into
    # the comparative form.
    IS_COMPARATIVE = "is_comparative"
    # This flag determines if the Adjective or Adverb should be inflected into
    # the superlative form.
    IS_SUPERLATIVE = "is_superlative"
    # The modal represents the modal auxiliary verb that is used in a verb
    # phrase to express mood or tense.
    MODAL = "modal"
    # The flag determines if the corresponding verb phrase should be negated.
    NEGATED = "negated"
    # This feature is used to determine if the element is to be represented in
    # singular or plural form.
    NUMBER = "number"
    # This feature represents the pattern that a particular word follows
    # when being inflected.
    PATTERN = "pattern"    # note -commented out in original code
    # This feature represents a particle used in conjunction with a verb.
    PARTICLE = "particle"
    # This flag shows if the phrase or clause should be written in the passive
    # form.
    PASSIVE = "passive"
    # This flag shows if the phrase or clause should be written in the perfect
    # form.
    PERFECT = "perfect"
    # This feature represents the first-person, second-person or third-person
    # nature of the phrase.
    PERSON = "person"
    # This flag shows if the noun phrase should be written in the possessive
    # form.
    POSSESSIVE = "possessive"
    # This flag can be set for noun phrases where it is desirable to overwrite
    # the subject with a suitable pronoun.
    PRONOMINAL = "pronominal"
    # This flag determines if the verb phrase should be constructed in the
    # progressive form.
    PROGRESSIVE = "progressive"
    # This flag can be set when specifiers in a coordinated phrase should be
    # raised.
    RAISE_SPECIFIER = "raise_specifier"
    # This flag is set when it is necessary to suppress the genitive when
    # dealing with gerund forms.
    SUPPRESS_GENITIVE_IN_GERUND = "suppress_genitive_in_gerund"
    # This flag determines if complementisers in subordinating clauses should
    # be suppressed.
    SUPRESSED_COMPLEMENTISER = "suppressed_complementiser"
    # This flag represents the tense or temporal quality of a verb.
    TENSE = "tense"
