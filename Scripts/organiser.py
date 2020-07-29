# ------------------------------------------------------------------------------------------------------
# A module to provide functions for preprocessing data
# ------------------------------------------------------------------------------------------------------
# Imports

from random import sample

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
# has been reduced to x% of the dataset or less

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
# generate batches of a dataset - data has already been pared based on

def gen_batch(data, targets, batch_size, epochs):
    for e in range(epochs):



