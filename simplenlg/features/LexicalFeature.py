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


# This class defines a list of constant values used by SimpleNLG lexicons. 
class LexicalFeature(object):
    # This feature is used to map an acronym element to the full forms of the
    # acronym.
    ACRONYM_OF = "acronym_of"
    # This feature is used to map a word to its acronyms.
    ACRONYMS = "acronyms"
    # This feature is used to list all the possible inflectional variants
    # of a word.
    INFLECTIONS = "infl"    # note - commented out in original code
    # This feature is used to specify, for a given word, what its default
    # inflectional variant is, if more than one is possible.
    DEFAULT_INFL = "default_infl"
    # This feature is used to specify the spelling variants of a word.
    SPELL_VARS = "spell_vars"
    # This feature is used to specify the default spelling variant of a word,
    # if it has more than one.
    DEFAULT_SPELL = "default_spell"
    # This feature is used to define the base form for phrases and words.
    BASE_FORM = "base_form"
    # This feature is used for determining the position of adjectives. Setting
    # this value to true means that the adjective can occupy the
    CLASSIFYING = "classifying"
    # This feature is used for determining the position of adjectives. Setting
    # this value to true means that the adjective can occupy the
    # colour position.
    COLOUR = "colour"
    # This feature gives the comparative form for adjectives and adverbs. For
    # example, dizzier is the comparative form of dizzy,
    # fatter is the comparative form of fat and
    # earlier is the comparative form of early.
    COMPARATIVE = "comparative"
    # This feature determines if a verb is ditransitive, meaning that it can
    # have a subject, direct object and indirect object. For example in the
    # phrase he gave Mary ten pounds, the verb give has three
    # components: the subject is the person doing the giving (he), the
    # direct object is the object being passed (ten pounds) and the
    # indirect object is the recipient (Mary).
    DITRANSITIVE = "ditransitive"
    # This feature determines whether a noun is masculine, feminine or neuter
    # in nature.
    GENDER = "gender"
    # This flag determines if an adverb is an intensifier, such as
    # very.
    INTENSIFIER = "intensifier"
    # This flag highlights a verb that can only take a subject and no objects.
    INTRANSITIVE = "intransitive"
    # <p> This feature represents non-countable nouns such as mud,
    # sand and water.
    NON_COUNT = "nonCount"     # commented out in original code
    # This feature gives the past tense form of a verb. For example, the past
    # tense of eat is ate, the past tense of walk is
    # walked.
    PAST = "past"
    # This feature gives the past participle tense form of a verb. For many
    # verbs the past participle is exactly the same as the past tense
    PAST_PARTICIPLE = "pastParticiple"
    # This feature gives the plural form of a noun.
    PLURAL = "plural"
    # This flag is set on adjectives that can also be used as a predicate.
    PREDICATIVE = "predicative"
    # This feature gives the present participle form of a verb.
    PRESENT_PARTICIPLE = "presentParticiple"
    # This feature gives the present third person singular form of a verb.
    PRESENT3S = "present3s"
    # This flag is used to determine whether a noun is a proper noun, such as a
    # person's name.
    PROPER = "proper"
    # This feature is used for determining the position of adjectives. Setting
    # this value to true means that the adjective can occupy the
    # qualitative position.
    QUALITATIVE = "qualitative"
    # This flag is set if a pronoun is written in the reflexive form.
    REFLEXIVE = "reflexive"
    # This feature is used to define whether an adverb can be used as a clause
    # modifier, which are normally applied at the beginning of clauses.
    SENTENCE_MODIFIER = "sentence_modifier"
    # This feature gives the superlative form for adjectives and adverbs.
    SUPERLATIVE = "superlative"
    # This flag highlights a verb that can only take a subject and an object.
    TRANSITIVE = "transitive"
    # This feature is used to define whether an adverb can be used as a verb
    # modifier, which are normally added in a phrase before the verb itself.
    VERB_MODIFIER = "verb_modifier"
    # This feature determines if the pronoun is an expletive or not. Expletive
    # pronouns are usually it or there in sentences such as:
    # It is raining now.
    # There are ten desks in the room.
    EXPLETIVE_SUBJECT = "expletive_subject"

    # Return those features related to a word's inflection, depending on its
    # category, that is, the constants for
    # PAST, PAST_PARTICIPLE, PLURAl, PRESENT_PARTICIPLE, PRESENT3S, COMPARATIVE
    # or SUPERLATIVE.
    @classmethod
    def getInflectionalFeatures(cls, element_category):
        from ..framework.LexicalCategory  import LexicalCategory    # prevent circular import
        from ..framework.PhraseCategory   import PhraseCategory
        if PhraseCategory.NOUN_PHRASE==element_category or LexicalCategory.NOUN==element_category:
            return [cls.PLURAL]
        elif PhraseCategory.VERB_PHRASE==element_category or LexicalCategory.VERB==element_category:
            return [cls.PAST, cls.PAST_PARTICIPLE, cls.PRESENT_PARTICIPLE, cls.PRESENT3S]
        elif PhraseCategory.ADJECTIVE_PHRASE==element_category or LexicalCategory.ADJECTIVE==element_category:
            return [cls.COMPARATIVE, cls.SUPERLATIVE]
        else:
            return None
