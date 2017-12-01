class Resolution()

	def __init__(self):
		self.clauses = tuple()


	def resolution_algorithm(self):
		ci, cj = self.choose_pair()
		result = self.resolve(ci, cj)

		if ci != None or cj != None:
			if result == False:
				return True
			else
				self.clauses = self.clauses + result 
		else:
			return False


	def resolve(self, ci, cj):

	def in_unit(self, ci)
		if len(ci) == 3:
			return True
		else
			return False


	def add_clause(self, clause_input):
		self.clauses = self.clauses + clause_input

		for i in self.clauses:


#-----------------------------------------------------------
class  Vertex():
	def __init__(self, clause_input):
		self.id = clause_input
		self.neighbors = list()

	def add_neighbor(self, clause_input):
		#Add neighbor (clause_input) to Vertex

		
#-----------------------------------------------------------
class Graph():

	def __init__(self):
		self.vertices = dict()
		self.num_vertices = 0

		pass

	def add_vertex(self, clause):
        if self.get_vertex(clause) is None:
            self.num_vertices += 1            
            new_vertex = Vertex(clause)
     
            if new_vertex.id.count("'") == 2:
            	for i in range(len(self.vertices)):
            		if new_vertex.id in self.vertices[i]:
            			self.vertices[i].add_neighbor(new_vertex.id)
            			new_vertex.add_neighbor(self.vertices[i].id)

           	else:
           		atom_set = set()
           		atom_set = search_atom(clause)
	            aux_vertices = list(self.vertices)
	        	for i in atom_set:
	        		for j in aux_vertices:
	        			if i in j:
	        				self.vertices[j].add_neighbor(new_vertex.id)
            				new_vertex.add_neighbor(self.vertices[j].id)
            				aux_vertices.remove(j)

            self.vertices = self.vertices + new_vertex
            return new_vertex
        return


    def get_vertex(self, vertex_id):
    	if clause in self.vertices:
            return True
        else:
            return None



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



def find_symmetric(clause, symmetric_set = set()):
	if len(clause) == 3:
		aux = "('not'," + aux_clause[i] + ")"
		symmetric_set.add(aux)
		return symmetric_set

	else:
		aux_clause = eval(clause)
		for i in range(len(aux_clause)):
			if isinstance(aux_clause[i], str):
				if aux_clause[i] == 0 and aux_clause[i] == 'not':
					symmetric_set.add(aux_clause[i+1])
					return symmetric_set

				if aux_clause[i] == 0 and aux_clause[i] != 'not':
					aux = "('not','" + aux_clause[i] + "')"
					symmetric_set.add(aux)
					return symmetric_set

			else:
				symmetric_set = find_symmetric(str(aux_clause[i]))

		return symmetric_set
