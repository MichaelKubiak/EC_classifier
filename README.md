# EC_classifier

## Description

This project will build a neural network that can classify enzymes by their EC numbers based on their HMMer scores against the Pfam database families.

It will be fresh start on the project previously stored in the Annotation repository, which became too confused and required too much maintenance.

The data parsing section will also be rewritten in order for the data to be directly useful in Keras NNs rather than the previous version, which was produced for use in Scikit-learn models.

---

## Scripts

### annotate

The script that will run the project when complete, currently serving as a guideline for the direction of development

### get_data

This script downloads the required files from ebi, expasy and uniprot respectively.

