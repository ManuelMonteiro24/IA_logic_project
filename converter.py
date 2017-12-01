""" A resolution-based theorem prover for propositional logic, assuming a
CNF knowledge base."""

import sys, fileinput, to_cnf, simplifications, utils

knowledge_base = set()

#read file from stdin line by line
for line in fileinput.input():

    #transform read line in a tuple object
    sample_obj = eval(line)

    if isinstance(sample_obj, str):
        #if a simple literal was read print right away (dont comtemplates negated literals)
        knowledge_base.add(sample_obj)
        continue

    sample_obj = utils.output_disjunctions_set(to_cnf.distribute_and_over_or(to_cnf.move_not_inwards(to_cnf.eliminate_implications(to_cnf.eliminate_equivalence(sample_obj)))))

    #add readed line to knowledge_base
    if isinstance(sample_obj, set):
        #clauses or negated literals case
        for sample in sample_obj:

            knowledge_base.add(sample)
    else:
        #simple literal case (dont comtemplates negated literals)
        knowledge_base.add(sample_obj)

#output CNF sentece to stdout in the pretended format
sys.stdout.write(utils.output_KB(simplifications.simplification3(simplifications.simplification2(simplifications.simplification1(knowledge_base)))))
sys.exit()
