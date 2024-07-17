#!/usr/bin/env python3

def trace_paths(end, paths):
    traverse = end
    path = []
    #print('HELLO')
    #print(paths)
    #print(traverse)
    #print(paths)
    while (traverse[0] != -1):
        path.append(traverse[2])
        traverse = paths[traverse]
        #print(traverse)
    #print(path)
    return path
