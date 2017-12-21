def is_literal(clause):
	''' Returns positive if it is a literal. 
		1 or 2 if it is a positive literal and 3 if it is a negative literal. 
		If it is NOT a literal returns -1 
	'''

	count = 0
	for i in clause:
		if i == "'":
			count += 1
	
	# In some situations it is received a clause 'X' instead of "'X'", eg when executing eval function to "('not','X')
	# If the clause is 'X', returns 1; if it is "'X'"", returns 2
	if count == 0:
		return 1
	if count == 2:
		return 2
	if count == 4 and 'not' in clause:
		return 3
	return -1


def find_symmetric(clause, symmetric_set):
	''' Returns a set of the symmetric literals of a sentence '''
	n = 1

	#If clause if of type "'X'", returns { "('not','X')"}
	if is_literal(clause) == 2:
		aux = "('not'," + clause + ")"
		symmetric_set.add(aux)
		return symmetric_set

	#Either a negative literal or a full sentence with [] '''
	else:
		#print(symmetric_set)
		aux_clause = eval(clause)
		for i in range(len(aux_clause)):
			#print(i,aux_clause[i])
			if isinstance(aux_clause[i], str):
				#print("0")
				if aux_clause[i] == 'not' and n == 1:					
					symmetric_set.add( "'" + aux_clause[i+1] + "'")
					#print("1 ", symmetric_set)
					n = 0

				if aux_clause[i] != 'not' and n == 1:
					aux = "('not','" + aux_clause[i] + "')"
					symmetric_set.add(aux)
					#print("2 ", symmetric_set)
					n = 0

			else:
				#print("3 ", symmetric_set)
				symmetric_set = find_symmetric(str(aux_clause[i]), symmetric_set)
				#print("4 ", symmetric_set)

		#print("final: ", symmetric_set)
		return symmetric_set



#-----------------------------------------------------------
#-----------------------------------------------------------
class  Vertex():
	''' Class that characterizes the Vertices of the Graph'''
	def __init__(self, clause_input):
		self.id = clause_input
		self.neighbors = list()
		self.symmetric = set()

	def __str__(self):
		return "Vertex id: %s neighbors: %s symmetric: %s" % (self.id, self.neighbors, self.symmetric)

	# Adds neightbors of a vertex
	def add_neighbor(self, neighbor):		
		if isinstance(neighbor, Vertex):
			if neighbor.id not in self.neighbors:
				self.neighbors.append(neighbor.id)
				return True
			return False
		else:
			return False


#-----------------------------------------------------------		
#-----------------------------------------------------------
class Graph():
	''' Class that characterizes the Graph of the problem. 
		The undirective graph is composed by vertex which are the sentences returned by the cnf converter '''

	def __init__(self):
		self.vertices = dict()
		self.num_vertices = 0

	# Add vertex to graph, and connect to its neighbors
	def add_vertex(self, clause):
		explored_vertices = list()
		#print("\tN vertices: ", self.num_vertices)

		# No vertex with id clause in graph
		if self.get_vertex(clause) is None:
			#print("\t0")
			new_vertex = Vertex(clause)

			# Graph with vertices
			if self.num_vertices != 0:
				#print("\t1")
				symmetric_set = set()
				new_vertex.symmetric = find_symmetric(clause, symmetric_set)	
					
				#print("\t3")
				neighbor = 0

				for i in new_vertex.symmetric:

					for vertex_id in self.vertices:

						# explored_vertices is used to ensure that the new vertex won't add the same neighbor more than once
						if (vertex_id not in explored_vertices or explored_vertices == []):
							# if vertex in graph has a literal equal to the symmetric literal of the new vertex, then it is a neighbor
							if i == vertex_id and (is_literal(vertex_id) == 2 or is_literal(vertex_id) == 3):
								neighbor = 1
						
							else:
								#print("0",is_literal(vertex_id), vertex_id)
								if is_literal(vertex_id) == -1:
									#print("1",is_literal(vertex_id), vertex_id,"\n")
									aux_vertex = eval(vertex_id)

									for j in range(len(aux_vertex)):
										if not isinstance(aux_vertex[j],str):
											#print(i, str(aux_vertex[j]))
											aux = str(aux_vertex[j])
											aux = aux.replace(' ', '')
											if aux == i:
												neighbor = 1
												break
										else:
											
											#print(aux_vertex,aux_vertex[j])
											if is_literal(aux_vertex[j]) == 1:
												aux = "'" + aux_vertex[j] + "'"
											else:
												aux = aux_vertex
											#print(i, aux_vertex[j])
											if aux == i:
												neighbor = 1
												break

						if neighbor == 1:
							explored_vertices.append(vertex_id)
							new_vertex.add_neighbor(self.vertices[vertex_id])
							self.vertices[vertex_id].add_neighbor(new_vertex)
							#print("NEIGH")
							#print(self.vertices[vertex_id])
							#print(new_vertex)
							neighbor = 0								

			# First vertex
			else:
				symmetric_set = set()
				new_vertex.symmetric = find_symmetric(clause, symmetric_set)
			
			self.num_vertices += 1
			self.vertices[new_vertex.id] = new_vertex
			#print("\t",new_vertex)
			return True

		else:
			return False


	# Checks if vertex with the same id as clause is already in the graph
	def get_vertex(self, clause):
		for vertex in self.vertices:
			if clause == vertex:
				return vertex
		return None



#-----------------------------------------------------------
#-----------------------------------------------------------
class Resolution(Graph):

	def __init__(self, vertices_input, n_vertices):
		self.clauses = tuple()
		self.knowledge_base = list()
		self.explored_clauses = list()
		self.vertices = vertices_input
		self.num_vertices = n_vertices

	def resolution_algorithm(self):
		#no solution
		no_solution = 1
		for i in self.vertices:
			if self.vertices[i].neighbors != []:
				no_solution = 0
				break

		if no_solution == 0:

			for i in self.knowledge_base:
				if i not in self.explored_clauses and self.vertices[i].neighbors != []:
					ci = self.vertices[i].id
					#print(self.vertices[i])
					cj = self.vertices[i].neighbors[0]
					break
			#print("\n")
			#print(self.vertices[ci])
			#print("KB: ", self.knowledge_base, "ci: ", ci, "cj: ", cj)
			#print("Explored clauses: ", self.explored_clauses)
			
			result = self.resolve3(ci, cj)

			if result == False:
				return self.resolution_algorithm()
			else:
				return True	
		else:
			#print("No solution!!")
			return False


	def resolve3(self, Ci, Cj):

		end_resolution = 0
		#print("\tRESOLVE3 ", Ci, Cj)

		if is_literal(Ci) == -1:
			ci = eval(Ci)

		if is_literal(Cj) == -1:
			cj = eval(Cj)


		if ( (is_literal(Ci) == 2 and list(self.vertices[Ci].symmetric)[0] == Cj) or (is_literal(Cj) == 2 and list(self.vertices[Ci].symmetric)[0] == Cj) ):
			#End of resolution
			#print("End resolution 0")
			return True

		else:
			literals = set()
			#print("Is literal 0: ", Ci, is_literal(Ci))
			if is_literal(Ci) == 2 or is_literal(Ci) == 3:
				literals.add(Ci)
			else:
				for i in ci:
					if is_literal(i) == 1 and isinstance(i,str):
						i = "'" + i + "'"
					else:
						i = str(i)
						i = i.replace(' ','')
						#print("0: ",i, is_literal(i))
						
					literals.add(i)

			#print("Is literal 1: ", Cj, is_literal(Cj))
			if is_literal(Cj) == 2 or is_literal(Cj) == 3:
				literals.add(Cj)
			else:
				for j in cj:
					if is_literal(j) == 1 and isinstance(j,str):
						j = "'" + j + "'"
					else:
						j = str(j)
						j = j.replace(' ','')
						#print("1: ",j, is_literal(j))
						

					literals.add(j)			

			#print("\tLiterals: ", literals)
			
			aux_literals = list(literals)[:]
			aux_literals = set(aux_literals)
			for l in literals:
				#print("\t",l, isinstance(l,str))
				sym_set = set()
				sym_set = find_symmetric(l, sym_set)
				#print("\tsym ", sym_set)

				if list(sym_set)[0] in aux_literals:
					#print("\t1", l, list(sym_set)[0])
					aux_literals.remove(l)
					aux_literals.remove(list(sym_set)[0])					
					#print(literals)
					#print(aux_literals)
			

			if literals != set():
				#New sentence
				new_clause = "["
				for i in list(aux_literals):
					new_clause += i + ","
				
				new_clause += "]"	
				new_clause.replace(' ','')

				if new_clause[-2] == "," and new_clause[-1] == "]":
					new_clause = new_clause[0:-2] + new_clause[-1]

				if len(eval(new_clause)) == 1:
					new_clause = new_clause[1:-1]

				#print("New clause: ", new_clause)

				if new_clause not in self.knowledge_base:
					if self.add_vertex(new_clause):
						#print("New clause: ", new_clause)
						if is_literal(new_clause) == 2 or is_literal(new_clause) == 3:
							self.knowledge_base.insert(0,new_clause)
						else:
							self.knowledge_base.append(new_clause)

						#print(self.vertices[new_clause])

								
			self.vertices[Ci].neighbors.remove(Cj)
			self.vertices[Cj].neighbors.remove(Ci)
			#print(self.vertices[Ci].neighbors)
			#print(self.vertices[Cj].neighbors)

			if self.vertices[Ci].neighbors == []:
				print("ci explored")		
				self.explored_clauses.append(Ci)
			
			return False
