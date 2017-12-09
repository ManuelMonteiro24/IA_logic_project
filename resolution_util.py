# Returns a set of atomic senteces given by the literals of a clause
def search_atom(clause, atom_set = set()):
	aux_clause = eval(clause)
	for i in aux_clause:
		if isinstance(i, str):
			if i != 'not':
				atom_set.add(i)
		else:
			atom_set = atom_set.union(search_atom(str(i)))

	return atom_set



def find_symmetric(clause, symmetric_set):
	if len(clause) == 3:
		aux = "('not'," + clause + ")"
		symmetric_set.add(aux)
		return symmetric_set

	else:
		aux_clause = eval(clause)
		for i in range(len(aux_clause)):
			if isinstance(aux_clause[i], str):
				if aux_clause[i] == 'not':
					symmetric_set.add(aux_clause[i+1])
					return symmetric_set

				if aux_clause[i] != 'not':
					aux = "('not','" + aux_clause[i] + "')"
					symmetric_set.add(aux)
					return symmetric_set

			else:
				symmetric_set = find_symmetric(str(aux_clause[i]), symmetric_set)

		return symmetric_set



#-----------------------------------------------------------
#-----------------------------------------------------------
class  Vertex():
	def __init__(self, clause_input):
		self.id = clause_input
		self.neighbors = list()
		self.symmetric = set()

	def __str__(self):
		return "Vertex id: %s neighbors: %s symmetric: %s" % (self.id, self.neighbors, self.symmetric)

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

	def __init__(self):
		self.vertices = dict()
		self.num_vertices = 0

	def add_vertex(self, clause):
		explored_vertices = list()
		print("N vertices: ", self.num_vertices)

		if self.get_vertex(clause) is None:
			new_vertex = Vertex(clause)
			if self.num_vertices != 0:
				symmetric_set = set()
				new_vertex.symmetric = find_symmetric(clause, symmetric_set)	
			
				if len(new_vertex.id) == 3:
					for vertex_id in self.vertices:						
						clause_elements = eval(vertex_id)

						for j in clause_elements:
							aux = str(j)
							aux = aux.replace(' ', '')
							if list(new_vertex.symmetric)[0] == aux:
								new_vertex.add_neighbor(self.vertices[vertex_id])
								self.vertices[vertex_id].add_neighbor(new_vertex)
								break

				else:
					neighbor = 0
					for i in new_vertex.symmetric:

						for vertex_id in self.vertices:
						
							if vertex_id not in explored_vertices or explored_vertices == []:
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
										#print(i, aux_vertex[j])
										if aux_vertex[j] == i:
											neighbor = 1
											break

								if neighbor == 1:
									explored_vertices.append(vertex_id)
									new_vertex.add_neighbor(self.vertices[vertex_id])
									self.vertices[vertex_id].add_neighbor(new_vertex)
									neighbor = 0									

			else:
				symmetric_set = set()
				new_vertex.symmetric = find_symmetric(clause, symmetric_set)
			
			self.num_vertices += 1
			self.vertices[new_vertex.id] = new_vertex
			return True

		else:
			return False



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
		if self.knowledge_base == []:
			print("asd")
			return False

		ci = self.vertices[self.knowledge_base[0]]
		cj_id = ci.neighbors[0]

		print("\nKB: ", self.knowledge_base, "ci: ", ci.id, "cj: ", cj_id)
		print(ci)
		print("Explored clauses: ", self.explored_clauses)
		
		result = self.resolve(ci.id, cj_id)

		if result == False:
			return self.resolution_algorithm()
		else:
			return True	

	def resolve(self, ci, cj):
		new_clause = "["
		end_resolution = 1
		count_clauses = 0

		if len(cj) > 3:
			aux_cj = eval(cj)
			print("len > 3")

		print(self.vertices[ci].symmetric)

		for i in self.vertices[ci].symmetric:

			if len(cj) > 3:
				for j in aux_cj:

					print(i, j)

					if not isinstance(j,str):
						j = str(j)
						j = j.replace(' ', '')

					if j !=  i:
						print("0")
						if count_clauses != 0:
							print("1")
							new_clause += ","
						
						if len(j) == 1:
							print("2")
							new_clause += "'"+ j + "'"
						else:
							print("3")
							new_clause += j

						end_resolution = 0
						count_clauses += 1

			else:
				print("len <= 3")
				if j !=  i:
					print("i: ", i, "j: ", j)
					end_resolution = 0
					new_clause += "'"+ j + "'"
					print(new_clause)

			if end_resolution == 1:
				return True

			new_clause += "]"
			
			if len(new_clause) == 5:
				print("Prev ", new_clause)
				new_clause = new_clause[1:-1]	
				print("After ", new_clause)	

			if new_clause not in self.knowledge_base and new_clause not in self.explored_clauses:
				if self.add_vertex(new_clause):
					if self.vertices[new_clause].neighbors == []:
						continue
					if len(new_clause) == 3:
						self.knowledge_base.insert(0,new_clause)
					else:
						self.knowledge_base.append(new_clause)

					print(self.vertices[new_clause])

			new_clause = "["
			count_clauses = 0

		self.vertices[ci].neighbors.remove(cj)
		self.vertices[cj].neighbors.remove(ci)

		if self.vertices[ci].neighbors == []:
			print("Remove ci")
			self.knowledge_base.remove(ci)			
			self.explored_clauses.append(ci)
			del self.vertices[ci]

		if self.vertices[cj].neighbors == []:
			print("Remove cj")
			self.knowledge_base.remove(cj)
			del self.vertices[cj]
			

		return False
			
