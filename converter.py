""" A resolution-based theorem prover for propositional logic, assuming a
CNF knowledge base."""

import sys, fileinput

#read file from stdin line by line
for line in fileinput.input():
    sample_obj = eval(line)
    print(sample_obj)

sys.stdout.write('here send CNF sentece')
