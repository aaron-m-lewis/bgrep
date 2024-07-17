#!/usr/bin/env python3

from trace_paths import trace_paths

def get_groups(end, paths):

    closed_groups = {}
    finished = set()
    path = trace_paths(end, paths)

    for transition in path:
        if not transition:
            continue
        if transition[0] == '&':
            if len(transition) > 1 and transition[1:6] == 'close' and transition[6:] not in closed_groups:
                closed_groups[transition[6:]] = ''
            elif len(transition) > 1 and transition[1:5] == 'open' and transition[5:] in closed_groups:
                finished.add(transition[5:])
        else:
            for key, char in closed_groups.items():
                if key not in finished:
                    closed_groups[key] += transition
    for key in closed_groups:
        closed_groups[key] = closed_groups[key][::-1]
    return closed_groups
