#!/usr/bin/env python3

from nfa_class import NFA

def backref_nfa(k: int):
    
    nfa = NFA()
    nfa.states = ['0', '1']
    nfa.alphabet = []
    nfa.start = nfa.states[0]

    for state in nfa.states:
        nfa.transitions[state] = {}
    nfa.transitions['0'][f'copy{k}'] = '1'

    # accept states (set of strings)
    nfa.accepts = {nfa.states[-1]}

    return nfa
