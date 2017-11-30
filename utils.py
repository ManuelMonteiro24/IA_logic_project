""" A set of utility functions to the converter program."""

import sys

def output_disjunctions(sample_obj):
    """ Returns a string with the cnf sentence received in the sample_obj argument
    in a format which is the same of the prover.py input. The print is done trough a recursive
    process similar to the one explained in the to_cnf.py file."""
    if isinstance(sample_obj, tuple):
        if sample_obj[0] == 'and':
            #a set of disjunctions per line
            return  "[ " + output_disjunctions(sample_obj[1]) + " ]\n[ " + output_disjunctions(sample_obj[2]) + " ]"
        elif sample_obj[0] == 'or':
            #in this format the 'or' represation is omited
            return output_disjunctions(sample_obj[1]) + " , " + output_disjunctions(sample_obj[2])
        else:
            #negated literal case
            return  "( 'not' , " + sample_obj[1] + " )"

    elif isinstance(sample_obj, str):
        #literal found
        return  "'" + sample_obj + "'"
    else:
        #wrong format case
        return None
