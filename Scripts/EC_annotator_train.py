#! /usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# A script to run the training of the neural networks
# ------------------------------------------------------------------------------------------------------
# Imports

import network
import organiser
import pickle
from paths import path_arg


# -------------------------------------------------------------------------------------------------------
# Function to build and train a level

def level(data, targets, layers, pattern, seed):

    # ---------------------------------------------------------------------------------------------------
    # set up dataset for nn

    active = organiser.remove_non_pfam(data)
    if pattern is None:
        active = organiser.reduce_none(targets, active, 20, seed)
    else:
        active = organiser.get_current(targets, active, pattern)
    inputs = data.dense_shape[1]
    outputs = network.get_outputs(targets, active, pattern)

    nodes = range(inputs, outputs, (inputs-outputs)/layers)

    nn = network.build(inputs, outputs, layers, "sigmoid", nodes, "rmsprop", "mse", ["accuracy"])

    network.train(nn, data, targets, active, 1000, 5, 0)
    return nn


# -------------------------------------------------------------------------------------------------------

def main():

    # ---------------------------------------------------------------------------------------------------
    # load files
    parser = path_arg("A script to produce a set of neural networks",
                  "Path to the folder to be used for i/o")
    parser.add_argument("-t", "--target_pattern", default=None, type=str, help="The series of values with which each EC "
                                                                     "identified by this neural network should start")
    parser.add_argument("-s", "--random_seed", default=0, type=int, help="The random seed used by the random number "
                                                                         "generator - for reproducibility")
    parser.add_argument("-i", "--hidden", default=5, type=int, help="The number of hidden layers that should be included "
                                                                    "in the network")
    args = parser.parse_args()
    DATA = args.path

    with open(DATA + "sparse_tensor", "rb") as datafile, open(DATA + "targets", "rb") as target_file, \
            open(DATA + "proteins(r)") as protein_file:
        data = pickle.load(datafile)
        targets = pickle.load(target_file)
        protein_list = protein_file.readlines()

    nn = level(data, targets, args.hidden, args.target_pattern, args.random_seed)

    with open("nn" + args.target_pattern, "wb") as nnout:
        pickle.dump(nn, nnout)


# --------------------------------------------------------------------------------------------------------

# Don't run if imported
if __name__ == '__main__':
    main()
