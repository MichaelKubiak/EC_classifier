#! /usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# A script to relate Swissprot entries to EC numbers
# ------------------------------------------------------------------------------------------------------
# Imports

from paths import path_arg
import re
import pickle


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# Function to make a dictionary of protein IDs and the EC numbers of those proteins

def get_ECs(enzyme):
    ECs = {}
    current = ""
    for line in enzyme:
        if line.startswith("ID"):
            current = line.split()[1]
        elif line.startswith("DR"):
            for protein in re.finditer(r"\w+,", line):
                if protein.group().split(",")[0] in ECs:
                    ECs[protein.group().split(",")[0]].append(current)
                else:
                    ECs[protein.group().split(",")[0]] = [current]
    return ECs


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def main():

    DATA = path_arg("A script to relate Swissprot entries to their EC numbers").path

    # ------------------------------------------------------------------------------------------------------
    # read files

    with open(DATA + "proteins(r)", "r") as protein_file, open (DATA + "enzyme.dat", "r") as enzyme_file:
        proteins = protein_file.readlines()
        enzymes = enzyme_file.readlines()

    ECs = get_ECs(enzymes)

    with open(DATA + "EC_dict", "w") as out:
        pickle.dump(ECs, out)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

# Don't run if imported
if __name__ == '__main__':
    main()

