#!/usr/bin/env python3
import sys
from collections import deque
import time

class NFA:
    def __init__(self):
        self.states: list
        self.alphabet: list
        self.start: str
        self.transitions: dict(dict(list)) = {}
        self.accepts: set

    def write_nfa(self, fileName):
        #open given file in write mode
        f = open(f'{fileName}', 'w')
        #write the simple variables using join on " "
        f.write(f'{" ".join(self.states)}\n')
        f.write(f'{" ".join(self.alphabet)}\n')
        f.write(f'{self.start}\n')
        f.write(f'{" ".join(list(self.accepts))}\n')
        #traverse the entire adjacency list to produce all of the transitions in the machine
        for states in self.transitions:
            for transitions in self.transitions[states]:
                for destinations in self.transitions[states][transitions]:
                    f.write(f'{states} {transitions} {destinations}\n')
        f.close()
                


    def read_nfa(self, fileName):
        fileNFA = open(f'{fileName}', 'r')
        lines = fileNFA.readlines()
        fileNFA.close()

        statesStr = lines[0]
        alphaStr = lines[1]
        startStr = lines[2]
        acceptStr = lines[3]

        states_dict: dict[str: str] = {}

        # setting attributes
        states = statesStr.split()

        for index, state in enumerate(states):
            states_dict[state] = str(index)

            
        self.states = list(states_dict.values())

        for i in range(len(self.states)):
            self.transitions[self.states[i]] = {}
        
        self.alphabet = alphaStr.split()
        

        self.start = states_dict[startStr.strip()]
        

        self.accepts = set([states_dict[i] for i in acceptStr.split()])
        
        

        # rest on lines is transitions, loop until done

        # use len of self.states and populate dictionary of transitions with an empty dictionary for each state
        for i in range(4, len(lines)):
            elements = lines[i].split()
            if elements[1] in self.transitions[states_dict[elements[0]]]:
                self.transitions[states_dict[elements[0]]][elements[1]].append(states_dict[elements[2]])
            else:
                self.transitions[states_dict[elements[0]]][elements[1]] = [states_dict[elements[2]]]

        #print(self.transitions)

        return self

    
    def print_nfa(self):
        print(f'{" ".join(self.states)}\n', end = '')
        print(f'{" ".join(self.alphabet)}\n', end = '')
        print(f'{self.start}\n', end = '')
        print(f'{" ".join(list(self.accepts))}\n', end = '')
        #traverse the entire adjacency list to produce all of the transitions in the machine
        for states in self.transitions:
            for transitions in self.transitions[states]:
                for destinations in self.transitions[states][transitions]:
                    print(f'{states} {transitions} {destinations}\n', end = '')


    def match(self, string):
        
        #queue that will hold node information
        frontier = deque([(0, (-1, 'q', '&', self.start))])
        #dict that will track all taken paths
        paths: dict((int, str, str, str)) = {}
        #set that will keep track of each node already processed
        visited = set()
        #variable that will hold node for each processing iteration, declared outside of loop to prevent repeated declaration and loss of scope
        node = ()
        #accept condition declared outside of loop to prevent loss of scope
        accept = False
        length = len(string)

        while (frontier):

            #pop the front of the queue to process a node in the NFA
            node = frontier.popleft()
            
            #set variables to avoid repeated index and increase clarity
            old_path = node[-1]
            new_path = ()
            curr_depth = node[0]
            curr_state = node[-1][-1]
            
            #check if node has been previously processed, if it has do not process it again, if it hasn't mark it as processed
            if (curr_depth, curr_state) in visited:
                continue
            else:
                visited.add((curr_depth, curr_state))
            
            #check to see if current node is an accept state and is at the end of the string, if so break with exit status True
            if curr_state in self.accepts and curr_depth >= length:
                accept = True
                break
            
            if curr_state not in self.transitions: ################## THIS CHANGE MADE IT WORK #####################
                continue

            #check for epsilon transitions from the current state and add any nodes to the frontier
            if '&' in self.transitions[curr_state]:
                for state in self.transitions[curr_state]['&']:
                    if (curr_depth, state) in visited:
                        continue
                    new_path = (curr_depth, curr_state, '&', state)
                    paths[new_path] = old_path
                    frontier.append((curr_depth, (new_path)))
            
            #check if the end of the string has been reached, if so stop processing current node
            if curr_depth >= length:
                continue

            curr_char = string[curr_depth]
                
            #check for any transitions from the current state on the current symbol in the string and any nodes to the frontier
            if curr_char not in self.transitions[curr_state]:
                continue
            else:
                for state in self.transitions[curr_state][curr_char]:
                    if (curr_depth + 1, state) in visited:
                        continue
                    new_path = (curr_depth + 1, curr_state, curr_char, state)
                    paths[new_path] = old_path
                    frontier.append((curr_depth + 1, (new_path)))
        return (accept, paths, node[-1])

    
    def alter_nfa(self, difference): ############################################################################################
        self.states = [str(difference + index) for index, state in enumerate(self.states)]

        self.start = str(int(self.start) + difference)

        new_transitions = {}
        for key in self.transitions.keys(): #grabs the outer keys, or the states transitions start from
            new_key = str(int(key) + difference)
            new_transitions[new_key] = {}
            for key2 in self.transitions[key]:
                new_transitions[new_key][key2] = [str(int(destination) + difference) for destination in self.transitions[key][key2]]

        self.transitions = new_transitions

        self.accepts = set([str((int(accept)+difference)) for accept in self.accepts])

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

    # transitions (dict [str, dict[str, list]])
    for i in range(length):
        #create a transition from the state of current index, to the next state
        nfa.transitions[str(i)] = {}
        nfa.transitions[str(i)][string[i]] = str(i + 1)

    # accept states (set of strings)
    nfa.accepts = {nfa.states[-1]}

    return nfa

def parse(regex):
    
    stack: list[(str, NFA)]  = [('$', string_nfa(''))]
    read_dict: dict[str, set] = {'a': {'$', '(', '|', 'T'}, '(': {'$', '(', '|', 'T'}, ')': {'E'}, '|': {'E'}, '*': {'P'}}

    while (True):
        #print(stack)
        #print(regex)
        #time.sleep(.5)
        if regex[0] == '⊣' and stack[-1][0] == 'E':
            nfa = stack[-1][1]
            return nfa
        if regex[0] in {'(', ')', '|', '\\', '*'}:
            if stack[-1][0] in read_dict[regex[0]]:
                stack.append((regex[0], string_nfa('')))
                regex = regex[1:]
                continue
        elif stack[-1][0] in read_dict['a'] and regex[0] != '⊣':
            stack.append((regex[0], string_nfa('')))
            regex = regex[1:]
            continue
  
        try:
            match (stack[-1][0]):
                case 'M': 
                    if stack[-2][0] == '|' and stack[-3][0] == 'E': #rule to pop E | M
                        tree = [None, None, None]
                        for i in range(0, 3):
                            tree[i] = stack.pop()[1] #now popping an NFA
                        stack.append(('E', union_nfa(tree[2],tree[0])))
                    elif stack[-2][0] in {'$', '('}: #rule to pop M
                        stack.append(('E', stack.pop()[1]))
                case 'T':
                    if len(regex) == 1 or regex[0] in {'|', ')', '⊣'}: #rule to pop T
                        stack.append(('M', stack.pop()[1]))  
                case 'F':
                    if stack[-2][0] == 'T': #rule to pop TF
                        tree = []
                        for i in range(0, 2):
                            nfa = stack.pop()[1]
                            tree.append(nfa)
                        nfa = concat_nfa(tree[1], tree[0])
                        stack.append(('T', nfa))
                    elif stack[-2][0] in {'$', '(', '|'}: #rule to pop F
                        stack.append(('T', stack.pop()[1]))  
                case '*':
                    if stack[-2][0] == 'P': #rule to pop P
                        tree = [None, None]
                        for i in range(0, 2):
                            nfa = stack.pop()[1]
                            tree.append(nfa)
                        stack.append(('F', star_nfa(nfa)))
                case 'P':
                    if len(regex) == 1 or regex[0] != '*': #rule to pop P*
                        stack.append(('F', stack.pop()[1]))  
                case ')': #rule to pop ( E )
                    if stack[-2][0] == 'E' and stack[-3][0] == '(': #rule to pop ( E )
                        tree = []
                        for i in range(0, 3):
                            nfa = stack.pop()[1]
                            tree.append(nfa)
                        stack.append(('P', tree[1]))
                case _:
                    if stack[-1][0] not in {'(', ')', '|', '\\', '*', '$'} and stack[-1][0].isascii():
                        stack.append(('P', string_nfa(stack.pop()[0])))  
                    elif stack[-1][0] in {'$', '(', '|'} and regex[0] in {'|', ')', '⊣'}: #rule to pop nothing
                        stack.append(('M', string_nfa('')))  
        except:
            if stack[-1][0] in {'$', '(', '|'} and regex[1] in {'|', ')', '⊣'}: #rule to pop nothing
                stack.append(('M', string_nfa('')))  
            else:
                break
