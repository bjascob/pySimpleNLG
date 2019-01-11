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

from ...features.DiscourseFunction          import *
from ...features.Feature                    import *
from ...features.Form                       import *
from ...features.InternalFeature            import *
from ...features.InterrogativeType          import *
from ...features.NumberAgreement            import *
from ...features.Tense                      import *
from ...framework.CoordinatedPhraseElement  import *
from ...framework.InflectedWordElement      import *
from ...framework.LexicalCategory           import *
from ...framework.ListElement               import *
from ...framework.NLGElement                import *
from ...framework.PhraseCategory            import *
from ...framework.PhraseElement             import *
from ...framework.StringElement             import *
from ...framework.WordElement               import *
from ...phrasespec.SPhraseSpec              import *
from .PhraseHelper                          import *


# This class contains static methods to help the syntax processor realise verb
# phrases. It adds auxiliary verbs into the element tree as required.
class VerbPhraseHelper(object):
    # The main method for realising verb phrases.
    @classmethod
    def realise(cls, parent,  phrase):
        realisedElement = ListElement()
        mainVerbRealisation = []
        auxiliaryRealisation = []
        if phrase is not None:
            vgComponents = cls.createVerbGroup(parent, phrase)
            cls.splitVerbGroup(vgComponents, mainVerbRealisation, auxiliaryRealisation)
            realisedElement = ListElement()
            if not phrase.hasFeature(InternalFeature.REALISE_AUXILIARY) or \
                    phrase.getFeatureAsBoolean(InternalFeature.REALISE_AUXILIARY):
                cls.realiseAuxiliaries(parent, realisedElement, auxiliaryRealisation)
                PhraseHelper.realiseList(parent, realisedElement, phrase.getPreModifiers(), \
                    DiscourseFunction.PRE_MODIFIER)
                cls.realiseMainVerb(parent, phrase, mainVerbRealisation, realisedElement)
            elif cls.isCopular(phrase.getHead()):
                cls.realiseMainVerb(parent, phrase, mainVerbRealisation, realisedElement)
                PhraseHelper.realiseList(parent, realisedElement, phrase.getPreModifiers(), \
                        DiscourseFunction.PRE_MODIFIER)
            else:
                PhraseHelper.realiseList(parent, realisedElement, phrase.getPreModifiers(), \
                        DiscourseFunction.PRE_MODIFIER)
                cls.realiseMainVerb(parent, phrase, mainVerbRealisation, realisedElement)
            cls.realiseComplements(parent, phrase, realisedElement)
            PhraseHelper.realiseList(parent, realisedElement, phrase.getPostModifiers(), \
                    DiscourseFunction.POST_MODIFIER)
        return realisedElement

    # Realises the auxiliary verbs in the verb group.
    @classmethod
    def realiseAuxiliaries(cls, parent, realisedElement, auxiliaryRealisation):
        aux = None
        currentElement = None
        while auxiliaryRealisation:
            aux = auxiliaryRealisation.pop()
            currentElement = parent.realise(aux)
            if currentElement is not None:
                realisedElement.addComponent(currentElement)
                currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.AUXILIARY)

    # Realises the main group of verbs in the phrase.
    @classmethod
    def realiseMainVerb(cls, parent, phrase, mainVerbRealisation, realisedElement):
        currentElement = None
        main = None
        while mainVerbRealisation:
            main = mainVerbRealisation.pop()
            main.setFeature(Feature.INTERROGATIVE_TYPE, phrase.getFeature(Feature.INTERROGATIVE_TYPE))
            currentElement = parent.realise(main)
            if currentElement is not None:
                realisedElement.addComponent(currentElement)

    # Realises the complements of this phrase.
    @classmethod
    def realiseComplements(cls, parent, phrase, realisedElement):
        indirects = ListElement()
        directs = ListElement()
        unknowns = ListElement()
        discourseValue = None
        currentElement = None
        for complement in phrase.getFeatureAsElementList(InternalFeature.COMPLEMENTS):
            discourseValue = complement.getFeature(InternalFeature.DISCOURSE_FUNCTION)
            currentElement = parent.realise(complement)
            if currentElement is not None:
                currentElement.setFeature(InternalFeature.DISCOURSE_FUNCTION, DiscourseFunction.COMPLEMENT)
                if DiscourseFunction.INDIRECT_OBJECT==discourseValue:
                    indirects.addComponent(currentElement)
                elif DiscourseFunction.OBJECT == discourseValue:
                    directs.addComponent(currentElement)
                else:
                    unknowns.addComponent(currentElement)
        if not InterrogativeType.isIndirectObject(phrase.getFeature(Feature.INTERROGATIVE_TYPE)):
            realisedElement.addComponents(indirects.getChildren())
        if not phrase.getFeatureAsBoolean(Feature.PASSIVE):
            if not InterrogativeType.isObject(phrase.getFeature(Feature.INTERROGATIVE_TYPE)):
                realisedElement.addComponents(directs.getChildren())
            realisedElement.addComponents(unknowns.getChildren())

    # Splits the stack of verb components into two sections. One being the verb
    # associated with the main verb group, the other being associated with the
    # auxiliary verb group.
    @classmethod
    def splitVerbGroup(cls, vgComponents, mainVerbRealisation, auxiliaryRealisation):
        mainVerbSeen = False
        for word in vgComponents:
            if not mainVerbSeen:
                mainVerbRealisation.append(word)
                if word != "not":
                    mainVerbSeen = True
            else:
                auxiliaryRealisation.append(word)

    # Creates a stack of verbs for the verb phrase. Additional auxiliary verbs
    # are added as required based on the features of the verb phrase.
    @classmethod
    def createVerbGroup(cls, parent, phrase):
        actualModal = None
        formValue = phrase.getFeature(Feature.FORM)
        tenseValue = phrase.getFeature(Feature.TENSE)
        modal = phrase.getFeatureAsString(Feature.MODAL)
        modalPast = False
        vgComponents = []
        interrogative = phrase.hasFeature(Feature.INTERROGATIVE_TYPE)
        if Form.GERUND==formValue or Form.INFINITIVE==formValue:
            tenseValue = Tense.PRESENT
        if Form.INFINITIVE==formValue:
            actualModal = "to"
        elif formValue is None or Form.NORMAL==formValue:
            if Tense.FUTURE==tenseValue and modal is None and \
                    ((not isinstance(phrase.getHead(), CoordinatedPhraseElement)) or \
                    (isinstance(phrase.getHead(), CoordinatedPhraseElement) and interrogative)):
                actualModal = "will"
            elif modal is not None:
                actualModal = modal
                if Tense.PAST==tenseValue:
                    modalPast = True
        cls.pushParticles(phrase, parent, vgComponents)
        frontVG = cls.grabHeadVerb(phrase, tenseValue, modal is not None)
        cls.checkImperativeInfinitive(formValue, frontVG)
        if phrase.getFeatureAsBoolean(Feature.PASSIVE):
            frontVG = cls.addBe(frontVG, vgComponents, Form.PAST_PARTICIPLE)
        if phrase.getFeatureAsBoolean(Feature.PROGRESSIVE):
            frontVG = cls.addBe(frontVG, vgComponents, Form.PRESENT_PARTICIPLE)
        if phrase.getFeatureAsBoolean(Feature.PERFECT) or modalPast:
            frontVG = cls.addHave(frontVG, vgComponents, modal, tenseValue)
        frontVG = cls.pushIfModal(actualModal is not None, phrase, frontVG, vgComponents)
        frontVG = cls.createNot(phrase, vgComponents, frontVG, modal is not None)
        if frontVG is not None:
            cls.pushFrontVerb(phrase, vgComponents, frontVG, formValue, interrogative)
        cls.pushModal(actualModal, phrase, vgComponents)
        return vgComponents

    # Pushes the modal onto the stack of verb components.
    @classmethod
    def pushModal(cls, actualModal, phrase, vgComponents):
        if actualModal is not None and not phrase.getFeatureAsBoolean(InternalFeature.IGNORE_MODAL):
            vgComponents.append(InflectedWordElement(actualModal, LexicalCategory.MODAL))

    # Pushes the front verb onto the stack of verb components.
    @classmethod
    def pushFrontVerb(cls, phrase, vgComponents,  frontVG, formValue, interrogative):
        interrogType = phrase.getFeature(Feature.INTERROGATIVE_TYPE)
        if Form.GERUND == formValue:
            frontVG.setFeature(Feature.FORM, Form.PRESENT_PARTICIPLE)
            vgComponents.append(frontVG)
        elif Form.PAST_PARTICIPLE==formValue:
            frontVG.setFeature(Feature.FORM, Form.PAST_PARTICIPLE)
            vgComponents.append(frontVG)
        elif Form.PRESENT_PARTICIPLE==formValue:
            frontVG.setFeature(Feature.FORM, Form.PRESENT_PARTICIPLE)
            vgComponents.append(frontVG)
        elif (not (formValue is None or Form.NORMAL==formValue) or interrogative) and \
                not cls.isCopular(phrase.getHead()) and not vgComponents:
            # AG: fix below: if interrogative, only set non-morph feature in
            # case it's not WHO_SUBJECT OR WHAT_SUBJECT
            if not (InterrogativeType.WHO_SUBJECT==interrogType or InterrogativeType.WHAT_SUBJECT==interrogType):
                frontVG.setFeature(InternalFeature.NON_MORPH, True)
            vgComponents.append(frontVG)
        else:
            numToUse = cls.determineNumber(phrase.getParent(), phrase)
            frontVG.setFeature(Feature.TENSE, phrase.getFeature(Feature.TENSE))
            frontVG.setFeature(Feature.PERSON, phrase.getFeature(Feature.PERSON))
            frontVG.setFeature(Feature.NUMBER, numToUse)
            #don't push the front VG if it's a negated interrogative WH object question
            if not (phrase.getFeatureAsBoolean(Feature.NEGATED) and (InterrogativeType.WHO_OBJECT==interrogType or \
                    InterrogativeType.WHAT_OBJECT==interrogType)):
                vgComponents.append(frontVG)

    # Adds not to the stack if the phrase is negated.
    @classmethod
    def createNot(cls, phrase,  vgComponents, frontVG, hasModal):
        newFront = frontVG
        if phrase.getFeatureAsBoolean(Feature.NEGATED):
            factory = phrase.getFactory()
            # before adding "do", check if this is an object WH interrogative
            # in which case, don't add anything as it's already done by ClauseHelper
            interrType = phrase.getFeature(Feature.INTERROGATIVE_TYPE)
            addDo = not (InterrogativeType.WHAT_OBJECT==interrType or InterrogativeType.WHO_OBJECT==interrType)
            if vgComponents or frontVG is not None and cls.isCopular(frontVG):
                vgComponents.append(InflectedWordElement("not", LexicalCategory.ADVERB))
            else:
                if frontVG is not None and not hasModal:
                    frontVG.setFeature(Feature.NEGATED, True)
                    vgComponents.append(frontVG)
                vgComponents.append(InflectedWordElement("not", LexicalCategory.ADVERB))
                if addDo:
                    if factory is not None:
                        newFront = factory.createInflectedWord("do", LexicalCategory.VERB)
                    else:
                        newFront = InflectedWordElement("do", LexicalCategory.VERB)
        return newFront

    # Pushes the front verb on to the stack if the phrase has a modal.
    @classmethod
    def pushIfModal(cls, hasModal, phrase, frontVG, vgComponents):
        newFront = frontVG
        if hasModal and not phrase.getFeatureAsBoolean(InternalFeature.IGNORE_MODAL):
            if frontVG is not None:
                frontVG.setFeature(InternalFeature.NON_MORPH, True)
                vgComponents.append(frontVG)
            newFront = None
        return newFront

    # Adds have to the stack.
    @classmethod
    def addHave(cls, frontVG, vgComponents, modal, tenseValue):
        newFront = frontVG
        if frontVG is not None:
            frontVG.setFeature(Feature.FORM, Form.PAST_PARTICIPLE)
            vgComponents.append(frontVG)
        newFront = InflectedWordElement("have", LexicalCategory.VERB)
        newFront.setFeature(Feature.TENSE, tenseValue)
        if modal is not None:
            newFront.setFeature(InternalFeature.NON_MORPH, True)
        return newFront

    # Adds the be verb to the front of the group.
    @classmethod
    def addBe(cls, frontVG, vgComponents, frontForm):
        if frontVG is not None:
            frontVG.setFeature(Feature.FORM, frontForm)
            vgComponents.append(frontVG)
        return InflectedWordElement("be", LexicalCategory.VERB)

    # Checks to see if the phrase is in imperative, infinitive or bare
    # infinitive form. If it is then no morphology is done on the main verb.
    @classmethod
    def checkImperativeInfinitive(cls, formValue, frontVG):
        if (Form.IMPERATIVE==formValue or Form.INFINITIVE==formValue or Form.BARE_INFINITIVE==formValue) and \
                frontVG is not None:
            frontVG.setFeature(InternalFeature.NON_MORPH, True)

    # Grabs the head verb of the verb phrase and sets it to future tense if the
    # phrase is future tense. It also turns off negation if the group has a
    # modal.
    @classmethod
    def grabHeadVerb(cls, phrase,  tenseValue, hasModal):
        frontVG = phrase.getHead()
        if frontVG is not None:
            if isinstance(frontVG, WordElement):
                frontVG = InflectedWordElement(frontVG)
            # AG: tense value should always be set on frontVG
            if tenseValue is not None:
                frontVG.setFeature(Feature.TENSE, tenseValue)
            if hasModal:
                frontVG.setFeature(Feature.NEGATED, False)
        return frontVG

    # Pushes the particles of the main verb onto the verb group stack.
    @classmethod
    def pushParticles(cls, phrase, parent, vgComponents):
        particle = phrase.getFeature(Feature.PARTICLE)
        if isinstance(particle, str):
            vgComponents.append(StringElement(particle))
        elif isinstance(particle, NLGElement):
            vgComponents.append(parent.realise(particle))

    # Determines the number agreement for the phrase ensuring that any number
    # agreement on the parent element is inherited by the phrase.
    @classmethod
    def determineNumber(cls, parent,  phrase):
        numberValue = phrase.getFeature(Feature.NUMBER)
        if isinstance(numberValue, NumberAgreement):
            number = numberValue
        else:
            number = NumberAgreement.SINGULAR
        # Ehud Reiter = modified below to force number from VP for WHAT_SUBJECT
        # and WHO_SUBJECT interrogatuves
        if isinstance(parent, PhraseElement):
            if parent.isA(PhraseCategory.CLAUSE) and (PhraseHelper.isExpletiveSubject(parent) or \
                    InterrogativeType.WHO_SUBJECT==parent.getFeature(Feature.INTERROGATIVE_TYPE) or \
                    InterrogativeType.WHAT_SUBJECT==parent.getFeature(Feature.INTERROGATIVE_TYPE)) and \
                    cls.isCopular(phrase.getHead()):
                if cls.hasPluralComplement(phrase.getFeatureAsElementList(InternalFeature.COMPLEMENTS)):
                    number = NumberAgreement.PLURAL
                else:
                    number = NumberAgreement.SINGULAR
        return number

    # Checks to see if any of the complements to the phrase are plural.
    @classmethod
    def hasPluralComplement(cls, complements):
        plural = False
        for eachComplement in complements:
            if eachComplement is not None and eachComplement.isA(PhraseCategory.NOUN_PHRASE):
                numberValue = eachComplement.getFeature(Feature.NUMBER)
                if numberValue is not None and NumberAgreement.PLURAL==numberValue:
                    plural = True
                    break
        return plural

    # Checks to see if the base form of the word is copular, i.e. be.
    @classmethod
    def isCopular(cls, element):
        copular = False
        if isinstance(element, InflectedWordElement) or isinstance(element, WordElement):
            copular = "be" == element.getBaseForm().lower()
        elif isinstance(element, PhraseElement):
            # get the head and check if it's "be"
            if isinstance(element, SPhraseSpec):
                head = element.getVerb()
            else:
                head = element.getHead()
            if head is not None:
                copular = isinstance(head, WordElement) and "be"==head.getBaseForm()
        return copular
