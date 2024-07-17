#!/usr/bin/env python3

# PUT THIS FILE IN SAME DIRECTORY AS FILE REQUIRING NFA MODULE
# import nfa_module as nfa
# to use the nfa class do: nfa.NFA()        or use a function like nfa.concat_nfa()

# LIBRARIES
import sys
sys.path.insert(1,'../nfa') # if run within cpX
sys.path.insert(1,'./nfa') # if run within future-layoffs

from collections import deque
import time

# FILES
from nfa_class import NFA
from string_nfa import string_nfa
from concat_nfa import concat_nfa
from union_nfa import union_nfa
from star_nfa import star_nfa
from backref_nfa import backref_nfa
from groups_nfa import groups_nfa
from parse import parse
from parse_string import parse_string
from trace_paths import trace_paths
from extract_numerical import extract_numerical
from get_groups import get_groups
from tm_class import TM
from tm_transition_class import TMTR
from cnf_to_reg_str import cnf_to_reg_str
