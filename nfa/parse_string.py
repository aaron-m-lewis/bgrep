#!/usr/bin/env python3

from extract_numerical import extract_numerical

def parse_string(regex: str):
    
    regex += '⊣'
   
    num_groups = 0
    stack: list[(str, str)]  = [('$', '')]
    read_dict: dict[str, set] = {'a': {'$', '(', '|', 'T'}, '(': {'$', '(', '|', 'T'}, ')': {'E'}, '|': {'E'}, '*': {'P'}}

    while (True):
        if regex[0] == '⊣' and stack[-1][0] == 'E':
            # handle group numbers first
            output = stack[-1][1]
            if num_groups:
                for group_num in range(1, num_groups + 1):
                    output = output.replace('group_num', str(group_num), 1)
            print(output)
            break
        if regex[0] in {'(', ')', '|', '*'}:
            if stack[-1][0] in read_dict[regex[0]]:
                stack.append((regex[0], ''))
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
            stack.append((regex[0], ''))
            regex = regex[1:]
            continue
  
        try:
            match (stack[-1][0][0]):
                case 'M': 
                    if stack[-2][0] == '|' and stack[-3][0] == 'E': #rule to pop E | M
                        tree = ['', '', '']
                        for i in range(0, 3):
                            tree[i] = stack.pop()[1]
                        stack.append(('E', f'union({tree[2]},{tree[0]})'))
                    elif stack[-2][0] in {'$', '('}: #rule to pop M
                        stack.append(('E', f'{stack.pop()[1]}'))
                case 'T':
                    if len(regex) == 1 or regex[0] in {'|', ')', '⊣'}: #rule to pop T
                        stack.append(('M', f'{stack.pop()[1]}'))  
                case 'F':
                    if stack[-2][0] == 'T': #rule to pop TF
                        tree = ['', '']
                        for i in range(0, 2):
                            tree[i] = stack.pop()[1]
                        stack.append(('T', f'concat({tree[1]},{tree[0]})'))
                    elif stack[-2][0] in {'$', '(', '|'}: #rule to pop F
                        stack.append(('T', f'{stack.pop()[1]}'))  
                case '*':
                    if stack[-2][0] == 'P': #rule to pop P
                        tree = ['', '']
                        for i in range(0, 2):
                            tree[i] = stack.pop()[1]
                        stack.append(('F', f'star({tree[1]})'))
                case 'P':
                    if len(regex) == 1 or regex[0] != '*': #rule to pop P*
                        stack.append(('F', f'{stack.pop()[1]}'))  
                case ')': #rule to pop ( E )
                    if stack[-2][0] == 'E' and stack[-3][0] == '(': #rule to pop ( E )
                        tree = ['', '', '']
                        for i in range(0, 3):
                            tree[i] = stack.pop()[1]
                        stack.append(('P', f'group(group_num,{tree[1]})'))  
                        num_groups += 1;
                case '\\':
                    back_ref = 0
                    if stack[-1][0][1] == 'g':
                        back_ref = extract_numerical(stack.pop()[0][3:])
                    else:
                        back_ref = extract_numerical(stack.pop()[0][1:])
                    stack.append(('P', f'backref({back_ref})'))
                case _:
                    if stack[-1][0] not in {'(', ')', '|', '\\', '*', '$'} and stack[-1][0].isascii():
                        stack.append(('P', f'symbol("{stack.pop()[0]}")'))  
                    elif stack[-1][0] in {'$', '(', '|'} and regex[0] in {'|', ')', '⊣'}: #rule to pop nothing
                        stack.append(('M', 'epsilon()'))  
        except:
            if stack[-1][0] in {'$', '(', '|'} and regex[1] in {'|', ')', '⊣'}: #rule to pop nothing
                stack.append(('M', 'epsilon()'))  
            else:
                break
