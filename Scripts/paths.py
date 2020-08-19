# ------------------------------------------------------------------------------------------------------
# A module containing paths for use in scripts
# ------------------------------------------------------------------------------------------------------
# Import
from pathlib import Path
import argparse

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

HOME = str(Path.home())
DATA = HOME + "/EC_classification/Data/"


# ------------------------------------------------------------------------------------------------------
# i/o path argument

def path_arg(description, help_arg):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-p", "--path", default=DATA, help=help_arg)
    return parser
