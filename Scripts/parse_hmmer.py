#! /usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# A script to parse the hmmer results table into a matrix of scores
# ------------------------------------------------------------------------------------------------------
# imports

from paths import path_arg
from tensorflow import sparse
import re
import pickle


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# get the accession numbers from a set of lines

def getaccessions(file, start, expression, position):
    accessions = []
    for line in file:
        if line.startswith(start):
            accessions.append(re.split(expression, line)[position])
    return accessions


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def main():

    DATA = path_arg("A script to parse the result of a searchhmm to a sparse tensor for use in the neural network",
                    "Path to the folder to be used for i/o").path

    # ------------------------------------------------------------------------------------------------------
    # Read files

    with open(DATA+"Pfam-A.hmm", encoding="utf-8") as pfamfile:
        pfam = pfamfile.readlines()

    with open(DATA+"uniprot_sprot.fasta") as fastafile:
        fasta = fastafile.readlines()

    with open(DATA+"hmmresult_full") as infile:
        result = infile.readlines()

    # ------------------------------------------------------------------------------------------------------
    # Prepare empty sparse tensor

    # Make a list of all Pfam accessions from the HMM file
    pfam_Accessions = getaccessions(pfam, "ACC", r"\s", 3)

    # Make a list of all protein accessions in swissprot from the fasta file
    protein_Accessions = getaccessions(fasta, ">", "\|", 1)

    # Create an empty, sparse tensor with the proportions of the lists that were made
    hmmtensor = sparse.SparseTensor(
        indices=[[0, 0]],
        values=[float(0)],
        dense_shape=[len(protein_Accessions), len(pfam_Accessions)])

    # ------------------------------------------------------------------------------------------------------
    # Add scores to rows and columns denoted by protein and family respectively

    for line in result:
        if not line.startswith("#"):
            # parse line for score
            splitline = [col for col in re.split(r"\s", line) if col != ""]
            protein_index = protein_Accessions.index(splitline[0].split("|")[1])
            pfam_index = pfam_Accessions.index(splitline[3])
            hmmtensor = sparse.add(hmmtensor, sparse.SparseTensor(
                indices=[[protein_index, pfam_index]],
                values=[float(splitline[5])],
                dense_shape=[len(protein_Accessions), len(pfam_Accessions)]))

    # ------------------------------------------------------------------------------------------------------
    # Write lists and sparse tensor to files
    with open(DATA + "sparse_tensor", "wb") as tensor, open(DATA + "proteins(r)", "w") as rows, open(DATA + "families(c)", "w") as columns:
        pickle.dump(hmmtensor, tensor)
        rows.write("\n".join(protein_Accessions))
        columns.write("\n". join(pfam_Accessions))


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

# Don't run if imported
if __name__ == '__main__':
    main()
