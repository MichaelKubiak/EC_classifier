# ------------------------------------------------------------------------------------------------------
# A module to provide functions for preprocessing data
# ------------------------------------------------------------------------------------------------------
# Imports

from random import sample, shuffle
from tensorflow import sparse
from math import floor
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# extract nth value from all EC numbers that begin with prev in a list

def extract(ECs, n, prev):
    out = []
    for EC in ECs:
        if EC.startswith(prev):
            out.append(EC.split(".")[n])
    if out == []:
        out.append(None)
    return out


# ------------------------------------------------------------------------------------------------------
# provide a list of active indices where the number of proteins without a classification in the current set
# has been reduced to x% of the dataset or less - for the first level of classification

def reduce(targets, protein_list, x):

    active = list(range(len(targets)))
    while (list(targets.values()).count(None)/len(targets) > x/100):
        for rand in sample(list(targets), 100000):
            target = targets[rand]
            if target is None:
                index = protein_list.index(rand)
                active.remove(index)
                del targets[index]
    return active


# ------------------------------------------------------------------------------------------------------
# produce a list of indices of proteins with ECs beginning with a series of values - for subsequent levels of classification

def get_current(targets, protein_list, pattern):
    active = list(range(len(targets)))
    for i in active:
        include = False
        for EC in targets[i]:
            if EC.startswith(pattern):
                include = True
        if not include:
            active.remove(i)
        return active


# ------------------------------------------------------------------------------------------------------
# generate batches of a dataset

def gen_batch(data, targets, active, batch_size, epochs, target_pattern=None):
    try:
        position = len(target_pattern.split("."))
    except AttributeError:
        position = 0
    for e in range(epochs):
        shuffle(active)
        for batch in range(floor(len(active)/batch_size)):
            active_batch = active[batch_size*batch:batch_size*(batch+1)]
            data_batch = sparse.SparseTensor([[0, 0]], [0], [0, data.dense_shape[1]])
            if position == 0:
                target_batch = [[target.split(".")[0] for target in targets[i]]for i in active_batch]
            else:
                target_batch = [check_list(targets[i], target_pattern, position) for i in active_batch]
            for member in active_batch:
                data_batch = sparse.concat(0, [data_batch, sparse.slice(data, [member, 0], [1, data.dense_shape[1]])])
            yield data_batch, target_batch


# ------------------------------------------------------------------------------------------------------
# return only members of a list that start with a pattern

def check_list(targets, pattern, position):
    matches = []
    for target in targets:
        if target.startswith(pattern):
            matches.append(target.split(".")[position])
    return matches
