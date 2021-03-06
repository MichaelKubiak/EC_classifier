# ------------------------------------------------------------------------------------------------------
# A module to provide functions for building and using a neural network
# ------------------------------------------------------------------------------------------------------
# Imports

import tensorflow as tf
import organiser


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# Function to build a neural network

def build(inputs, outputs, hidden, activations, nodes, optimiser, loss, metrics):

    # if only one number of nodes or activation function is given, multiply it by the number of hidden layers so that all hidden layers have those values
    if hidden != 1:
        if type(nodes) is int:
            nodes = [nodes] * hidden
        if type(activations) is str:
            activations = [activations] * hidden

    # create the sequential neural network
    nn = tf.keras.Sequential()

    # add the input layer
    nn.add(tf.keras.layers.Dense(nodes[0], activations[0], input_shape=(inputs,)))
    for i in range(1, hidden):
        nn.add(tf.keras.layers.Dense(nodes[i], activations[i]))
    # add the output layer with as many nodes as there are classifications
    nn.add(tf.keras.layers.Dense(outputs, "sigmoid"))
    # compile the neural network
    nn.compile(optimiser, loss, metrics)
    return nn


# ------------------------------------------------------------------------------------------------------
# Function to train a neural network

def train(nn, data, targets, active, batch_size, epochs, rand_seed):

    nn.fit(organiser.gen_batch(data, targets, active, batch_size, epochs, rand_seed), epochs=epochs, verbose=1)


# ------------------------------------------------------------------------------------------------------
# Function to determine the number of distinct outputs

def get_outputs(targets, active, prev):
    unique = set()
    for target in [targets[i] for i in active]:
        try:
            unique = unique | set(organiser.extract(target, len(prev.split(".")), prev))
        except AttributeError:
            unique = unique | set(organiser.extract(targets, 0))
    outputs = len(unique)
    return outputs
