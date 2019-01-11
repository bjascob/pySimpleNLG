#!/usr/bin/python3
#
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

import sys
import unittest
sys.path.append('../../..')
from simplenlg.features         import Feature, InterrogativeType, Tense
from simplenlg.framework        import CoordinatedPhraseElement, DocumentElement, NLGElement, NLGFactory
from simplenlg.lexicon          import Lexicon
from simplenlg.phrasespec       import *
from simplenlg.realiser.english import Realiser


# Tests from SimpleNLG tutorial
class TutorialTest(unittest.TestCase):
    # no code in sections 1 and 2
    def testSection3(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory(lexicon)
        s1 = nlgFactory.createSentence("my dog is happy")
        r = Realiser(lexicon)
        output = r.realiseSentence(s1)
        self.assertEqual("My dog is happy.", output)

    # test section 5 code
    def testSection5(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory(lexicon)
        realiser = Realiser(lexicon)
        p = nlgFactory.createClause()
        p.setSubject("my dog")
        p.setVerb("chase")
        p.setObject("George")
        output = realiser.realiseSentence(p)
        self.assertEqual("My dog chases George.", output)

    # test section 6 code
    def testSection6(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory(lexicon)
        realiser = Realiser(lexicon)

        p = nlgFactory.createClause()
        p.setSubject("Mary")
        p.setVerb("chase")
        p.setObject("George")

        p.setFeature(Feature.TENSE, Tense.PAST)
        output = realiser.realiseSentence(p)
        self.assertEqual("Mary chased George.", output)

        p.setFeature(Feature.TENSE, Tense.FUTURE)
        output = realiser.realiseSentence(p)
        self.assertEqual("Mary will chase George.", output)

        p.setFeature(Feature.NEGATED, True)
        output = realiser.realiseSentence(p)
        self.assertEqual("Mary will not chase George.", output)

        p = nlgFactory.createClause()
        p.setSubject("Mary")
        p.setVerb("chase")
        p.setObject("George")

        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
        output = realiser.realiseSentence(p)
        self.assertEqual("Does Mary chase George?", output)

        p.setSubject("Mary")
        p.setVerb("chase")
        p.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_OBJECT)
        output = realiser.realiseSentence(p)
        self.assertEqual("Who does Mary chase?", output)

        p = nlgFactory.createClause()
        p.setSubject("the dog")
        p.setVerb("wake up")
        output = realiser.realiseSentence(p)
        self.assertEqual("The dog wakes up.", output)

    # test ability to use variant words
    def testVariants(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory(lexicon)
        realiser = Realiser(lexicon)

        p = nlgFactory.createClause()
        p.setSubject("my dog")
        p.setVerb("is")  # variant of be
        p.setObject("George")

        output = realiser.realiseSentence(p)
        self.assertEqual("My dog is George.", output)

        p = nlgFactory.createClause()
        p.setSubject("my dog")
        p.setVerb("chases")  # variant of chase
        p.setObject("George")

        output = realiser.realiseSentence(p)
        self.assertEqual("My dog chases George.", output)

        p = nlgFactory.createClause()
        p.setSubject(nlgFactory.createNounPhrase("the", "dogs"))   # variant of "dog"
        p.setVerb("is")  # variant of be
        p.setObject("happy")  # variant of happy
        output = realiser.realiseSentence(p)
        self.assertEqual("The dog is happy.", output)

        p = nlgFactory.createClause()
        p.setSubject(nlgFactory.createNounPhrase("the", "children"))   # variant of "child"
        p.setVerb("is")  # variant of be
        p.setObject("happy")  # variant of happy
        output = realiser.realiseSentence(p)
        self.assertEqual("The child is happy.", output)

        # following functionality is enabled
        p = nlgFactory.createClause()
        p.setSubject(nlgFactory.createNounPhrase("the", "dogs"))   # variant of "dog"
        p.setVerb("is")  # variant of be
        p.setObject("happy")  # variant of happy
        output = realiser.realiseSentence(p)
        self.assertEqual("The dog is happy.", output) #corrected automatically

    # Following code tests the section 5 to 15
    # test section 5 to match simplenlg tutorial version 4's code
    def testSection5A(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory( lexicon )
        realiser = Realiser( lexicon )
        p = nlgFactory.createClause()
        p.setSubject( "Mary" )
        p.setVerb( "chase" )
        p.setObject( "the monkey" )
        output = realiser.realiseSentence( p )
        self.assertEqual( "Mary chases the monkey.", output )

    # test section 6 to match simplenlg tutorial version 4' code
    def testSection6A(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory( lexicon )
        realiser = Realiser( lexicon )

        p = nlgFactory.createClause()
        p.setSubject( "Mary" )
        p.setVerb( "chase" )
        p.setObject( "the monkey" )

        p.setFeature( Feature.TENSE, Tense.PAST )
        output = realiser.realiseSentence( p )
        self.assertEqual( "Mary chased the monkey.", output )

        p.setFeature( Feature.TENSE, Tense.FUTURE )
        output = realiser.realiseSentence( p )
        self.assertEqual( "Mary will chase the monkey.", output )

        p.setFeature( Feature.NEGATED, True )
        output = realiser.realiseSentence( p )
        self.assertEqual( "Mary will not chase the monkey.", output )

        p = nlgFactory.createClause()
        p.setSubject( "Mary" )
        p.setVerb( "chase" )
        p.setObject( "the monkey" )

        p.setFeature( Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO )
        output = realiser.realiseSentence( p )
        self.assertEqual( "Does Mary chase the monkey?", output )

        p.setSubject( "Mary" )
        p.setVerb( "chase" )
        p.setFeature( Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_OBJECT )
        output = realiser.realiseSentence( p )
        self.assertEqual( "Who does Mary chase?", output )

    # test section 7 code
    def testSection7(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory( lexicon )
        realiser = Realiser( lexicon )

        p = nlgFactory.createClause()
        p.setSubject( "Mary" )
        p.setVerb( "chase" )
        p.setObject( "the monkey" )
        p.addComplement( "very quickly" )
        p.addComplement( "despite her exhaustion" )

        output = realiser.realiseSentence( p )
        self.assertEqual( "Mary chases the monkey very quickly despite her exhaustion.", output )

    # test section 8 code
    def testSection8(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory( lexicon )
        realiser = Realiser( lexicon )

        subject = nlgFactory.createNounPhrase( "Mary" )
        object = nlgFactory.createNounPhrase( "the monkey" )
        verb = nlgFactory.createVerbPhrase( "chase" )
        subject.addModifier( "fast" )

        p = nlgFactory.createClause()
        p.setSubject( subject )
        p.setVerb( verb )
        p.setObject( object )

        outputA = realiser.realiseSentence( p )
        self.assertEqual( "Fast Mary chases the monkey.", outputA )
        verb.addModifier( "quickly" )
        outputB = realiser.realiseSentence( p )
        self.assertEqual( "Fast Mary quickly chases the monkey.", outputB )

    # there is no code specified in section 9
    # test section 10 code
    def testSection10(self):
        lexicon = Lexicon.getDefaultLexicon()      # default simplenlg lexicon
        nlgFactory = NLGFactory( lexicon )  # factory based on lexicon
        realiser = Realiser( lexicon )

        subject1 = nlgFactory.createNounPhrase( "Mary" )
        subject2 = nlgFactory.createNounPhrase( "your", "giraffe" )

        # next line is not correct ~ should be nlgFactory.createCoordinatedPhrase ~ may be corrected in the API
        subj = nlgFactory.createCoordinatedPhrase( subject1, subject2 )
        verb = nlgFactory.createVerbPhrase( "chase" )
        p = nlgFactory.createClause()
        p.setSubject( subj )
        p.setVerb( verb )
        p.setObject( "the monkey" )

        outputA = realiser.realiseSentence( p )
        self.assertEqual( "Mary and your giraffe chase the monkey.", outputA )
        object1 = nlgFactory.createNounPhrase( "the monkey" )
        object2 = nlgFactory.createNounPhrase( "George" )

        # next line is not correct ~ should be nlgFactory.createCoordinatedPhrase ~ may be corrected in the API
        obj = nlgFactory.createCoordinatedPhrase( object1, object2 )
        obj.addCoordinate( "Martha" )
        p.setObject( obj )
        outputB = realiser.realiseSentence( p )
        self.assertEqual( "Mary and your giraffe chase the monkey, George and Martha.", outputB )

        obj.setFeature( Feature.CONJUNCTION, "or" )
        outputC = realiser.realiseSentence( p )
        self.assertEqual( "Mary and your giraffe chase the monkey, George or Martha.", outputC )

    # test section 11 code
    def testSection11(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory( lexicon )
        realiser = Realiser( lexicon )

        pA = nlgFactory.createClause( "Mary", "chase", "the monkey" )
        pA.addComplement( "in the park" )
        outputA = realiser.realiseSentence( pA )
        self.assertEqual( "Mary chases the monkey in the park.", outputA )

        # alternative build paradigm
        place = nlgFactory.createNounPhrase( "park" )
        pB = nlgFactory.createClause( "Mary", "chase", "the monkey" )

        # next line is depreciated ~ may be corrected in the API
        place.setDeterminer( "the" )
        pp = nlgFactory.createPrepositionPhrase()
        pp.addComplement( place )
        pp.setPreposition( "in" )
        pB.addComplement( pp )
        outputB = realiser.realiseSentence( pB )
        self.assertEqual( "Mary chases the monkey in the park.", outputB )
        place.addPreModifier( "leafy" )
        outputC = realiser.realiseSentence( pB )
        self.assertEqual( "Mary chases the monkey in the leafy park.", outputC )

    # section12 only has a code table as illustration
    # test section 13 code
    def testSection13(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory( lexicon )
        realiser = Realiser( lexicon )

        s1 = nlgFactory.createClause( "my cat",   "like", "fish"  )
        s2 = nlgFactory.createClause( "my dog",  "like",  "big bones" )
        s3 = nlgFactory.createClause( "my horse", "like", "grass" )
        c = nlgFactory.createCoordinatedPhrase()
        c.addCoordinate( s1 )
        c.addCoordinate( s2 )
        c.addCoordinate( s3 )
        outputA = realiser.realiseSentence( c )
        correct = "My cat likes fish, my dog likes big bones and my horse likes grass."
        self.assertEqual(correct, outputA )

        p = nlgFactory.createClause( "I", "be",  "happy" )
        q = nlgFactory.createClause( "I", "eat", "fish" )
        q.setFeature( Feature.COMPLEMENTISER, "because" )
        q.setFeature( Feature.TENSE, Tense.PAST )
        p.addComplement( q )
        outputB = realiser.realiseSentence( p )
        self.assertEqual( "I am happy because I ate fish.", outputB )

    # test section 14 code
    def testSection14(self):
        lexicon = Lexicon.getDefaultLexicon()
        nlgFactory = NLGFactory( lexicon )
        realiser = Realiser( lexicon )

        p1 = nlgFactory.createClause( "Mary", "chase", "the monkey" )
        p2 = nlgFactory.createClause( "The monkey", "fight back" )
        p3 = nlgFactory.createClause( "Mary", "be", "nervous" )
        s1 = nlgFactory.createSentence( p1 )
        s2 = nlgFactory.createSentence( p2 )
        s3 = nlgFactory.createSentence( p3 )
        par1 = nlgFactory.createParagraph( [s1, s2, s3] )
        output14a = realiser.realise( par1 ).getRealisation()
        correct = "Mary chases the monkey. The monkey fights back. Mary is nervous.\n\n"
        self.assertEqual(correct, output14a )

        section = nlgFactory.createSection( "The Trials and Tribulation of Mary and the Monkey" )
        section.addComponent( par1 )
        output14b = realiser.realise( section ).getRealisation()
        correct = "The Trials and Tribulation of Mary and the Monkey\nMary chases the monkey. " + \
                  "The monkey fights back. Mary is nervous.\n\n"
        self.assertEqual(correct, output14b )


if __name__ == '__main__':
    unittest.main()     # runs all methods that start with 'test'
