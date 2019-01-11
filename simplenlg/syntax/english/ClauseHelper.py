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

from ...features.ClauseStatus               import *
from ...features.DiscourseFunction          import *
from ...features.Feature                    import *
from ...features.Form                       import *
from ...features.InternalFeature            import *
from ...features.InterrogativeType          import *
from ...features.NumberAgreement            import *
from ...features.Person                     import *
from ...features.Tense                      import *
from ...framework.CoordinatedPhraseElement  import *
from ...framework.LexicalCategory           import *
from ...framework.ListElement               import *
from ...framework.PhraseCategory            import *
from ...framework.PhraseElement             import *
from ...phrasespec.SPhraseSpec              import *
from ...phrasespec.VPPhraseSpec             import *
from .PhraseHelper                          import *
from .VerbPhraseHelper                      import *

# This is a helper class containing the main methods for realising the syntax
# of clauses. It is used exclusively by the SyntaxProcessor.
class ClauseHelper(object):

    # The main method for controlling the syntax realisation of clauses.
    @classmethod
    def realise(cls, parent, phrase):
        realisedElement = None
        phraseFactory = phrase.getFactory()
        splitVerb = None
        interrogObj = False
        if phrase is not None:
            realisedElement = ListElement()
            verbElement = phrase.getFeatureAsElement(InternalFeature.VERB_PHRASE)
            if verbElement is None:
                verbElement = phrase.getHead()
            cls.checkSubjectNumberPerson(phrase, verbElement)
            cls.checkDiscourseFunction(phrase)
            cls.copyFrontModifiers(phrase, verbElement)
            cls.addComplementiser(phrase, parent, realisedElement)
            cls.addCuePhrase(phrase, parent, realisedElement)
            if phrase.hasFeature(Feature.INTERROGATIVE_TYPE):
                inter = phrase.getFeature(Feature.INTERROGATIVE_TYPE)
                interrogObj = inter in [InterrogativeType.WHAT_OBJECT, InterrogativeType.WHO_OBJECT, \
                                        InterrogativeType.HOW_PREDICATE, InterrogativeType.HOW, \
                                        InterrogativeType.WHY, InterrogativeType.WHERE]
                splitVerb = cls.realiseInterrogative(phrase, parent, realisedElement, phraseFactory, verbElement)
            else:
                PhraseHelper.realiseList(parent, realisedElement, \
                                         phrase.getFeatureAsElementList(InternalFeature.FRONT_MODIFIERS), \
                                         DiscourseFunction.FRONT_MODIFIER)
            cls.addSubjectsToFront(phrase, parent, realisedElement, splitVerb)
            passiveSplitVerb =cls.addPassiveComplementsNumberPerson(phrase, parent, realisedElement, verbElement)
            if passiveSplitVerb is not None:
                splitVerb = passiveSplitVerb
            # realise verb needs to know if clause is object interrogative
            cls.realiseVerb(phrase, parent, realisedElement, splitVerb, verbElement, interrogObj)
            cls.addPassiveSubjects(phrase, parent, realisedElement, phraseFactory)
            cls.addInterrogativeFrontModifiers(phrase, parent, realisedElement)
            cls.addEndingTo(phrase, parent, realisedElement, phraseFactory)
        return realisedElement

    # Adds to to the end of interrogatives concerning indirect
    # objects.
    @classmethod
    def addEndingTo(cls, phrase, parent, realisedElement, phraseFactory):
        if InterrogativeType.WHO_INDIRECT_OBJECT == phrase.getFeature(Feature.INTERROGATIVE_TYPE):
            word = phraseFactory.createWord("to", LexicalCategory.PREPOSITION)
            realisedElement.addComponent(parent.realise(word))

    # Adds the front modifiers to the end of the clause when dealing with
    # interrogatives.
    @classmethod
    def addInterrogativeFrontModifiers(cls, phrase, parent, realisedElement):
        currentElement = None
        if phrase.hasFeature(Feature.INTERROGATIVE_TYPE):
            for subject in phrase.getFeatureAsElementList(InternalFeature.FRONT_MODIFIERS):
                currentElement = parent.realise(subject)
                if currentElement is not None:
                    currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.FRONT_MODIFIER)
                    realisedElement.addComponent(currentElement)

    # Realises the subjects of a passive clause.
    @classmethod
    def addPassiveSubjects(cls, phrase, parent, realisedElement, phraseFactory):
        currentElement = None
        if phrase.getFeatureAsBoolean(Feature.PASSIVE):
            allSubjects = phrase.getFeatureAsElementList(InternalFeature.SUBJECTS)
            if allSubjects or phrase.hasFeature(Feature.INTERROGATIVE_TYPE):
                realisedElement.addComponent(parent.realise(phraseFactory.createPrepositionPhrase("by")))
            for subject in allSubjects:
                subject.setFeature(Feature.PASSIVE, True)
                if subject.isA(PhraseCategory.NOUN_PHRASE) or isinstance(subject, CoordinatedPhraseElement):
                    currentElement = parent.realise(subject)
                    if currentElement is not None:
                        currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.SUBJECT)
                        realisedElement.addComponent(currentElement)

    # Realises the verb part of the clause.
    @classmethod
    def realiseVerb(cls, phrase, parent, realisedElement, splitVerb, verbElement, whObj):
        cls.setVerbFeatures(phrase, verbElement)
        currentElement = parent.realise(verbElement)
        if currentElement is not None:
            if splitVerb is None:
                currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.VERB_PHRASE)
                realisedElement.addComponent(currentElement)
            else:
                if isinstance(currentElement, ListElement):
                    children = currentElement.getChildren()
                    currentElement = children[0]
                    currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.VERB_PHRASE)
                    realisedElement.addComponent(currentElement)
                    realisedElement.addComponent(splitVerb)
                    for eachChild in range(1,len(children)):
                        currentElement = children[eachChild]
                        currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.VERB_PHRASE)
                        realisedElement.addComponent(currentElement)
                else:
                    currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.VERB_PHRASE)
                    if whObj:
                        realisedElement.addComponent(currentElement)
                        realisedElement.addComponent(splitVerb)
                    else:
                        realisedElement.addComponent(splitVerb)
                        realisedElement.addComponent(currentElement)

    @classmethod
    def setVerbFeatures(cls, phrase, verbElement):
        pass

    # Realises the complements of passive clauses also sets number, person for passive
    @classmethod
    def addPassiveComplementsNumberPerson(cls, phrase, parent, realisedElement, verbElement):
        passiveNumber = None
        passivePerson = None
        currentElement = None
        splitVerb = None
        verbPhrase = phrase.getFeatureAsElement(InternalFeature.VERB_PHRASE)
        # count complements to set plural feature if more than one
        numComps = 0
        coordSubj = False
        if phrase.getFeatureAsBoolean(Feature.PASSIVE) and verbPhrase is not None and not \
                InterrogativeType.WHAT_OBJECT==phrase.getFeature(Feature.INTERROGATIVE_TYPE):
            # complements of a clause are stored in the VPPhraseSpec
            for subject in verbPhrase.getFeatureAsElementList(InternalFeature.COMPLEMENTS):
                if DiscourseFunction.OBJECT == subject.getFeature(InternalFeature.DISCOURSE_FUNCTION):
                    subject.setFeature(Feature.PASSIVE, True)
                    numComps += 1
                    currentElement = parent.realise(subject)
                    if currentElement is not None:
                        currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.OBJECT)
                        if phrase.hasFeature(Feature.INTERROGATIVE_TYPE):
                            splitVerb = currentElement
                        else:
                            realisedElement.addComponent(currentElement)
                    # flag if passive subject is coordinated with an "and"
                    if not coordSubj and isinstance(subject, CoordinatedPhraseElement):
                        conj = subject.getConjunction()
                        coordSubj = (conj is not None and conj=="and")
                    if passiveNumber is None:
                        passiveNumber = subject.getFeature(Feature.NUMBER)
                    else:
                        passiveNumber = NumberAgreement.PLURAL
                    if Person.FIRST == subject.getFeature(Feature.PERSON):
                        passivePerson = Person.FIRST
                    elif Person.SECOND == subject.getFeature(Feature.PERSON) and not \
                            Person.FIRST == passivePerson:
                        passivePerson = Person.SECOND
                    elif passivePerson is None:
                        passivePerson = Person.THIRD
                    if Form.GERUND == phrase.getFeature(Feature.FORM) and not \
                            phrase.getFeatureAsBoolean(Feature.SUPPRESS_GENITIVE_IN_GERUND):
                        subject.setFeature(Feature.POSSESSIVE, True)
        if verbElement is not None:
            if passivePerson is not None:
                verbElement.setFeature(Feature.PERSON, passivePerson)
            if numComps > 1 or coordSubj:
                verbElement.setFeature(Feature.NUMBER, NumberAgreement.PLURAL)
            elif passiveNumber is not None:
                verbElement.setFeature(Feature.NUMBER, passiveNumber)
        return splitVerb

    # Adds the subjects to the beginning of the clause unless the clause is
    # infinitive, imperative or passive, or the subjects split the verb.
    @classmethod
    def addSubjectsToFront(cls, phrase, parent, realisedElement, splitVerb):
        if not Form.INFINITIVE == phrase.getFeature(Feature.FORM) and not \
               Form.IMPERATIVE == phrase.getFeature(Feature.FORM) and not \
               phrase.getFeatureAsBoolean(Feature.PASSIVE) and splitVerb is None:
            realisedElement.addComponents(cls.realiseSubjects(phrase, parent).getChildren())

    # Realises the subjects for the clause.
    @classmethod
    def realiseSubjects(cls, phrase, parent):
        currentElement = None
        realisedElement = ListElement()
        for subject in phrase.getFeatureAsElementList(InternalFeature.SUBJECTS):
            subject.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.SUBJECT)
            if Form.GERUND==phrase.getFeature(Feature.FORM) and not \
                    phrase.getFeatureAsBoolean(Feature.SUPPRESS_GENITIVE_IN_GERUND):
                subject.setFeature(Feature.POSSESSIVE, True)
            currentElement = parent.realise(subject)
            if currentElement is not None:
                realisedElement.addComponent(currentElement)
        return realisedElement

    # This is the main controlling method for handling interrogative clauses.
    @classmethod
    def realiseInterrogative(cls, phrase, parent, realisedElement, phraseFactory, verbElement):
        splitVerb = None
        if phrase.getParent() is not None:
            phrase.getParent().setFeature(InternalFeature.INTERROGATIVE, True)
        ptype = phrase.getFeature(Feature.INTERROGATIVE_TYPE)
        if isinstance(ptype, InterrogativeType):
            if ptype == InterrogativeType.YES_NO:
                splitVerb = cls.realiseYesNo(phrase, parent, verbElement, phraseFactory, realisedElement)
            elif ptype == InterrogativeType.WHO_SUBJECT or ptype == InterrogativeType.WHAT_SUBJECT:
                cls.realiseInterrogativeKeyWord(ptype.getString(), LexicalCategory.PRONOUN, parent, \
                        realisedElement, phraseFactory)
                phrase.removeFeature(InternalFeature.SUBJECTS)
            elif ptype == InterrogativeType.HOW_MANY:
                cls.realiseInterrogativeKeyWord("how", LexicalCategory.PRONOUN, parent, realisedElement, \
                                            phraseFactory)
                cls.realiseInterrogativeKeyWord("many", LexicalCategory.ADVERB, parent, realisedElement, \
                                            phraseFactory)
            elif ptype in [InterrogativeType.HOW, InterrogativeType.WHY, InterrogativeType.WHERE, \
                           InterrogativeType.WHO_OBJECT, InterrogativeType.WHO_INDIRECT_OBJECT, \
                           InterrogativeType.WHAT_OBJECT]:
                splitVerb = cls.realiseObjectWHInterrogative(ptype.getString(), phrase, parent, realisedElement, \
                                                         phraseFactory)
            elif ptype == InterrogativeType.HOW_PREDICATE:
                splitVerb = cls.realiseObjectWHInterrogative("how", phrase, parent, realisedElement, phraseFactory)
        return splitVerb

    # Check if a sentence has an auxiliary (needed to relise questions correctly)
    @classmethod
    def hasAuxiliary(cls, phrase):
        return phrase.hasFeature(Feature.MODAL) or phrase.getFeatureAsBoolean(Feature.PERFECT) or \
               phrase.getFeatureAsBoolean(Feature.PROGRESSIVE) or \
               Tense.FUTURE == phrase.getFeature(Feature.TENSE)

    # Controls the realisation of wh object questions.
    @classmethod
    def realiseObjectWHInterrogative(cls, keyword, phrase, parent, realisedElement, phraseFactory):
        splitVerb = None
        cls.realiseInterrogativeKeyWord(keyword, LexicalCategory.PRONOUN, parent, realisedElement, \
                                        phraseFactory)
        if not cls.hasAuxiliary(phrase) and not VerbPhraseHelper.isCopular(phrase):
            cls.addDoAuxiliary(phrase, parent, phraseFactory, realisedElement)
        elif not phrase.getFeatureAsBoolean(Feature.PASSIVE):
            splitVerb = cls.realiseSubjects(phrase, parent)
        return splitVerb

    # Adds a do verb to the realisation of this clause.
    @classmethod
    def addDoAuxiliary(cls, phrase, parent, phraseFactory, realisedElement):
        doPhrase = phraseFactory.createVerbPhrase("do")
        doPhrase.setFeature(Feature.TENSE, phrase.getFeature(Feature.TENSE))
        doPhrase.setFeature(Feature.PERSON, phrase.getFeature(Feature.PERSON))
        doPhrase.setFeature(Feature.NUMBER, phrase.getFeature(Feature.NUMBER))
        realisedElement.addComponent(parent.realise(doPhrase))

    # Realises the key word of the interrogative. For example, who,
    # what
    @classmethod
    def realiseInterrogativeKeyWord(cls, keyWord, cat, parent, realisedElement, phraseFactory):
        if keyWord is not None:
            question = phraseFactory.createWord(keyWord, cat)
            currentElement = parent.realise(question)
            if currentElement is not None:
                realisedElement.addComponent(currentElement)

    # Performs the realisation for YES/NO types of questions.
    @classmethod
    def realiseYesNo(cls, phrase, parent, verbElement, phraseFactory, realisedElement):
        splitVerb = None
        if not (isinstance(verbElement, VPPhraseSpec) and VerbPhraseHelper.isCopular(verbElement.getVerb())) and not \
                phrase.getFeatureAsBoolean(Feature.PROGRESSIVE) and not phrase.hasFeature(Feature.MODAL) and not \
                Tense.FUTURE==phrase.getFeature(Feature.TENSE) and not \
                phrase.getFeatureAsBoolean(Feature.NEGATED) and not \
                phrase.getFeatureAsBoolean(Feature.PASSIVE):
            cls.addDoAuxiliary(phrase, parent, phraseFactory, realisedElement)
        else:
            splitVerb = cls.realiseSubjects(phrase, parent)
        return splitVerb

    # Realises the cue phrase for the clause if it exists.
    @classmethod
    def addCuePhrase(cls, phrase, parent, realisedElement):
        currentElement = parent.realise(phrase.getFeatureAsElement(Feature.CUE_PHRASE))
        if currentElement is not None:
            currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.CUE_PHRASE)
            realisedElement.addComponent(currentElement)

    # Checks to see if this clause is a subordinate clause.
    @classmethod
    def addComplementiser(cls, phrase, parent, realisedElement):
        if ClauseStatus.SUBORDINATE== phrase.getFeature(InternalFeature.CLAUSE_STATUS) and not \
                phrase.getFeatureAsBoolean(Feature.SUPRESSED_COMPLEMENTISER):
            currentElement = parent.realise(phrase.getFeatureAsElement(Feature.COMPLEMENTISER))
            if currentElement is not None:
                realisedElement.addComponent(currentElement)

    # Copies the front modifiers of the clause to the list of post-modifiers of
    # the verb only if the phrase has infinitive form.
    @classmethod
    def copyFrontModifiers(cls, phrase, verbElement):
        frontModifiers = phrase.getFeatureAsElementList(InternalFeature.FRONT_MODIFIERS)
        clauseForm = phrase.getFeature(Feature.FORM)
        # do not overwrite existing post-mods in the VP
        if verbElement is not None:
            phrasePostModifiers = phrase.getFeatureAsElementList(InternalFeature.POSTMODIFIERS)
            if isinstance(verbElement, PhraseElement):
                verbPostModifiers = verbElement.getFeatureAsElementList(InternalFeature.POSTMODIFIERS)
                for eachModifier in phrasePostModifiers:
                    # need to check that VP doesn't already contain the post-modifier
                    # this only happens if the phrase has already been realised
                    # and later modified, with realiser called again. In that
                    # case, postmods will be copied over twice
                    if eachModifier not in verbPostModifiers:
                        verbElement.addPostModifier(eachModifier)
        if Form.INFINITIVE == clauseForm:
            phrase.setFeature(Feature.SUPRESSED_COMPLEMENTISER, True)
            for eachModifier in frontModifiers:
                if isinstance(verbElement, PhraseElement):
                    verbElement.addPostModifier(eachModifier)
            phrase.removeFeature(InternalFeature.FRONT_MODIFIERS)
            if verbElement is not None:
                verbElement.setFeature(InternalFeature.NON_MORPH, True)

    # Checks the discourse function of the clause and alters the form of the
    # clause as necessary.
    @classmethod
    def checkDiscourseFunction(cls, phrase):
        subjects = phrase.getFeatureAsElementList(InternalFeature.SUBJECTS)
        clauseForm = phrase.getFeature(Feature.FORM)
        discourseValue = phrase.getFeature(InternalFeature.DISCOURSE_FUNCTION)
        if discourseValue in [DiscourseFunction.OBJECT, DiscourseFunction.INDIRECT_OBJECT]:
            if Form.IMPERATIVE==clauseForm:
                phrase.setFeature(Feature.SUPRESSED_COMPLEMENTISER, True)
                phrase.setFeature(Feature.FORM, Form.INFINITIVE)
            elif Form.GERUND==clauseForm and len(subjects)==0:
                phrase.setFeature(Feature.SUPRESSED_COMPLEMENTISER, True)
        elif discourseValue==DiscourseFunction.SUBJECT:
            phrase.setFeature(Feature.FORM, Form.GERUND)
            phrase.setFeature(Feature.SUPRESSED_COMPLEMENTISER, True)

    # Checks the subjects of the phrase to determine if there is more than one
    # subject. This ensures that the verb phrase is correctly set. Also set
    # person correctly
    @classmethod
    def checkSubjectNumberPerson(cls, phrase, verbElement):
        currentElement = None
        subjects = phrase.getFeatureAsElementList(InternalFeature.SUBJECTS)
        pluralSubjects = False
        person = None
        if subjects:
            if len(subjects) == 1:
                currentElement = subjects[0]
                # coordinated NP with "and" are plural (not coordinated NP with "or")
                if isinstance(currentElement, CoordinatedPhraseElement) and currentElement.checkIfPlural():
                    pluralSubjects = True
                elif currentElement.getFeature(Feature.NUMBER)==NumberAgreement.PLURAL and not \
                        isinstance(currentElement, SPhraseSpec):
                    pluralSubjects = True
                elif currentElement.isA(PhraseCategory.NOUN_PHRASE):
                    currentHead = currentElement.getFeatureAsElement(InternalFeature.HEAD)
                    person = currentElement.getFeature(Feature.PERSON)
                    if currentHead is None:
                        # subject is null and therefore is not gonna be plural
                        pluralSubjects = False
                    elif currentHead.getFeature(Feature.NUMBER)==NumberAgreement.PLURAL:
                        pluralSubjects = True
                    elif isinstance(currentHead, ListElement):
                        pluralSubjects = True
            else:   # more than 1 subject
                pluralSubjects = True
        if verbElement is not None:
            plural = NumberAgreement.PLURAL if pluralSubjects else  phrase.getFeature(Feature.NUMBER)
            verbElement.setFeature(Feature.NUMBER,  plural)
            if person is not None:
                verbElement.setFeature(Feature.PERSON, person)
