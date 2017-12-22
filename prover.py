from resolution_util import *
import sys, fileinput


graph = Graph()

# Read file from stdin line by line
for line in fileinput.input():
	line = line.replace(' ', '')
	clause = line[0:-1]
	graph.add_vertex(clause)

problem = Resolution(graph.vertices, graph.num_vertices)

for i in graph.vertices:
	if is_literal(problem.vertices[i].id) == 2 or is_literal(problem.vertices[i].id) == 3:
		problem.knowledge_base.insert(0,i)
	else:
		problem.knowledge_base.append(i)

result = problem.resolution_algorithm()

print(result)

sys.exit(0)