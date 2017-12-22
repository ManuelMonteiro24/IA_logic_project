""" A resolution-based theorem prover for propositional logic, assuming a
CNF knowledge base."""

import sys, fileinput, to_cnf, simplifications, utils

knowledge_base = set()

#read file from stdin line by line
for line in fileinput.input():

    #transform read line in a tuple object
    try:
        sample_obj = eval(line)
    except:
        print("Error: Program coudln't use eval() function on input file, check input format on project report, (use tuple/string tree.")
        sys.exit()

    sample_obj_cnf_1 = to_cnf.eliminate_equivalence(sample_obj)
    sample_obj_cnf_2 = to_cnf.eliminate_implications(sample_obj_cnf_1)
    sample_obj_cnf_3 = to_cnf.move_not_inwards(sample_obj_cnf_2)
    sample_obj_cnf_final = to_cnf.distribute_and_over_or(sample_obj_cnf_3)
    sample_obj = utils.output_disjunctions_set(sample_obj_cnf_final)

    #add readed line to knowledge_base
    if len(sample_obj) == 3:
        #final relation its a or
        for sample in sample_obj:
            if isinstance(sample, frozenset):
                knowledge_base.add(sample)
                break
    else:
        #get set,str or tuple clause
        if isinstance(sample_obj[0], str) and ( sample_obj[0] == 'or' or sample_obj[0] == 'not' or sample_obj[0] == 'str' or sample_obj[0] == 'and'):
            sample_obj = sample_obj[1]

        else:
            sample_obj = sample_obj[0]

        if isinstance(sample_obj, set):

            #set clause case
            for sample in sample_obj:
                    knowledge_base.add(sample)

        elif isinstance(sample_obj, tuple):

            #tuple clause case
            knowledge_base.add(sample_obj)
        else:

            #literal clause case
            knowledge_base.add(sample_obj)


knowledge_base_simplified1 = simplifications.simplification1(knowledge_base)
knowledge_base_simplified2 = simplifications.simplification2(knowledge_base_simplified1)
knowledge_base_simplified3 = simplifications.simplification3(knowledge_base_simplified2)
sys.stdout.write(utils.output_KB(knowledge_base_simplified3))
sys.exit()
