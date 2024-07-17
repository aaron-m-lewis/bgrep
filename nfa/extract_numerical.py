#!/usr/bin/env python3

def extract_numerical(string: str):
    index = 0
    number = ''
    while (index < len(string) and string[index].isdigit()):
        number += string[index]
        index += 1
    return number
