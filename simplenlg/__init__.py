import os
resource_directory = os.path.join(os.path.dirname(__file__), 'resources')

from .features      import *
from .format        import *
from .framework     import *
from .lexicon       import *
from .morphology    import *
from .orthography   import *
from .phrasespec    import *
from .realiser      import *
from .syntax        import *
