""" A resolution-based theorem prover for propositional logic, assuming a
CNF knowledge base."""

import sys, fileinput, to_cnf, simplifications, utils


knowledge_base = set()
#read file from stdin line by line
for line in fileinput.input():

    #transform read line in a tuple object
    sample_obj = eval(line)

    if isinstance(sample_obj, str):
        #if a simple literal (dont comtemplates negated literals) was read print right away
        sys.stdout.write("'" + sample_obj + "'" + "\n")
        knowledge_base.add(sample_obj)
        continue

    sys.stdout.write(utils.output_disjunctions_str(to_cnf.distribute_and_over_or(to_cnf.move_not_inwards(to_cnf.eliminate_implications(to_cnf.eliminate_equivalence(sample_obj))))) + "\n")
    sample_obj = utils.output_disjunctions_set(to_cnf.distribute_and_over_or(to_cnf.move_not_inwards(to_cnf.eliminate_implications(to_cnf.eliminate_equivalence(sample_obj)))))
    if isinstance(sample_obj, set):
        for sample in sample_obj:
            knowledge_base.add(sample)
    else:
        knowledge_base.add(sample_obj)

print(knowledge_base)
sys.exit()
