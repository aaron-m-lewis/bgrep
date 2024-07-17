#!/usr/bin/env python3

from nfa_class import NFA

def string_nfa(string):
    
    length = len(string)
    
    nfa = NFA()

    # states (list)
    nfa.states = [str(i) for i in range(length + 1)]

    # alphabet (list)
    unique = []
    for letter in string:
        if letter not in unique:
            unique.append(letter)
    nfa.alphabet = unique

    # start state (string)
    nfa.start = nfa.states[0]

    for state in nfa.states:
        nfa.transitions[state] = {}

    # transitions (dict [str, dict[str, list]])
    for i in range(length):
        #create a transition from the state of current index, to the next state
        nfa.transitions[str(i)] = {}
        nfa.transitions[str(i)][string[i]] = str(i + 1)

    # accept states (set of strings)
    nfa.accepts = {nfa.states[-1]}

    return nfa
