# from resolution_util import Vertex
# from resolution_util import Graph
# from resolution_util import find_symmetric
from resolution_util import *
import sys

graph = Graph()


def read_cnf():
	file = open("Testes/p2_result.txt","r")
	i = 0
	symmetric_clause = set()

	for line in file:
		i += 1
		line = line.replace(' ', '')
		clause = line[0:-1]
		#print(clause)
		graph.add_vertex(clause)
		#print("\n")


read_cnf()

problem = Resolution(graph.vertices, graph.num_vertices)
for i in graph.vertices:
	if len(eval(i)) == 1:
		problem.knowledge_base.insert(0,i)
	else:
		problem.knowledge_base.append(i)
	#print("Vertex ", i)
	#print("Symmetric: ", graph.vertices[i].symmetric)

result = problem.resolution_algorithm()

#print("AA",result)

if result == True:
	print("True")

if result == False:
	print("No solution")

sys.exit(0)