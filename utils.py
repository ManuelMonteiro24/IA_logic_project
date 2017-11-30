""" A set of utility functions to the converter program."""

import sys

def output_disjunctions_str(sample_obj):
    """ Returns a string with the cnf sentence received in the sample_obj argument
    in a format which is the same of the prover.py input. The print is done trough a recursive
    process similar to the one explained in the to_cnf.py file."""
    if isinstance(sample_obj, tuple):
        if sample_obj[0] == 'and':
            #a set of disjunctions per line
            result1 = output_disjunctions_str(sample_obj[1])
            if result1[0] == "[":
                result1 = result1[2:-2]

            result2 = output_disjunctions_str(sample_obj[2])
            if result2[0] == "[":
                result2 = result2[2:-2]
            return  "[ " + result1  + " ]\n[ " + result2 + " ]"
        elif sample_obj[0] == 'or':
            #in this format the 'or' represation is omited
            return output_disjunctions_str(sample_obj[1]) + " , " + output_disjunctions_str(sample_obj[2])
        else:
            #negated literal case
            return  "( 'not' , '" + sample_obj[1] + "' )"

    elif isinstance(sample_obj, str):
        #literal found
        return  "'" + sample_obj + "'"
    else:
        #wrong format case
        return None

def output_disjunctions_set(sample_obj):
    """ Returns a string with the cnf sentence received in the sample_obj argument
    in a format which is the same of the prover.py input. The print is done trough a recursive
    process similar to the one explained in the to_cnf.py file."""
    if isinstance(sample_obj, tuple):
        if sample_obj[0] == 'and':
            #a set of disjunctions per line
            return_set = set()
            auxset1 = set()
            auxset2 = set()
            auxset3 = set()
            auxset4 = set()

            if isinstance(sample_obj[1], tuple) and sample_obj[1][0] == 'and' and isinstance(sample_obj[2], tuple) and sample_obj[2][0] == 'and' :
                for sample in output_disjunctions_set(sample_obj[1]):
                    if isinstance(sample, frozenset):
                        for sample2 in sample:
                            auxset3.add(sample2)
                    else:
                        auxset3.add(sample)
                return_set.add(frozenset(auxset3))
                for sample in output_disjunctions_set(sample_obj[2]):
                    if isinstance(sample, frozenset):
                        for sample2 in sample:
                            auxset4.add(sample2)
                    else:
                        auxset4.add(sample)
                return_set.add(frozenset(auxset4))
            elif isinstance(sample_obj[1], tuple) and sample_obj[1][0] == 'and':
                for sample in output_disjunctions_set(sample_obj[1]):
                    if isinstance(sample, frozenset):
                        for sample2 in sample:
                            auxset3.add(sample2)
                    else:
                        auxset3.add(sample)
                return_set.add(frozenset(auxset3))
                secondpart = remove_extra_tuple(output_disjunctions_set(sample_obj[2]), auxset2)
                for sample in secondpart:
                    if isinstance(sample, frozenset):
                        for sample2 in sample:
                            auxset4.add(sample2)
                    else:
                        auxset4.add(sample)
                return_set.add(frozenset(auxset4))
            elif isinstance(sample_obj[2], tuple) and sample_obj[2][0] == 'and':
                for sample in output_disjunctions_set(sample_obj[2]):
                    if isinstance(sample, frozenset):
                        for sample2 in sample:
                            auxset4.add(sample2)
                    else:
                        auxset4.add(sample)
                return_set.add(frozenset(auxset4))
                firstpart = remove_extra_tuple(output_disjunctions_set(sample_obj[1]), auxset1)
                for sample in firstpart:
                    if isinstance(sample, frozenset):
                        for sample2 in sample:
                            auxset3.add(sample2)
                    else:
                        auxset3.add(sample)
                return_set.add(frozenset(auxset3))
            else:
                firstpart = remove_extra_tuple(output_disjunctions_set(sample_obj[1]), auxset1)
                secondpart = remove_extra_tuple(output_disjunctions_set(sample_obj[2]), auxset2)
                for sample in firstpart:
                    if isinstance(sample, frozenset):
                        for sample2 in sample:
                            auxset3.add(sample2)
                    else:
                        auxset3.add(sample)
                return_set.add(frozenset(auxset3))
                for sample in secondpart:
                    if isinstance(sample, frozenset):
                        for sample2 in sample:
                            auxset4.add(sample2)
                    else:
                        auxset4.add(sample)
                return_set.add(frozenset(auxset4))
            return return_set
        elif sample_obj[0] == 'or':
            #in this format the 'or' represation is omited
            auxset1 = set()
            auxset2 = set()

            firstpart = remove_extra_tuple(output_disjunctions_set(sample_obj[1]), auxset1)
            secondpart = remove_extra_tuple(output_disjunctions_set(sample_obj[2]), auxset2)
            for sample in secondpart:
                firstpart.add(sample)
            return firstpart
        else:
            #negated literal case
            return  sample_obj

    elif isinstance(sample_obj, str):
        #literal found
        return  sample_obj
    else:
        #wrong format case
        return None

def remove_extra_tuple(sample_obj,outputset):
    if isinstance(sample_obj, set):
        auxset = set()
        for sample in sample_obj:
            auxset.add(sample)
        return auxset
    elif isinstance(sample_obj, tuple):
        if sample_obj[0] == 'not':
            outputset.add(sample_obj)
        elif isinstance(sample_obj[0], str) and isinstance(sample_obj[1], str):
            outputset.add(sample_obj[0])
            outputset.add(sample_obj[1])
        elif isinstance(sample_obj[0], str):
            outputset.add(sample_obj[0])
            outputset.union(remove_extra_tuple(sample_obj[1],outputset))
        elif isinstance(sample_obj[1], str):
            outputset.add(sample_obj[1])
            outputset.union(remove_extra_tuple(sample_obj[0],outputset))
        else:
            outputset.union(remove_extra_tuple(sample_obj[0],outputset))
            outputset.union(remove_extra_tuple(sample_obj[1],outputset))
        return outputset
    elif isinstance(sample_obj, str):
        outputset.add(sample_obj)
        return outputset
    else:
        #wrong format case
        return None
