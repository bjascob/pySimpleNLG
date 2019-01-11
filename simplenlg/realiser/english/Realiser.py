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

from ...format.english.TextFormatter                import *
from ...framework.DocumentCategory                  import *
from ...framework.DocumentElement                   import *
from ...framework.NLGElement                        import *
from ...framework.NLGModule                         import *
from ...morphology.english.MorphologyProcessor      import *
from ...orthography.english.OrthographyProcessor    import *
from ...syntax.english.SyntaxProcessor              import *


class Realiser(NLGModule):
    def __init__(self, lexicon=None):
        super().__init__()
        self.initialise()
        if lexicon is not None:
            self.setLexicon(lexicon)
        self.debug = False

    # Check whether this processor separates premodifiers using a comma.
    def isCommaSepPremodifiers(self):
        if self.orthography is None:
            return False
        return self.orthography.isCommaSepPremodifiers()

    # Set whether to separate premodifiers using a comma.
    def setCommaSepPremodifiers(self, commaSepPremodifiers):
        if self.orthography is not None:
            self.orthography.setCommaSepPremodifiers(commaSepPremodifiers)

    # Check whether this processor separates cue phrases from the matrix clause using a comma.
    def isCommaSepCuephrase(self):
        if self.orthography is None:
            return False
        return self.orthography.isCommaSepCuephrase()

    # Set whether to separate cue phrases from the host phrase using a comma.
    def setCommaSepCuephrase(self, commaSepCuephrase):
        if self.orthography is not None:
            self.orthography.setCommaSepCuephrase(commaSepCuephrase)

    # @Override
    def initialise(self):
        self.morphology = MorphologyProcessor()
        self.morphology.initialise()
        self.orthography = OrthographyProcessor()
        self.orthography.initialise()
        self.syntax = SyntaxProcessor()
        self.syntax.initialise()
        self.formatter = TextFormatter()
        self.formatter.initialise()

    # @Override
    def realise(self, element):
        if isinstance(element, NLGElement):
            return self._realiseElement(element)
        elif isinstance(element, list):
            return self._realiseElementList(element)
        elif element is None:
            return ListElement()
        else:
            raise ValueError('Invalid element type: ' + str(type(element)))

    def _realiseElement(self, element):
        if self.debug:
            print("INITIAL TREE")
            print(element.printTree(None) + '\n')
        postSyntax = self.syntax.realise(element)
        if self.debug:
            print("POST-SYNTAX TREE")
            print(postSyntax.printTree(None) + '\n')
        postMorphology = self.morphology.realise(postSyntax)
        if self.debug:
            print("POST-MORPHOLOGY TREE")
            print(postMorphology.printTree(None) + '\n')
        postOrthography = self.orthography.realise(postMorphology)
        if self.debug:
            print("POST-ORTHOGRAPHY TREE")
            print(postOrthography.printTree(None) + '\n')
        if self.formatter is not None:
            postFormatter = self.formatter.realise(postOrthography)
            if self.debug:
                print("POST-FORMATTER TREE")
                print(postFormatter.printTree(None) + '\n')
        else:
            postFormatter = postOrthography
        return postFormatter

    # Convenience class to realise any NLGElement as a sentence
    def realiseSentence(self, element):
        if isinstance(element, DocumentElement):
            realised = self.realise(element)
        else:
            sentence = DocumentElement(DocumentCategory.SENTENCE, None)
            sentence.addComponent(element)
            realised = self.realise(sentence)
        if realised is None:
            return None
        else:
            return realised.getRealisation()

    # @Override
    def _realiseElementList(self, elements):
        realisedElements = []
        if elements is not None:
            for element in elements:
                realisedElement = self.realise(element)
                realisedElements.append(realisedElement)
        return realisedElements

    # @Override
    def setLexicon(self, newLexicon):
        self.syntax.setLexicon(newLexicon)
        self.morphology.setLexicon(newLexicon)
        self.orthography.setLexicon(newLexicon)

    def setFormatter(self, formatter):
        self.formatter = formatter

    def setDebugMode(self, debugOn):
        self.debug = debugOn
