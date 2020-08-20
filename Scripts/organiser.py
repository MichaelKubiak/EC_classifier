# ------------------------------------------------------------------------------------------------------
# A module to provide functions for preprocessing data
# ------------------------------------------------------------------------------------------------------
# Imports

from random import sample, shuffle, seed
import tensorflow as tf
from math import floor
# try:
#     from progress.bar import IncrementalBar
# except ModuleNotFoundError:
#     ...


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# extract nth value from all EC numbers that begin with prev in a list

def extract(targets, n, prev=None):
    out = []
    if targets != "None":
        for EC in targets:
            if (n != 0 and EC.startswith(prev)) or n == 0:
                out.append(EC.split(".")[n])

    if not out:
        out.append("None")
    return out


# ------------------------------------------------------------------------------------------------------
# provide a list of active indices where the proteins all have pfam hits

def remove_non_pfam(data):
    active = list(range(data.dense_shape[0]))
    for i in active[:]:
        if tf.sparse.fill_empty_rows(tf.sparse.slice(data, [i, 0], [1, data.dense_shape[1]]), default_value=0)[1][0]:
            active.remove(i)
    return active


# ------------------------------------------------------------------------------------------------------
# reduce a list of active indices to one where the number of proteins without a classification in the current set
# is x% of the dataset or less - for the first level of classification

def reduce_none(targets, active, x, rand_seed=0):
    run = 0
    seed(rand_seed)
    while [targets[i] for i in active].count("None")/len(active) > x/100:
        run += 1
        print("Reducing 'None's: \n Run " + str(run))
        # TODO: implement progress bar
        for rand in sample(active, 100000):
            if targets[rand] == "None":
                active.remove(rand)
        print(str([targets[i] for i in active].count("None")/len(active)*100) + "%")
    return active


# ------------------------------------------------------------------------------------------------------
# produce a list of indices of proteins with ECs beginning with a series of values - for subsequent levels of classification

def get_current(targets, active, pattern):
    for i in active[:]:
        include = False
        for EC in targets[i]:
            if EC.startswith(pattern):
                include = True
        if not include:
            active.remove(i)
        return active


# ------------------------------------------------------------------------------------------------------
# generate batches of a dataset

def gen_batch(data, targets, active, batch_size, epochs, target_pattern=None, rand_seed=0):
    seed(rand_seed)
    position = get_position(target_pattern)
    for e in range(epochs):
        shuffle(list(active))
        for batch in list(range(floor(len(active)/batch_size))):
            active_batch = active[batch_size*batch:batch_size*(batch+1)]
            data_batch = tf.zeros([0, data.dense_shape[1]], dtype=float)
            target_batch = [extract(targets[i], position, target_pattern) for i in active_batch]
            for member in active_batch:
                data_batch = tf.concat([data_batch, tf.sparse.to_dense(tf.sparse.slice(data, [member, 0], [1, data.dense_shape[1]]))], axis=0)
            yield data_batch, target_batch


# ------------------------------------------------------------------------------------------------------
# get the position of the next value

def get_position(pattern):
    try:
        position = len(target_pattern.split("."))
    except AttributeError:
        position = 0
    return position
