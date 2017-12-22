def is_literal(clause):
	""" Returns positive if it is a literal. 
		1 or 2 if it is a positive literal and 3 if it is a negative literal. 
		If it is NOT a literal returns -1 
	"""
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
	""" Returns a set of the symmetric literals of a sentence"""

	#If clause if of type "'X'", returns {"('not','X')"}
	if is_literal(clause) == 2:
		aux = "('not'," + clause + ")"
		symmetric_set.add(aux)
		return symmetric_set

	#If clause if of type "('not','X')", returns {"'X'"}
	elif is_literal(clause) == 3:
		aux_clause = eval(clause)
		aux = "'" + aux_clause[1] + "'"
		symmetric_set.add(aux)
		return symmetric_set

	# It is a full sentence with []
	else:
		aux_clause = eval(clause)
		for i in range(len(aux_clause)):
			if isinstance(aux_clause[i], str):
				if aux_clause[i] == 'not':					
					symmetric_set.add( "'" + aux_clause[i+1] + "'")

				if aux_clause[i] != 'not':
					aux = "('not','" + aux_clause[i] + "')"
					symmetric_set.add(aux)

			else:
				symmetric_set = find_symmetric(str(aux_clause[i]), symmetric_set)
		return symmetric_set



#-----------------------------------------------------------
#-----------------------------------------------------------
class  Vertex():
	""" Class that characterizes the Vertices of the Graph """
	def __init__(self, clause_input):
		self.id = clause_input
		self.neighbors = list()
		self.symmetric = set()

	def __str__(self):
		return "Vertex id: %s neighbors: %s symmetric: %s" % (self.id, self.neighbors, self.symmetric)

	# Adds neighbors of a vertex
	def add_neighbor(self, neighbor):		
		if isinstance(neighbor, Vertex):
			if neighbor.id not in self.neighbors:
				#self.neighbors.append(neighbor.id)
				if is_literal(neighbor.id) == 2 or is_literal(neighbor.id) == 3:
					self.neighbors.insert(0,neighbor.id)
				else:
					self.neighbors.append(neighbor.id)

				return True
			return False
		else:
			return False


#-----------------------------------------------------------		
#-----------------------------------------------------------
class Graph():
	""" Class that characterizes the Graph of the problem. 
		The undirective graph is composed by vertex which are the sentences returned by the cnf converter """

	def __init__(self):
		self.vertices = dict()
		self.num_vertices = 0

	# Add vertex to graph, and connect to its neighbors
	def add_vertex(self, clause):
		explored_vertices = list()

		# No vertex with ID "clause" in graph
		if self.get_vertex(clause) is None:
			# New vertex with ID "clause"
			new_vertex = Vertex(clause)

			# Graph with vertices
			if self.num_vertices != 0:
				symmetric_set = set()
				# Find the set of negated literals of each positive or negative literal in sentence new_vertex.id
				new_vertex.symmetric = find_symmetric(clause, symmetric_set)	
				neighbor = 0

				# Find a neighbor. A neighbor is a vertex whose ID has at least a literal that is equal 
				#to one of the  new vertex ID's symmetric literals.
				for i in new_vertex.symmetric:

					for vertex_id in self.vertices:

						# explored_vertices is used to ensure that the new vertex won't add the same neighbor more than once
						if (vertex_id not in explored_vertices or explored_vertices == []):
							# if vertex in graph has a literal equal to the symmetric literal of the new vertex, then it is a neighbor
							if i == vertex_id and (is_literal(vertex_id) == 2 or is_literal(vertex_id) == 3):
								neighbor = 1
						
							else:
								#if vertex_id is a sentence with more than one literal
								if is_literal(vertex_id) == -1:
									aux_vertex = eval(vertex_id)

									for j in range(len(aux_vertex)):
										if not isinstance(aux_vertex[j],str):
											aux = str(aux_vertex[j])
											aux = aux.replace(' ', '')
											if aux == i:
												neighbor = 1
												break
										else:
											if is_literal(aux_vertex[j]) == 1:
												aux = "'" + aux_vertex[j] + "'"
											else:
												aux = aux_vertex
											if aux == i:
												neighbor = 1
												break

						# Add new neighbor to list of neighbors. New_vertex is a new neighbor of self.vertices[vertex_id] and
						#self.vertices[vertex_id] is a new neighbor of new_vertex
						if neighbor == 1:
							explored_vertices.append(vertex_id)
							new_vertex.add_neighbor(self.vertices[vertex_id])
							self.vertices[vertex_id].add_neighbor(new_vertex)
							neighbor = 0								

			# First vertex
			else:
				symmetric_set = set()
				new_vertex.symmetric = find_symmetric(clause, symmetric_set)
			
			self.num_vertices += 1
			self.vertices[new_vertex.id] = new_vertex
			return True

		else:
			return False


	# Checks if vertex with the same ID is already in the graph
	def get_vertex(self, clause):
		for vertex in self.vertices:
			if clause == vertex:
				return vertex
		return None



#-----------------------------------------------------------
#-----------------------------------------------------------
class Resolution(Graph):
	""" Class associated to the resolution problem """

	def __init__(self, vertices_input, n_vertices):
		self.clauses = tuple()
		self.knowledge_base = list()
		self.explored_clauses = list()
		self.vertices = vertices_input
		self.num_vertices = n_vertices
		#self.count_iter = 0

	# Resolution solver
	def resolution_algorithm(self):
		no_solution = 1
		for i in self.vertices:
			if self.vertices[i].neighbors != []:
				no_solution = 0
				break

		if no_solution == 0:

			for i in self.knowledge_base:
				# Choose a sentence i that was not already explored and a neighbor might or not been explored
				if i not in self.explored_clauses and self.vertices[i].neighbors != []:
					ci = self.vertices[i].id
					cj = self.vertices[i].neighbors[0]
					break
			
			result = self.resolve3(ci, cj)
			#self.count_iter += 1

			# continue resolution
			if result == False:
				return self.resolution_algorithm()
			# KB entails alpha
			else:
				#print("Iterations: ", self.count_iter)
				return True	
		#no solution
		else:
			#print("Iterations: ", self.count_iter)
			return False


	def resolve3(self, Ci, Cj):
		end_resolution = 0

		if is_literal(Ci) == -1:
			ci = eval(Ci)

		if is_literal(Cj) == -1:
			cj = eval(Cj)

		# End of resolution. (X == -X) or (-X == X) 
		# The resolution is only finished when two sentences with only one literal are the symmetric of one another
		if ( (is_literal(Ci) == 2 and list(self.vertices[Ci].symmetric)[0] == Cj) or (is_literal(Cj) == 2 and list(self.vertices[Ci].symmetric)[0] == Cj) ):
			return True

		# Every literal of sentences Ci and Cj are gathered in a set named literals. Then the symmetrics are eliminated
		# Eg: [X, Y, A, -X, B], the resulting set is [Y, A, B]. Only applicable because the converter eliminated tautolagies
		else:
			literals = set()

			# Add literals to set
			if is_literal(Ci) == 2 or is_literal(Ci) == 3:
				literals.add(Ci)
			else:
				for i in ci:
					if is_literal(i) == 1 and isinstance(i,str):
						i = "'" + i + "'"
					else:
						i = str(i)
						i = i.replace(' ','')						
					literals.add(i)

			if is_literal(Cj) == 2 or is_literal(Cj) == 3:
				literals.add(Cj)
			else:
				for j in cj:
					if is_literal(j) == 1 and isinstance(j,str):
						j = "'" + j + "'"
					else:
						j = str(j)
						j = j.replace(' ','')						

					literals.add(j)			

			aux_literals = list(literals)[:]
			aux_literals = set(aux_literals)
			for l in literals:
				sym_set = set()
				sym_set = find_symmetric(l, sym_set)

				# Remove symmetric literals
				if list(sym_set)[0] in aux_literals:
					aux_literals.remove(l)
					aux_literals.remove(list(sym_set)[0])					
		
			# Set is not empty -> new sentence. If set is empty nothing is done. The test of the end of resolution is done before.
			#This avoids resolution between -AvB and -BvA returning falsely true.
			if literals != set():
				new_clause = "["
				for i in list(aux_literals):
					new_clause += i + ","
				
				new_clause += "]"	
				new_clause.replace(' ','')

				if new_clause[-2] == "," and new_clause[-1] == "]":
					new_clause = new_clause[0:-2] + new_clause[-1]

				# Removes brackets [] if sentence has only one literal
				if len(eval(new_clause)) == 1:
					new_clause = new_clause[1:-1]

				# Checks if it is a new sentence. If it is, add it to knowledge_base (KB union Alpha)
				if new_clause not in self.knowledge_base:
					if self.add_vertex(new_clause):
						if is_literal(new_clause) == 2 or is_literal(new_clause) == 3:
							self.knowledge_base.insert(0,new_clause)
						else:
							self.knowledge_base.append(new_clause)

			# Remove neighbor. Avoids the same resolution happening twice								
			self.vertices[Ci].neighbors.remove(Cj)
			self.vertices[Cj].neighbors.remove(Ci)

			# Explored vertice when neighbors is an empty set.
			# If in following resolutions a neighbor of Ci (explored set) is created, there is no problem. 
			# Ci will be chosen as a Cj (neighbor of the new vertex) in resolution algorithm
			if self.vertices[Ci].neighbors == []:
				self.explored_clauses.append(Ci)
			
			return False
