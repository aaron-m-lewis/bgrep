#!/usr/bin/env python3

from nfa_class import NFA

def concat_nfa(n1: NFA, n2: NFA):
    ''' creates a new NFA that is the concatenation of NFAs N1 and N2'''
    concat = NFA()

    difference = max([index for index, state in enumerate(n1.states)]) + 1
    
    n2.alter_nfa(difference)

    #create new states
    concat.states = n1.states + n2.states

    #create new alphabet

    new_alpha = n1.alphabet
    for letter in n2.alphabet:
        if letter not in new_alpha:
            new_alpha.append(letter)

    concat.alphabet = new_alpha

    #set new start state
    concat.start = n1.start

    #create new transitions
    concat.transitions = concat.transitions | n1.transitions | n2.transitions
    #create transitions from accept states of n1 to start states of n2
    for state in n1.accepts:
        if state not in concat.transitions:
            concat.transitions[state] = {}
            concat.transitions[state]['&'] = [n2.start]
        elif '&' in concat.transitions[state].keys(): #KEY ERROR
            concat.transitions[state]['&'].append(n2.start)
        else:
            concat.transitions[state]['&'] = [n2.start]

    #create new accept states
    concat.accepts = n2.accepts

    return concat
