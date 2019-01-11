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

import os
import logging
from   copy         import deepcopy
from   collections  import defaultdict
import xml.etree.ElementTree as ET
from   .Lexicon                     import *
from   ..features.Inflection        import *
from   ..features.LexicalFeature    import *
from   ..framework.LexicalCategory  import *
from   ..framework.WordElement      import *
from simplenlg import resource_directory

# This class loads words from an XML lexicon. All features specified in the
# lexicon are loaded
class XMLLexicon(Lexicon):
    XML_BASE     = "base"       # base form of Word
    XML_CATEGORY = "category"   # base form of Word
    XML_ID       = "id"         # base form of Word
    XML_WORD     = "word"       # node defining a word
    def __init__(self, lexicon_fn=None):
        super().__init__()
        if not lexicon_fn:
            lexicon_fn = os.path.join(resource_directory, 'default-lexicon.xml')
        self.words          = set()                    # all words in the lexicon
        self.indexByID      = {}                       # ID's are unique mapping to word
        self.indexByBase    = defaultdict(list)        # list of WordElements by base_form
        self.indexByVariant = defaultdict(list)        # list of WordElements by variants
        self.createLexicon(lexicon_fn)

    # Lexicon Note: not all entries have an ID
    # 'base' is the word but this is not unique either (multiple pos)
    def createLexicon(self, xmlfile):
        # Load the XML file to a list of dictionaries
        tree = ET.parse(xmlfile)
        for word in tree.getroot():
            if word.tag != self.XML_WORD :
                logging.warning('Unrecognized element: %s', word.tag)
                continue
            definition = {}
            for item in word:
                if len(item) != 0:
                    raise ValueError('Parsing error. There should be no sub-items')
                definition[item.tag] = item.text
            we = self.convertToWord(definition)
            self.words.add(we)
            self.IndexWord(we)
        self.addSpecialCases()

    # create a simplenlg WordElement from a Word node in a lexicon XML file
    def convertToWord(self, word_dict):
        word = WordElement()
        inflections = []
        for feature, value in word_dict.items():
            feature = feature.strip()
            if isinstance(value, str):
                value = value.strip()
            if not feature:
                logging.error("Error in XML lexicon for %s", word)
                break
            if feature.lower() == self.XML_BASE:
                word.setBaseForm(value)
            elif feature.lower() == self.XML_CATEGORY:
                word.setCategory(LexicalCategory[value.upper()])
            elif feature.lower() == self.XML_ID:
                word.setId(value)
            elif value is None or value=='':
                # if this is an infl code, add it to inflections
                infl = Inflection.getInflCode(feature)
                if infl is not None:
                    inflections.append(infl)
                # otherwise assume it's a boolean feature
                else:
                    word.setFeature(feature, True)
            else:
                word.setFeature(feature, value)
        # if no infl specified, assume regular
        if not inflections:
            inflections.append(Inflection.REGULAR)
        # default inflection code is "reg" if we have it, else random pick form infl codes available
        if Inflection.REGULAR in inflections:
            defaultInfl = Inflection.REGULAR
        else:
            defaultInfl = inflections[0]
        word.setFeature(LexicalFeature.DEFAULT_INFL, defaultInfl)
        word.setDefaultInflectionalVariant(defaultInfl)
        for infl in inflections:
            word.addInflectionalVariant(infl)
        return word

    def IndexWord(self, word):
        base_form = word.getBaseForm()
        if base_form:
            self.indexByBase[base_form].append(word)
        wid = word.getId()
        if wid:
            if wid in self.indexByID:
                logging.error("Lexicon error: ID %s occurs more than once", wid)
            else:
                self.indexByID[wid] = word
        for variant in self.getVariants(word):
            self.indexByVariant[variant].append(word)

    def addSpecialCases(self):
        be = self.getWord("be", LexicalCategory.VERB)
        if be is not None:
            self.indexByVariant['is'  ].append(be)
            self.indexByVariant['am'  ].append(be)
            self.indexByVariant['are' ].append(be)
            self.indexByVariant['was' ].append(be)
            self.indexByVariant['were'].append(be)

    # Override Lexicon see simplenlg.lexicon.Lexicon#getWords
    def getWords(self, baseForm, category):
        return self.getWordsFromIndex(baseForm, category, self.indexByBase)

    # get matching keys from an index map
    def getWordsFromIndex(self, indexKey, category, indexMap):
        results = []
        # case 1: unknown, return empty list
        if indexKey not in indexMap:
            return results
        # case 2: category is ANY, return everything
        if category == LexicalCategory.ANY:
            for word in indexMap[indexKey]:
                results.append(deepcopy(word))
            return results
        else:
            # case 3: other category, search for match
            for word in indexMap[indexKey]:
                if word.getCategory() == category:
                    results.append(deepcopy(word))
            return results

    # Override Lexicon see simplenlg.lexicon.Lexicon#getWordsByID
    def getWordsByID(self, wid):
        results = []
        if wid in self.indexByID:
            results.append(deepcopy(self.indexByID[wid]))
        return results

    # Override Lexicon see simplenlg.lexicon.Lexicon#getWordsFromVariant
    def getWordsFromVariant(self, variant, category):
        return self.getWordsFromIndex(variant, category, self.indexByVariant)

    # quick-and-dirty routine for getting morph variants should be replaced by something better!
    def getVariants(self, word):
        variants = set()
        variants.add(word.getBaseForm())
        category = word.getCategory()
        if isinstance(category, LexicalCategory):
            if category == LexicalCategory.NOUN:
                variants.add(self.getVariant(word, LexicalFeature.PLURAL, "s"))
            elif category == LexicalCategory.ADJECTIVE:
                variants.add(self.getVariant(word, LexicalFeature.COMPARATIVE, "er"))
                variants.add(self.getVariant(word, LexicalFeature.SUPERLATIVE, "est"))
            elif category == LexicalCategory.VERB:
                variants.add(self.getVariant(word, LexicalFeature.PRESENT3S, "s"))
                variants.add(self.getVariant(word, LexicalFeature.PAST, "ed"))
                variants.add(self.getVariant(word, LexicalFeature.PAST_PARTICIPLE, "ed"))
                variants.add(self.getVariant(word, LexicalFeature.PRESENT_PARTICIPLE, "ing"))
        return variants

    # quick-and-dirty routine for computing morph forms Should be replaced by something better!
    def getVariant(self, word, feature, suffix):
        if word.hasFeature(feature):
            return word.getFeatureAsString(feature)
        else:
            return self.getForm(word.getBaseForm(), suffix)

    # quick-and-dirty routine for standard orthographic changes Should be replaced by something better!
    def getForm(self, base, suffix):
        # add a suffix to a base form, with orthographic changes
        # rule 1 - convert final "y" to "ie" if suffix does not start with "i"
        # eg, cry + s = cries , not crys
        if base.endswith("y") and not suffix.startswith("i"):
            base = base[0:-1] + "ie"
        # rule 2 - drop final "e" if suffix starts with "e" or "i"
        # eg, like+ed = liked, not likeed
        if base.endswith("e") and (suffix.startswith("e") or suffix.startswith("i")):
            base = base[0:-1]
        # rule 3 - insert "e" if suffix is "s" and base ends in s, x, z, ch, sh
        # eg, watch+s -> watches, not watchs
        if suffix.startswith("s") and (base.endswith("s") or base.endswith("x") \
                or base.endswith("z") or base.endswith("ch") or base.endswith("sh")):
            base = base + "e"
        # have made changes, now append and return
        return base + suffix # eg, want + s = wants
