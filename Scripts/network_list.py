#! /usr/bin/env python3
# ---------------------------------------------------------------------------------------------
# A script to determine networks that need to be made
# ---------------------------------------------------------------------------------------------
# Imports

from paths import path_arg
import organiser

# ---------------------------------------------------------------------------------------------
# A function to make a dictionary of the patterns that will be used for networks

def network_patterns(targets, active, prev = None):
    patterns = {}
    position = organiser.get_position(prev)
    patterns[position] = []
    for i in active:
        patterns[position].append(organiser.extract(targets[i], position, prev))


