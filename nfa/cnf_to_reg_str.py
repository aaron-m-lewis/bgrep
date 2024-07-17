#!/usr/bin/env python3

def cnf_to_reg_str(cnf_name, regexp_name, string_name):
    #read the cnf file
    f = open(f'{cnf_name}', 'r')
    lines = f.readlines()
    f.close()

    regexp_1 = ''
    regexp_2 = ''
    string_1 = ''
    string_2 = ''

    literals = set()

    for line in lines:
        clause = line.split()
        regexp_2 += '('
        backrefs = []
        for literal in clause:
            lit_num = int(literal)
            if abs(lit_num) not in literals:
                literals.add(abs(lit_num))
                regexp_1 += '((1)|(1))'
            if lit_num < 0: #negation of literal
                backrefs.append(f'\\{3 * abs(lit_num)}')
            else: #literal
                backrefs.append(f'\\{3 * abs(lit_num) - 1}')
        regexp_2 += '|'.join(backrefs)
        regexp_2 += ')'

    regexp = regexp_1 + regexp_2
    string_1 = '1' * len(literals)
    string_2 = '1' * len(lines)
    string = string_1 + string_2




    #open given file in write mode
    fre = open(f'{regexp_name}', 'w')
    #write the simple variables using join on " "
    fre.write(f'{regexp}')
    fre.close()

    #open given file in write mode
    fstr = open(f'{string_name}', 'w')
    #write the simple variables using join on " "
    fstr.write(f'{string}')
    fstr.close()
