#!/usr/bin/env python3

from collections import deque
from get_groups import get_groups
from trace_paths import trace_paths

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
            real_path = trace_paths(old_path, paths)
            path = tuple(real_path)
            group_matches = ()
            if old_path:
                group_matches = tuple([(key, value) for key, value in get_groups(old_path, paths).items()])
            
            backref = 0

            #check if node has been previously processed, if it has do not process it again, if it hasn't mark it as processed
            if (curr_depth, curr_state, group_matches) in visited:
                continue
            else:
                visited.add((curr_depth, curr_state, group_matches))
            
            #check to see if current node is an accept state and is at the end of the string, if so break with exit status True
            if curr_state in self.accepts and curr_depth >= length:
                accept = True
                break
            
            if curr_state not in self.transitions: ################## THIS CHANGE MADE IT WORK #####################
                continue

            #check for epsilon transitions from the current state and add any nodes to the frontier
            for key in self.transitions[curr_state]:
                if '&' == key[0]:
                    for state in self.transitions[curr_state][key]:
                        if (curr_depth, state, group_matches) in visited:
                            continue
                        new_path = (curr_depth, curr_state, key, group_matches, state)
                        paths[new_path] = old_path
                        frontier.append((curr_depth, (new_path)))
                elif 'copy' == key[:4]:
                    backref = key[-1] #FIX LATER
                    
            
            #check if the end of the string has been reached, if so stop processing current node
            if curr_depth >= length and not backref:
                continue

            try:
                curr_char = string[curr_depth]
            except:
                curr_char = ''
                
            #check for any transitions from the current state on the current symbol in the string and any nodes to the frontier
            if curr_char not in self.transitions[curr_state] and not backref:
                continue
            elif curr_char in self.transitions[curr_state]:
                for state in self.transitions[curr_state][curr_char]:
                    if (curr_depth + 1, state, group_matches) in visited:
                        continue
                    new_path = (curr_depth + 1, curr_state, curr_char, group_matches, state)
                    paths[new_path] = old_path
                    frontier.append((curr_depth + 1, (new_path)))
            if backref:
                state = self.transitions[curr_state][f'copy{backref}'][0]
                groups_dict = get_groups(old_path, paths)
                try:
                    group_match = groups_dict[backref]
                except:
                    group_match = ''
                if len(string) >= curr_depth + len(group_match) and string[curr_depth:len(group_match) + curr_depth] == group_match:
                    new_path = (curr_depth + len(group_match), curr_state, group_match, group_matches, state)
                    paths[new_path] = old_path
                    frontier.append((curr_depth + len(group_match), (new_path)))
                    
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

