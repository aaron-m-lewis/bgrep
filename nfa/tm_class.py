#!/usr/bin/env python3

from tm_transition_class import TMTR

class TM:
    def __init__(self):
        self.states: list
        self.tm_alphabet: list
        self.tape_alphabet: list
        self.start: str
        self.accept: str
        self.reject: str
        self.transitions: list #FILL

    def read_tm(self, fileName):
        fileTM = open(f'{fileName}', 'r')
        lines = fileTM.readlines()
        fileTM.close

        statesStr = lines[0]
        alphaStr = lines[1]
        tapeAlphaStr = lines[2]
        startStr = lines[3]
        acceptStr = lines[4]
        rejectStr = lines[5]

        states_dict: dict[str: str] = {}

        states = statesStr.split()

        # all states are numbers
        for index, state in enumerate(states):
            states_dict[state] = str(index)


        self.states = list(states_dict.values())

        self.tm_alphabet = alphaStr.split()
        
        self.tape_alphabet = tapeAlphaStr.split()
        
        self.start = states_dict[startStr.strip()]
        
        self.accept = states_dict[acceptStr.strip()]

        self.reject = states_dict[rejectStr.strip()]
        
        # rest of lines is transitions, loop on remaining lines until done
        self.transitions = []
        for i in range(6, len(lines)):
            elements = lines[i].split()
            transition = TMTR()
            transition.from_state = states_dict[elements[0]]
            transition.reading = elements[1]
            transition.to_state = states_dict[elements[2]]
            transition.writing = elements[3]
            transition.direction = elements[4]
            self.transitions.append(transition)
            
        return self


