# Returns a set of atomic senteces given by the literals of a clause
def search_atom(clause, atom_set = set()):
	aux_clause = eval(clause)
	#print("\t\t",aux_clause)
	for i in aux_clause:
		#print("\t\t",i)
		if isinstance(i, str):
			#print("\t\t0")
			if i != 'not':
				#print("\t\t1")
				atom_set.add( "'" + i + "'")
				#print("\t\t", atom_set)

		else:
			#print("\t\t2")
			aux = str(i)
			aux = aux.replace(' ', '')
			aux_set, _ = search_atom(aux)
			atom_set = atom_set.union(aux_set)
			#atom_set,_ = atom_set.union(search_atom(aux))
			#print("\t\t", atom_set)

	#print("\t\tAtom set: ", atom_set, len(list(atom_set)))
	return atom_set, len(list(atom_set))



def find_symmetric(clause, symmetric_set):
	n = 1

	if len(clause) == 3:
		aux = "('not'," + clause + ")"
		symmetric_set.add(aux)
		return symmetric_set

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
		#print("\tN vertices: ", self.num_vertices)

		if self.get_vertex(clause) is None:
			#print("\t0")
			new_vertex = Vertex(clause)
			if self.num_vertices != 0:
				#print("\t1")
				symmetric_set = set()
				new_vertex.symmetric = find_symmetric(clause, symmetric_set)

				#print("\t3")
				neighbor = 0
				for i in new_vertex.symmetric:

					for vertex_id in self.vertices:

						if (vertex_id not in explored_vertices or explored_vertices == []):
							if i == vertex_id and len(vertex_id) == 3:
								neighbor = 1

							else:
								if len(vertex_id) > 3:
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
											if len(aux_vertex[j]) == 1:
												aux_vertex[j] = "'" + aux_vertex[j] + "'"

											#print(i, aux_vertex[j])
											if aux_vertex[j] == i:
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

			else:
				symmetric_set = set()
				new_vertex.symmetric = find_symmetric(clause, symmetric_set)

			self.num_vertices += 1
			self.vertices[new_vertex.id] = new_vertex
			#print("\t",new_vertex)
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

		if len(Ci) > 3:
			ci = eval(Ci)

		if len(Cj) > 3:
			cj = eval(Cj)

		#print(len(Ci), len(Cj))
		#print(list(self.vertices[Ci].symmetric)[0])
		#print(list(self.vertices[Cj].symmetric)[0])

		if (len(Ci) == 3 and len(eval(Cj)) == 1 and list(self.vertices[Ci].symmetric)[0] in Cj ) or (len(Cj) == 3 and list(self.vertices[Ci].symmetric)[0] == Cj):
			#End of resolution
			#print("End resolution 0")
			return True

		else:
			literals = set()

			if len(eval(Ci)) == 1 and Ci == Cj:
				return True

			if len(Ci) == 3:
				literals.add(Ci)
			else:
				for i in ci:
					if len(i) == 1:
						i = "'" + i + "'"
					else:
						i = str(i)
						i = i.replace(' ','')
					literals.add(i)

			if len(Cj) == 3:
				literals.add(Cj)
			else:
				for j in cj:
					if len(j) == 1:
						j = "'" + j + "'"
					else:
						j = str(j)
						j = j.replace(' ','')

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

						if len(new_clause) == 3 or ('not' in new_clause and len(eval(new_clause)) == 2):
							self.knowledge_base.insert(0,new_clause)
						else:
							self.knowledge_base.append(new_clause)

						#print(self.vertices[new_clause])


			self.vertices[Ci].neighbors.remove(Cj)
			self.vertices[Cj].neighbors.remove(Ci)
			#print(self.vertices[Ci].neighbors)
			#print(self.vertices[Cj].neighbors)

			if self.vertices[Ci].neighbors == []:
				#print("ci explored")
				self.explored_clauses.append(Ci)

			return False

	# def resolve2(self, ci, cj):

	# 	end_resolution = -1

	# 	for i in self.vertices[ci].symmetric:

	# 		print(i, cj)
	# 		print(len(i), len(cj))

	# 		if len(cj) > 3:

	# 			if (i in cj and 'not' in i) or (i in cj and 'not' not in i and cj[cj.index(i)-6:cj.index(i)-1] != 'not'):
	# 				end_resolution = 0
	# 				new_clause = self.remove_literal(cj,i)
	# 				print("1", new_clause)
	# 		else:
	# 			if i in cj:
	# 				end_resolution = 1


	# 		if end_resolution == 1 or new_clause == "[]":
	# 			print("End resolution!")
	# 			return True

	# 		if end_resolution == 0 and new_clause not in self.knowledge_base:
	# 			print(2)
	# 			if self.add_vertex(new_clause):
	# 				print("New clause: ", new_clause)

	# 				if len(new_clause) == 3 or ('not' in new_clause and len(eval(new_clause)) == 2):
	# 					self.knowledge_base.insert(0,new_clause)
	# 				else:
	# 					self.knowledge_base.append(new_clause)

	# 				print(self.vertices[new_clause])

	# 	# print("4", cj,ci)
	# 	# self.vertices[ci].neighbors.remove(cj)
	# 	# self.vertices[cj].neighbors.remove(ci)

	# 	# if self.vertices[ci].neighbors == []:
	# 	# 	print("Remove ci")
	# 	# 	self.explored_clauses.append(ci)

	# 	return False


	# def remove_literal(self, clause, literal):
	# 	new_clause = ""

	# 	if len(clause) == 1:
	# 		clause = '"' + clause +'"'

	# 	print("\tLiteral: ", literal)
	# 	for i in range(len(clause)-len(literal)):

	# 		print("\tClause: ", clause[i:i+len(literal)])

	# 		if clause[i:i+len(literal)] == literal:
	# 			print("\t1")
	# 			new_clause += clause[i+len(literal):]
	# 			n_range = range(1,len(new_clause)-1)
	# 			for i in n_range:
	# 				if (new_clause[i] == "," and new_clause[i+1] == "]") or (new_clause[i] == "," and new_clause[i-1] == "["):
	# 					new_clause = new_clause[0:i] + new_clause[i+1:]

	# 			print("\t",new_clause)
	# 			print("\tSearch atom")
	# 			atom_set = set()
	# 			_, n_literals = search_atom(new_clause, atom_set)
	# 			print("\tN literals:", n_literals)

	# 			if n_literals == 1:
	# 				new_clause = new_clause[1:-1]
	# 				print("\t",new_clause)

	# 			return new_clause

	# 		else:
	# 			print("\t2")
	# 			new_clause += clause[i]

	# 	return False
