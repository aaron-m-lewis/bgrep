#!/usr/bin/env python3

from nfa_class import NFA

def star_nfa(n1: NFA):

    ''' creates a new NFA that is the star of NFA N1'''

    star = NFA()
    n1.alter_nfa(1) #make room for new start state
    
    #create new states
    star.states = ['0'] + n1.states

    #create new alphabet
    star.alphabet = n1.alphabet

    #set new start state
    star.start = '0' 

    #create new accept states
    star.accepts = n1.accepts
    star.accepts.add(star.start)

    #create new transitions
    star.transitions = star.transitions | n1.transitions
    star.transitions[star.start] = {}
    for state in star.accepts:
        if state not in star.transitions:
            star.transitions[state] = {}
            star.transitions[state]['&'] = [n1.start]
        elif '&' in star.transitions[state].keys():
            star.transitions[state]['&'].append(n1.start)
        else:
            star.transitions[state]['&'] = [n1.start]

    return star
