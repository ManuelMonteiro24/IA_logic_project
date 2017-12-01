""" A set of functions that implement the 4 simplifications rules of CNF sentences
in order to remove redudant cases from the knowledge base."""

def simplification1(knowledge_base):
    if len(knowledge_base) == 0:
        return knowledge_base
    clauses_not_to_remove = set()
    for sample in knowledge_base:
        if isinstance(sample, frozenset):
            for sample1 in sample:
                if isinstance(sample1, tuple):
                    example1 = sample1[1]
                else:
                    example1 = tuple(['not', sample1])
                for sample2 in knowledge_base:
                    if isinstance(sample2, frozenset):
                        for sample3 in sample2:
                            if sample1 == sample3 or example1 == sample3:
                                clauses_not_to_remove.add(sample)
                    else:
                        if sample1 == sample2 or example1 == sample2:
                            clauses_not_to_remove.add(sample)
        else:
            for sample1 in knowledge_base:
                if isinstance(sample1, frozenset):
                    for sample2 in sample1:
                        if sample == sample2 or tuple(['not', sample]) == sample2:
                            clauses_not_to_remove.add(sample)
                else:
                    if sample == sample1 or tuple(['not', sample]) == sample1:
                        clauses_not_to_remove.add(sample)

    new_set = set()
    for sample in clauses_not_to_remove:
        new_set.add(sample)
    return new_set

def simplification2(knowledge_base):
    if len(knowledge_base) == 0:
        return knowledge_base
    clauses_to_remove = set()
    for sample in knowledge_base:
        if isinstance(sample, frozenset):
            for sample1 in sample:
                for sample2 in sample:
                    if isinstance(sample2, tuple):
                        example1 = sample2[1]
                    else:
                        example1 = tuple(['not', sample2])
                    if sample1 == example1:
                        clauses_to_remove.add(sample)
        else:
            continue
    for sample in clauses_to_remove:
        knowledge_base.remove(sample)
    return knowledge_base

#utilize intersections
def simplification3(knowledge_base):
    if len(knowledge_base) == 0:
        return knowledge_base
    clauses_to_remove = set()
    for sample in knowledge_base:
        if isinstance(sample, frozenset):
            for sample1 in knowledge_base:
                if sample1 != sample and isinstance(sample1, frozenset) and len(sample) <= len(sample1):
                    if sample1.intersection(sample) == sample:
                        clauses_to_remove.add(sample1)
        else:
            continue
    for sample in clauses_to_remove:
        knowledge_base.remove(sample)
    return knowledge_base


#with the use of frozenset's for the clause representation the forth simplification is already implemented
