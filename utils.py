""" A set of utility functions to the converter program."""

import sys

def output_KB(knowledge_base):
    """ Returns a string with the cnf sentence received in the sample_obj argument
    in a format which is the same of the prover.py input."""

    return_str = ""

    #empty string case
    if len(knowledge_base) == 0:
        return return_str
    else:
        #auxliar iterator to help with \n to the desired output format
        aux_iter0 = 0

        #for each clause or literals in the sentece
        for sample in knowledge_base:
            aux_iter0 = aux_iter0 + 1

            #simple literal case
            if isinstance(sample,str):
                return_str += "'" + sample + "'\n"
                #if aux_iter0 > len(knowledge_base):
                    #return_str += "\n"
            elif isinstance(sample,tuple):
                return_str += str(sample) + "\n"
                #if aux_iter0 > len(knowledge_base):
                    #return_str += "\n"

            #frozenset case
            else:
                if len(sample) == 1 and isinstance(list(sample)[0],tuple):
                    return_str += str(list(sample)[0]) + "\n"
                else:
                    return_str += "["
                    #second auxiliar iterator to help with commas to the desired output format
                    aux_iter = 0
                    for sample1 in sample:
                        aux_iter = aux_iter + 1
                        if isinstance(sample1, str):
                            return_str +=  "'" + sample1 + "'"
                        else:
                            return_str += str(sample1)
                        if aux_iter != len(sample):
                            return_str += ", "

                    #string sentence finished
                    return_str += "]\n"

        return return_str

#function used for debug in the beginning obsolete in the final version of the program
def output_disjunctions_str(sample_obj):
    """ Returns a string with the cnf sentence received (in the sentence input format) in the sample_obj argument
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
    """ Returns a set with the cnf sentence received in the sample_obj argument.
    This set represents the cnf where the elements (separated by conjunction), are of the type
    string if simply literals or the type frozenset if clauses or negated literals.
    This process is done recursively as the transformation functions described in the to_cnf.py file."""

    #clause or negated literal case
    if isinstance(sample_obj, tuple):
        if sample_obj[0] == 'and':
            if isinstance(sample_obj[1], tuple) and sample_obj[1][0] == 'and' and isinstance(sample_obj[2], tuple) and sample_obj[2][0] == 'and' :
                return receive_set(receive_set(set(), output_disjunctions_set(sample_obj[1])), output_disjunctions_set(sample_obj[2]) ), 'and'

            elif isinstance(sample_obj[1], tuple) and sample_obj[1][0] == 'and':
                return receive_set(receive_set(set(), output_disjunctions_set(sample_obj[1])), remove_extra_tuple(output_disjunctions_set(sample_obj[2])[0], set()) ), 'and'

            elif isinstance(sample_obj[2], tuple) and sample_obj[2][0] == 'and':
                return receive_set(receive_set(set(), output_disjunctions_set(sample_obj[2])), remove_extra_tuple(output_disjunctions_set(sample_obj[1])[0], set()) ), 'and'

            else:
                return receive_set(receive_set(set(), remove_extra_tuple(output_disjunctions_set(sample_obj[1])[0], set())), remove_extra_tuple(output_disjunctions_set(sample_obj[2])[0], set()) ), 'and'

        elif sample_obj[0] == 'or':
            #in this format the 'or' represation is omited

            firstpart = remove_extra_tuple(output_disjunctions_set(sample_obj[1])[0], set())
            for sample in remove_extra_tuple(output_disjunctions_set(sample_obj[2])[0], set())[0]:
                firstpart[0].add(sample)
            return firstpart[0], 'or'
        else:
            #negated literal case
            return  sample_obj, 'not'

    elif isinstance(sample_obj, str):

        #literal found
        return  sample_obj, 'str'
    else:

        #wrong format case
        return None, None

def receive_set(old_set, last_return):
    """ Utility function that receives a set in old_set parameter that will receive new values from the last_return parameter."""

    if last_return[1] == 'or':
        auxset = set()
        for sample in last_return[0]:
                auxset.add(sample)
        old_set.add(frozenset(auxset))
        return old_set

    elif last_return[1] == 'str':
        auxset = set()
        for sample in last_return[0]:
                old_set.add(sample)
        return old_set

    for sample in last_return[0]:
        if isinstance(sample, frozenset):
            auxset = set()
            for sample2 in sample:
                auxset.add(sample2)
            old_set.add(frozenset(auxset))
        else:
            old_set.add(sample)

    return old_set

def remove_extra_tuple(sample_obj,outputset):
    """ Utility function that removes the excess of () from the "or" tuple relation
    with the objective to represent the clauses as a frozenset of simple (string) or negated literals (tuple).
    This process is done recursively as the the output_disjunctions_set function.
    The outputset argument receives the a set that the function will use to add the desired literals, when finished the function will return this set.
    """
    if isinstance(sample_obj, set):
        auxset = set()
        for sample in sample_obj:
            auxset.add(sample)
        return auxset, 'or'
    elif isinstance(sample_obj, tuple):
        if sample_obj[0] == 'not':
            outputset.add(sample_obj)
        elif isinstance(sample_obj[0], str) and isinstance(sample_obj[1], str):
            outputset.add(sample_obj[0]),
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
        return outputset, 'or'
    elif isinstance(sample_obj, str):
        outputset.add(sample_obj)
        return outputset, 'str'
    else:

        #wrong format case
        return None, None
