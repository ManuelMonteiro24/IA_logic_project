""" A set of functions that implement the 4 simplifications rules of CNF sentences
in order to remove redudant cases from the knowledge base."""

def simplification1(knowledge_base):
    """Change the CNF sentece received trough the knowledge_base argument into a conjunction of disjunctions or literals,
    that doesn't has any clause that contains a literal that is not complementary with any other in the remanaing clauses.
    """
    if len(knowledge_base) == 0:
        #empty sentence case
        return knowledge_base

    #set that will hold the clauses that the conditon being check doesn't apply
    clauses_not_to_remove = set()

    #for each element (separated by conjunctions) in CNF sentence
    for sample in knowledge_base:
        if sample in clauses_not_to_remove:
            continue
        #negated literal or clause case
        if isinstance(sample, frozenset):
            #for each literal in the clause
            for sample1 in sample:
                if sample in clauses_not_to_remove:
                    break
                #generate the negation of the literal which we want to check, that is going to be hold by example1
                if isinstance(sample1, tuple):
                    example1 = sample1[1]
                else:
                    example1 = tuple(['not', sample1])

                #go trough the sentence (from the beginning) to compare the sample1 and example1 (its negation)
                #to all the literal in sentence to check if the one in sample1 and example1 has another occurence
                for sample2 in knowledge_base:
                    #negated literal or clause case
                    if isinstance(sample2, frozenset):
                        #for each literal in the clause
                        for sample3 in sample2:
                            if sample1 == sample3 or example1 == sample3:
                                clauses_not_to_remove.add(sample)
                                break
                    #literal case
                    else:
                        if sample1 == sample2 or example1 == sample2:
                            clauses_not_to_remove.add(sample)
                            break
        #literal case
        else:
            #goes trough the sentence (from the beginning) to compare the sample1 and its negation
            #to all the literal in sentence to check if the one in sample1 and its negation has another occurence
            for sample1 in knowledge_base:
                if sample in clauses_not_to_remove:
                    break
                #negated literal or clause case
                if isinstance(sample1, frozenset):
                    #for each literal in the clause
                    for sample2 in sample1:
                        if sample == sample2 or tuple(['not', sample]) == sample2:
                            clauses_not_to_remove.add(sample)
                            break

                #literal case
                else:
                    if sample == sample1 or tuple(['not', sample]) == sample1:
                        clauses_not_to_remove.add(sample)
                        break

    # set that will receive all the clauses that "survived" the conditon being checked, (simplified sentence)
    new_set = set()
    for sample in clauses_not_to_remove:
        new_set.add(sample)
    return new_set

def simplification2(knowledge_base):
    """Change the CNF sentece received through the knowledge_base argument into a conjunction of disjunctions or literals,
    that doesn't has tautologies (any clause that contains both the literal and its negation)."""
    if len(knowledge_base) == 0:
        #empty sentence case
        return knowledge_base

    #set that will hold the clauses identified with tautologies
    clauses_to_remove = set()

    #for each element (separated by conjunctions) in CNF sentence
    for sample in knowledge_base:
        #negated literal or clause case
        if isinstance(sample, frozenset):
            # for each literal in the clause, check if its negation occurs in the clause
            for sample1 in sample:
                for sample2 in sample:
                    #example holds the negation of the literal beign evaluated, to compare
                    #to the literals from the iteration of the clause
                    if isinstance(sample2, tuple):
                        example1 = sample2[1]
                    else:
                        example1 = tuple(['not', sample2])

                    if sample1 == example1:
                        clauses_to_remove.add(sample)
        #literal case
        else:
            continue

    #remove from the sentence the clauses identified with tautologies, (simplified sentence)
    for sample in clauses_to_remove:
        knowledge_base.remove(sample)
    return knowledge_base

def simplification3(knowledge_base):
    """Change the CNF sentece received trough the knowledge_base argument into a conjunction of disjunctions or literals,
    that doesn't has clauses implied by other clauses (any clause that is a subset of another, the largest clause can be eliminated)."""
    if len(knowledge_base) == 0:
        #empty sentence case
        return knowledge_base

    #set that will hold the clauses identified has the bigger sets of subsets that occur in the sentence
    clauses_to_remove = set()

    for sample in knowledge_base:
        #negated literal or clause case
        if isinstance(sample, frozenset) and len(sample) != 1:
            #goes trough the sentence (from the beginning), to check if the intersection between the clause being
            #checked and the others clauses are equal to the clause being checked, which tell us that the last one
            #is a bigger set to be removed
            for sample1 in knowledge_base:
                if sample1 != sample and isinstance(sample1, frozenset) and len(sample) <= len(sample1):
                    if sample1.intersection(sample) == sample:
                        clauses_to_remove.add(sample1)
        #literal case
        else:
            continue

    #remove from the sentence the clauses with the bigger sets of subtes that occur in the sentence, (simplified sentence)
    for sample in clauses_to_remove:
        knowledge_base.remove(sample)
    return knowledge_base


#with the use of frozenset's for the clause representation the forth simplification is already implemented
