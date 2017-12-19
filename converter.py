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
    print("first eliminate_equivalence: ", sample_obj_cnf_1)
    print()
    sample_obj_cnf_2 = to_cnf.eliminate_implications(sample_obj_cnf_1)
    print("first eliminate_implications: ", sample_obj_cnf_2)
    print()
    sample_obj_cnf_3 = to_cnf.move_not_inwards(sample_obj_cnf_2)
    print("first move_not_inwards: ", sample_obj_cnf_3)
    print()
    sample_obj_cnf_final = to_cnf.distribute_and_over_or(sample_obj_cnf_3)
    print("first distribute_and_over_or: ", sample_obj_cnf_final)
    print()
    sample_obj = utils.output_disjunctions_set(sample_obj_cnf_final)[0]

    flag = 0
    for sample in sample_obj:
        if isinstance(sample, frozenset) and len(sample) != 1:
            flag =1
    if flag== 0:
        sample_obj = frozenset(sample_obj)

    #add readed line to knowledge_base
    if isinstance(sample_obj, set):
        #clauses or negated literals case
        for sample in sample_obj:
            if isinstance(sample, frozenset) and len(sample) == 1:
                aux = next(iter(sample))
                if isinstance(aux, tuple):
                    knowledge_base.add(sample)
                else:
                    knowledge_base.add(aux)
            else:
                knowledge_base.add(sample)
    else:
        #simple literal case (dont comtemplates negated literals)
        knowledge_base.add(sample_obj)

print("kb", knowledge_base)
print()
#output CNF sentece to stdout in the pretended format
knowledge_base_simplified1 = simplifications.simplification1(knowledge_base)
print("first kb_simpled: ", knowledge_base_simplified1)
print()
knowledge_base_simplified2 = simplifications.simplification2(knowledge_base_simplified1)
print("second kb_simpled: ", knowledge_base_simplified2)
print()
knowledge_base_simplified3 = simplifications.simplification3(knowledge_base_simplified2)
print("final kb_simpled: ", knowledge_base_simplified3)
print()
sys.stdout.write(utils.output_KB(knowledge_base_simplified3 ))
fh=open("result.txt",'w')
fh.write(utils.output_KB(knowledge_base_simplified3 ))
fh.close()
sys.exit()
