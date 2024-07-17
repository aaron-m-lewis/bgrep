#!/usr/bin/env python3

from nfa_class import NFA
from string_nfa import string_nfa
from groups_nfa import groups_nfa
from union_nfa import union_nfa
from star_nfa import star_nfa
from concat_nfa import concat_nfa
from backref_nfa import backref_nfa
from extract_numerical import extract_numerical

def parse(regex):

    regex += '⊣'
    groups_dict: dict[int, int] = {0:-1}
    stack: list[(str, NFA)]  = [('$', string_nfa(''))]
    read_dict: dict[str, set] = {'a': {'$', '(', '|', 'T'}, '(': {'$', '(', '|', 'T'}, ')': {'E'}, '|': {'E'}, '*': {'P'}}

    while (True):
        opened = 0
        if regex[0] == '⊣' and stack[-1][0] == 'E':
            #print(stack)
            nfa = stack[-1][1]
            return nfa
        if regex[0] in {'(', ')', '|', '*'}:
            # handling dictionary for labeling groups in regex
            if stack[-1][0] in read_dict[regex[0]]:
                if regex[0] == '(':
                    keys = list(groups_dict.keys())
                    max_key = max(keys)
                    for key in keys:
                        if groups_dict[key] != -1:
                            groups_dict[key] += 1
                    groups_dict[max_key + 1] = 0
                    opened = 1
                stack.append((regex[0], string_nfa('')))
                regex = regex[1:]
                continue
        elif regex[0] == '\\' and stack[-1][0] in read_dict['a']:
            if regex[1] == 'g':
                back_ref = extract_numerical(regex[3:])
                stack.append((f'\\g<{back_ref}>', ''))
                regex = regex[(4 + len(str(back_ref))):]
            else:
                back_ref = extract_numerical(regex[1:])
                stack.append((f'\\{back_ref}', ''))
                regex = regex[(1 + len(str(back_ref))):]
            continue

        elif stack[-1][0] in read_dict['a'] and regex[0] != '⊣':
            stack.append((regex[0], string_nfa('')))
            regex = regex[1:]
            continue
        backref_nfa(1)
        try:
            match (stack[-1][0][0]):
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
                        group_num = -1
                        looper = sorted(list(groups_dict.keys()))
                        for key in looper:
                            if groups_dict[key] - opened == 0:
                                group_num = key
                                groups_dict[key] = -1
                                break
                            if groups_dict[key] != 0:
                                if groups_dict[key] == -1:
                                    continue
                                groups_dict[key] -= 1


                        stack.append(('P', groups_nfa(tree[1], group_num)))
                case '\\':
                    back_ref = 0
                    if stack[-1][0][1] == 'g':
                        back_ref = extract_numerical(stack.pop()[0][3:])
                    else:
                        back_ref = extract_numerical(stack.pop()[0][1:])
                    stack.append(('P', backref_nfa(back_ref)))
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
