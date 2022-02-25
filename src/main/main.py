#!/usr/bin/python
"""Main source file"""

import sys

from secondary_structure import *

edit_dict = create_edit_dict(sys.argv[1])
score_dict = find_secondary_structures(edit_dict, sys.argv[2])
create_output_csv("scores.csv", score_dict)
