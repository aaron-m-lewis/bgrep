#!/usr/bin/env python3

from nfa_class import NFA

def groups_nfa(n, group: int):

    groups = NFA()

    n.alter_nfa(1)

    accept = str(int(max([int(i) for i in n.states])) + 1)

    groups.alphabet = n.alphabet
    groups.states = ['0'] + n.states + [f'{accept}']
    groups.transitions = n.transitions.copy()
    groups.start = '0'

    groups.transitions['0'] = {}

    groups.transitions['0'][f'&open{group}'] = [n.start]
    groups.accepts = {accept}
    
    for state in n.accepts:
        if state not in groups.transitions:
            groups.transitions[state] = {}
        groups.transitions[state][f'&close{group}'] = [accept]


    return groups
