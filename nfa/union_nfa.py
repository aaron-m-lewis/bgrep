#!/usr/bin/env python3

from nfa_class import NFA

def union_nfa(n1: NFA, n2: NFA):
    ''' creates a new NFA that is the union of NFAs N1 and N2'''
    union = NFA()
    n1.alter_nfa(1) #make room for new start state
    difference = max([index for index, state in enumerate(n1.states)]) + 2

    #altering everything on one nfa for easier combination
    n2.alter_nfa(difference)

    #create new states
    union.states = ['0'] + n1.states + n2.states

    #create new alphabet
    new_alpha = n1.alphabet
    for letter in n2.alphabet:
        if letter not in new_alpha:
            new_alpha.append(letter)

    union.alphabet = new_alpha

    #create new start state
    union.start = '0'

    #create new transitions
    #new start state with epsilon transition to the start states of each individual NFA
    union.transitions = union.transitions | n1.transitions | n2.transitions
    union.transitions[union.start] = {}
    union.transitions[union.start]['&'] = [n1.start, n2.start]

    #create new accept states
    union.accepts = n1.accepts.union(n2.accepts)

    return union
