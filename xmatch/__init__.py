"""

subpackage syntax

this will allow import and call of the form

from librgm.xmatch import xmatch_groups

idxmatch1, idxmatch2, dr = xmatch_groups()

"""
from .match_lists import *
from .xmatch_cat import *
from .xmatch_checkplots import *
from .xmatch_cat_checkplots import *
from .xmatch_checkplot1 import *
from .xmatch_checkplot2 import *
from .xmatch_groups import *
from .xmatch_cat_join import *
from .xmatch_selfcheck import *
from .add_columns_spherical_offsets import *
from .check_matching import *
