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
from ...features.DiscourseFunction      import *
from ...features.Feature                import *
from ...features.Form                   import *
from ...features.Gender                 import *
from ...features.InternalFeature        import *
from ...features.LexicalFeature         import *
from ...features.NumberAgreement        import *
from ...features.Inflection             import *
from ...features.Person                 import *
from ...features.Tense                  import *
from ...framework.LexicalCategory       import *
from ...framework.StringElement         import *
from .DeterminerAgrHelper               import *


# This contains a number of rules for doing simple inflection.
class MorphologyRules(object):
    # A triple array of Pronouns organised by singular/plural,
    # possessive/reflexive/subjective/objective and by gender/person.
    PRONOUNS = [ [ [ "I", "you", "he", "she", "it" ],
                   [ "me", "you", "him", "her", "it" ],
                   [ "myself", "yourself", "himself", "herself", "itself" ],
                   [ "mine", "yours", "his", "hers", "its" ],
                   [ "my", "your", "his", "her", "its" ] ],
                 [ [ "we", "you", "they", "they", "they" ],
                   [ "us", "you", "them", "them", "them" ],
                   [ "ourselves", "yourselves", "themselves", "themselves", "themselves" ],
                   [ "ours", "yours", "theirs", "theirs", "theirs" ],
                   [ "our", "your", "their", "their", "their" ] ] ]
    WH_PRONOUNS = [ "who", "what", "which", "where", "why", "how", "how many" ]

    # This method performs the morphology for nouns.
    @classmethod
    def doNounMorphology(cls, element, baseWord):
        realised = ''
        # base form from baseWord if it exists, otherwise from element
        baseForm = cls.getBaseForm(element, baseWord)
        if element.isPlural() and not element.getFeatureAsBoolean(LexicalFeature.PROPER):
            pluralForm = None
            elementDefaultInfl = element.getFeature(LexicalFeature.DEFAULT_INFL)
            if elementDefaultInfl is not None and Inflection.UNCOUNT==elementDefaultInfl:
                pluralForm = baseForm
            else:
                pluralForm = element.getFeatureAsString(LexicalFeature.PLURAL)
            if pluralForm is None and baseWord is not None:
                baseDefaultInfl = baseWord.getFeatureAsString(LexicalFeature.DEFAULT_INFL)
                if baseDefaultInfl is not None and baseDefaultInfl == "uncount":
                    pluralForm = baseForm
                else:
                    pluralForm = baseWord.getFeatureAsString(LexicalFeature.PLURAL)
            if pluralForm is None:
                pattern = element.getFeature(LexicalFeature.DEFAULT_INFL)
                if Inflection.GRECO_LATIN_REGULAR == pattern:
                    pluralForm = cls.buildGrecoLatinPluralNoun(baseForm)
                else:
                    pluralForm = cls.buildRegularPluralNoun(baseForm)
            realised = pluralForm
        else:
            realised = baseForm
        realised = cls.checkPossessive(element, realised)
        realisedElement = StringElement(realised)
        realisedElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, \
                element.getFeature(InternalFeature.DISCOURSE_FUNCTION))
        return realisedElement

    # Builds a plural for regular nouns. The rules are performed in this order:
    @classmethod
    def buildRegularPluralNoun(cls, baseForm):
        plural = None
        if baseForm is not None:
            if re.fullmatch(r".*[^aeiou]y\b", baseForm):
                plural = re.sub(r"y\b", "ies", baseForm)
            elif re.fullmatch(r".*([szx]|[cs]h)\b", baseForm):
                plural = baseForm + "es"
            else:
                plural = baseForm + "s"
        return plural

    # Builds a plural for Greco-Latin regular nouns.
    @classmethod
    def buildGrecoLatinPluralNoun(cls, baseForm):
        plural = None
        if baseForm is not None:
            if baseForm.endswith("us"):
                plural = re.sub(r"us\b", "i", baseForm)
            elif baseForm.endswith("ma"):
                plural = baseForm + "ta"
            elif baseForm.endswith("a"):
                plural = baseForm + "e"
            elif re.fullmatch(r".*[(um)(on)]\b", baseForm):
                plural = re.sub(r"[(um)(on)]\b",  "a", baseForm)
            elif baseForm.endswith("sis"):
                plural = re.sub(r"sis\b", "ses", baseForm)
            elif baseForm.endswith("is"):
                plural = re.sub(r"is\b", "ides", baseForm)
            elif baseForm.endswith("men"):
                plural = re.sub(r"men\b", "mina", baseForm)
            elif baseForm.endswith("ex"):
                plural = re.sub(r"ex\b", "ices", baseForm)
            elif baseForm.endswith("x"):
                plural = re.sub(r"x\b", "ces", baseForm)
            else:
                plural = baseForm
        return plural

    # This method performs the morphology for verbs.
    @classmethod
    def doVerbMorphology(cls, element, baseWord):
        realised = None
        numberValue = element.getFeature(Feature.NUMBER)
        personValue = element.getFeature(Feature.PERSON)
        tense       = element.getFeature(Feature.TENSE)
        if isinstance(tense, Tense):
            tenseValue = tense
        else:
            tenseValue = Tense.PRESENT
        formValue = element.getFeature(Feature.FORM)
        patternValue = element.getFeature(LexicalFeature.DEFAULT_INFL)
        # base form from baseWord if it exists, otherwise from element
        baseForm = cls.getBaseForm(element, baseWord)
        if element.getFeatureAsBoolean(Feature.NEGATED) or Form.BARE_INFINITIVE == formValue:
            realised = baseForm
        elif Form.PRESENT_PARTICIPLE == formValue:
            realised = element.getFeatureAsString(LexicalFeature.PRESENT_PARTICIPLE)
            if realised is None and baseWord is not None:
                realised = baseWord.getFeatureAsString(LexicalFeature.PRESENT_PARTICIPLE)
            if realised is None:
                if Inflection.REGULAR_DOUBLE == patternValue:
                    realised = cls.buildDoublePresPartVerb(baseForm)
                else:
                    realised = cls.buildRegularPresPartVerb(baseForm)
        elif Tense.PAST == tenseValue or Form.PAST_PARTICIPLE == formValue:
            if Form.PAST_PARTICIPLE == formValue:
                realised = element.getFeatureAsString(LexicalFeature.PAST_PARTICIPLE)
                if realised is None and baseWord is not None:
                    realised = baseWord.getFeatureAsString(LexicalFeature.PAST_PARTICIPLE)
                if realised is None:
                    if "be" == baseForm.lower():
                        realised = "been"
                    elif Inflection.REGULAR_DOUBLE == patternValue:
                        realised = cls.buildDoublePastVerb(baseForm)
                    else:
                        realised = cls.buildRegularPastVerb(baseForm, numberValue, personValue)
            else:
                realised = element.getFeatureAsString(LexicalFeature.PAST)
                if realised is None and baseWord is not None:
                    realised = baseWord.getFeatureAsString(LexicalFeature.PAST)
                if realised is None:
                    if Inflection.REGULAR_DOUBLE == patternValue:
                        realised = cls.buildDoublePastVerb(baseForm)
                    else:
                        realised = cls.buildRegularPastVerb(baseForm, numberValue, personValue)
        elif (numberValue is None or NumberAgreement.SINGULAR==numberValue) and \
                (personValue is None or Person.THIRD==personValue) and \
                (tenseValue is None or Tense.PRESENT==tenseValue):
            realised = element.getFeatureAsString(LexicalFeature.PRESENT3S)
            if realised is None and baseWord is not None and not "be" == baseForm.lower():
                realised = baseWord.getFeatureAsString(LexicalFeature.PRESENT3S)
            if realised is None:
                realised = cls.buildPresent3SVerb(baseForm)
        else:
            if "be"==baseForm.lower():
                if Person.FIRST == personValue and (NumberAgreement.SINGULAR==numberValue or numberValue is None):
                    realised = "am"
                else:
                    realised = "are"
            else:
                realised = baseForm
        realisedElement = StringElement(realised)
        realisedElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, \
                element.getFeature(InternalFeature.DISCOURSE_FUNCTION))
        return realisedElement

    # return the base form of a word
    @classmethod
    def getBaseForm(cls, element, baseWord):
        # unclear what the right behaviour should be
        # for now, prefer baseWord.getBaseForm() to element.getBaseForm() for
        # verbs (ie, "is" mapped to "be")
        # but prefer element.getBaseForm() to baseWord.getBaseForm() for other
        # words (ie, "children" not mapped to "child")
        # AG: changed this to get the default spelling variant
        # needed to preserve spelling changes in the VP
        if LexicalCategory.VERB == element.getCategory():
            if baseWord is not None and baseWord.getDefaultSpellingVariant() is not None:
                return baseWord.getDefaultSpellingVariant()
            else:
                return element.getBaseForm()
        else:
            if element.getBaseForm() is not None:
                return element.getBaseForm()
            elif baseWord is None:
                return None
            else:
                return baseWord.getDefaultSpellingVariant()

    # Checks to see if the noun is possessive. If it is then nouns in ending in
    # -s become -s' while every other noun has -'s appended to
    # the end.
    @classmethod
    def checkPossessive(cls, element, realised):
        if element.getFeatureAsBoolean(Feature.POSSESSIVE):
            if realised[-1] == 's':
                realised += '\''
            else:
                realised += "'s"
        return realised

    # Builds the third-person singular form for regular verbs. The rules are
    # performed in this order:
    @classmethod
    def buildPresent3SVerb(cls, baseForm):
        morphology = None
        if baseForm is not None:
            if baseForm.lower() == "be":
                morphology = "is"
            elif re.fullmatch(r".*[szx(ch)(sh)]\b", baseForm):
                morphology = baseForm + "es"
            elif re.fullmatch(r".*[^aeiou]y\b", baseForm):
                morphology = re.sub(r"y\b", "ies", baseForm)
            else:
                morphology = baseForm + "s"
        return morphology

    # Builds the past-tense form for regular verbs. The rules are performed in
    # this order:
    @classmethod
    def buildRegularPastVerb(cls, baseForm, number, person):
        morphology = None
        if baseForm is not None:
            if baseForm.lower() == "be":
                if NumberAgreement.PLURAL == number:
                    morphology = "were"
                elif Person.SECOND == person:
                    morphology = "were"
                else:
                    morphology = "was"
            elif baseForm.endswith("e"):
                morphology = baseForm + "d"
            elif re.fullmatch(r".*[^aeiou]y\b",  baseForm):
                morphology = re.sub(r"y\b", "ied", baseForm)
            else:
                morphology = baseForm + "ed"
        return morphology

    # Builds the past-tense form for verbs that follow the doubling form of the
    # last consonant. -ed is added to the end after the last consonant
    # is doubled. For example, tug becomes tugged.
    @classmethod
    def buildDoublePastVerb(cls, baseForm):
        morphology = None
        if baseForm is not None:
            morphology = baseForm + baseForm[-1] + "ed"
        return morphology

    # Builds the present participle form for regular verbs. The rules are
    # performed in this order:
    @classmethod
    def buildRegularPresPartVerb(cls, baseForm):
        morphology = None
        if baseForm is not None:
            if baseForm.lower() == "be":
                morphology = "being"
            elif baseForm.endswith("ie"):
                morphology = re.sub(r"ie\b", "ying", baseForm)
            elif re.fullmatch(r".*[^iyeo]e\b", baseForm):
                morphology = re.sub(r"e\b", "ing", baseForm)
            else:
                morphology = baseForm + "ing"
        return morphology

    # Builds the present participle form for verbs that follow the doubling
    # form of the last consonant. -ing is added to the end after the
    # last consonant is doubled. For example, tug becomes
    # tugging.
    @classmethod
    def buildDoublePresPartVerb(cls, baseForm):
        morphology = None
        if baseForm is not None:
            morphology = baseForm + baseForm[-1] + "ing"
        return morphology

    # This method performs the morphology for adjectives.
    @classmethod
    def doAdjectiveMorphology(cls, element, baseWord):
        realised = None
        patternValue = element.getFeature(LexicalFeature.DEFAULT_INFL)
        # base form from baseWord if it exists, otherwise from element
        baseForm = cls.getBaseForm(element, baseWord)
        if element.getFeatureAsBoolean(Feature.IS_COMPARATIVE):
            realised = element.getFeatureAsString(LexicalFeature.COMPARATIVE)
            if realised is None and baseWord is not None:
                realised = baseWord.getFeatureAsString(LexicalFeature.COMPARATIVE)
            if realised is None:
                if Inflection.REGULAR_DOUBLE==patternValue:
                    realised = cls.buildDoubleCompAdjective(baseForm)
                else:
                    realised = cls.buildRegularComparative(baseForm)
        elif element.getFeatureAsBoolean(Feature.IS_SUPERLATIVE):
            realised = element.getFeatureAsString(LexicalFeature.SUPERLATIVE)
            if realised is None and baseWord is not None:
                realised = baseWord.getFeatureAsString(LexicalFeature.SUPERLATIVE)
            if realised is None:
                if Inflection.REGULAR_DOUBLE == patternValue:
                    realised = cls.buildDoubleSuperAdjective(baseForm)
                else:
                    realised = cls.buildRegularSuperlative(baseForm)
        else:
            realised = baseForm
        realisedElement = StringElement(realised)
        realisedElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, \
                element.getFeature(InternalFeature.DISCOURSE_FUNCTION))
        return realisedElement

    # Builds the comparative form for adjectives that follow the doubling form
    # of the last consonant. -er is added to the end after the last
    # consonant is doubled. For example, fat becomes fatter.
    @classmethod
    def buildDoubleCompAdjective(cls, baseForm):
        morphology = None
        if baseForm is not None:
            morphology = baseForm + baseForm[-1] + "er"
        return morphology

    # Builds the comparative form for regular adjectives. The rules are
    # performed in this order:
    @classmethod
    def buildRegularComparative(cls, baseForm):
        morphology = None
        if baseForm is not None:
            if re.fullmatch(r".*[^aeiou]y\b", baseForm):
                morphology = re.sub(r"y\b", "ier", baseForm)
            elif baseForm.endswith("e"):
                morphology = baseForm + "r"
            else:
                morphology = baseForm + "er"
        return morphology

    # Builds the superlative form for adjectives that follow the doubling form
    # of the last consonant.
    @classmethod
    def buildDoubleSuperAdjective(cls, baseForm):
        morphology = None
        if baseForm is not None:
            morphology = baseForm + baseForm[-1] + "est"
        return morphology

    # Builds the superlative form for regular adjectives. The rules are
    # performed in this order:
    @classmethod
    def buildRegularSuperlative(cls, baseForm):
        morphology = None
        if baseForm is not None:
            if re.fullmatch(r".*[^aeiou]y\b", baseForm):
                morphology = re.sub(r"y\b", "iest", baseForm)
            elif baseForm.endswith("e"):
                morphology = baseForm + "st"
            else:
                morphology = baseForm + "est"
        return morphology

    # This method performs the morphology for adverbs.
    @classmethod
    def doAdverbMorphology(cls, element, baseWord):
        realised = None
        # base form from baseWord if it exists, otherwise from element
        baseForm = cls.getBaseForm(element, baseWord)
        if element.getFeatureAsBoolean(Feature.IS_COMPARATIVE):
            realised = element.getFeatureAsString(LexicalFeature.COMPARATIVE)
            if realised is None and baseWord is not None:
                realised = baseWord.getFeatureAsString(LexicalFeature.COMPARATIVE)
            if realised is None:
                realised = cls.buildRegularComparative(baseForm)
        elif element.getFeatureAsBoolean(Feature.IS_SUPERLATIVE):
            realised = element.getFeatureAsString(LexicalFeature.SUPERLATIVE)
            if realised is None and baseWord is not None:
                realised = baseWord.getFeatureAsString(LexicalFeature.SUPERLATIVE)
            if realised is None:
                realised = cls.buildRegularSuperlative(baseForm)
        else:
            realised = baseForm
        realisedElement = StringElement(realised)
        realisedElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, \
                element.getFeature(InternalFeature.DISCOURSE_FUNCTION))
        return realisedElement

    # This method performs the morphology for pronouns.
    @classmethod
    def doPronounMorphology(cls, element):
        realised = None
        if not element.getFeatureAsBoolean(InternalFeature.NON_MORPH) and not cls.isWHPronoun(element):
            genderValue = element.getFeature(LexicalFeature.GENDER)
            personValue = element.getFeature(Feature.PERSON)
            discourseValue = element.getFeature(InternalFeature.DISCOURSE_FUNCTION)
            if element.isPlural():
                numberIndex = 1
            else:
                numberIndex = 0
            if isinstance(genderValue, Gender):
                genderIndex = genderValue.value
            else:
                genderIndex = 2
            if isinstance(personValue, Person):
                personIndex = personValue.value
            else:
                personIndex = 2
            if personIndex == 2:
                personIndex += genderIndex
            positionIndex = 0
            if element.getFeatureAsBoolean(LexicalFeature.REFLEXIVE):
                positionIndex = 2
            elif element.getFeatureAsBoolean(Feature.POSSESSIVE):
                positionIndex = 3
                if DiscourseFunction.SPECIFIER == discourseValue:
                    positionIndex += 1
            else:
                if (DiscourseFunction.SUBJECT==discourseValue and not element.getFeatureAsBoolean(Feature.PASSIVE)) or \
                   (DiscourseFunction.OBJECT ==discourseValue and     element.getFeatureAsBoolean(Feature.PASSIVE)) or \
                   DiscourseFunction.SPECIFIER == discourseValue or \
                   (DiscourseFunction.COMPLEMENT == discourseValue and element.getFeatureAsBoolean(Feature.PASSIVE)):
                    positionIndex = 0
                else:
                    positionIndex = 1
            realised = cls.PRONOUNS[numberIndex][positionIndex][personIndex]
        else:
            realised = element.getBaseForm()
        realisedElement = StringElement(realised)
        realisedElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, element.getFeature(InternalFeature.DISCOURSE_FUNCTION))
        return realisedElement

    @classmethod
    def isWHPronoun(cls, word):
        base = word.getBaseForm()
        wh = False
        if base is not None:
            for pronoun in cls.WH_PRONOUNS:
                wh = pronoun == base
                if wh:
                    break
        return wh

    # This method performs the morphology for determiners.
    @classmethod
    def doDeterminerMorphology(cls, determiner, realisation):
        if realisation is not None:
            if determiner.getRealisation() == "a":
                if determiner.isPlural():
                    determiner.setRealisation("some")
                elif DeterminerAgrHelper.requiresAn(realisation):
                    determiner.setRealisation("an")
