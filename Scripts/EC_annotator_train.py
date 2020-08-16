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

def level():
    ...

# -------------------------------------------------------------------------------------------------------

def main():

    # ---------------------------------------------------------------------------------------------------
    # load files
    DATA = path_arg("A script to produce a set of neural networks",
                  "Path to the folder to be used for i/o").path

    with open(DATA + "sparse_tensor", "rb") as datafile, open(DATA + "EC_dict", "rb") as EC_file, \
            open(DATA + "proteins(r)") as protein_file:
        tensor = pickle.load(datafile)
        targets = pickle.load(EC_file)
        protein_list = protein_file.readlines()

    # ---------------------------------------------------------------------------------------------------
    # set up dataset for first nn

    active = organiser.reduce_none(targets, protein_list, 20)

# --------------------------------------------------------------------------------------------------------

# Don't run if imported
if __name__ == '__main__':
    main()
