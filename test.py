# from resolution_util import Vertex
# from resolution_util import Graph
# from resolution_util import find_symmetric
from resolution_util2 import *
import sys, fileinput


graph = Graph()

#read file from stdin line by line
for line in fileinput.input():
	line = line.replace(' ', '')
	clause = line[0:-1]
	#print("Clause: ", clause)
	graph.add_vertex(clause)

problem = Resolution(graph.vertices, graph.num_vertices)

for i in graph.vertices:
	if len(problem.vertices[i].symmetric) == 1 or len(i) == 3:
		problem.knowledge_base.insert(0,i)
	else:
		problem.knowledge_base.append(i)
	#print("Vertex ", i)
	#print("Symmetric: ", graph.vertices[i].symmetric)

result = problem.resolution_algorithm()

print(result)

sys.exit(0)