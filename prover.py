""" A program to convert logical sentences in propositional logic into the
clausal normal form (CNF)."""
from resolution_util import *
import sys, fileinput


graph = Graph()

#read file from stdin line by line
for line in fileinput.input():
	line = line.replace(' ', '')
	clause = line[0:-1]
	graph.add_vertex(clause)

problem = Resolution(graph.vertices, graph.num_vertices)

for i in graph.vertices:
	if len(eval(i)) == 1:
		problem.knowledge_base.insert(0,i)
	else:
		problem.knowledge_base.append(i)

# Resolution result
result = problem.resolution_algorithm()

if result == True:
	print("True")

if result == False:
	print("No solution")

sys.exit(0)