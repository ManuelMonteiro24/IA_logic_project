""" A resolution-based theorem prover for propositional logic, assuming a
CNF knowledge base."""

import sys, fileinput

def literal_check(sample_obj):
    if len(sample_obj) == 1:
        return True
    else:
        return False

def negation_check(sample_obj):
    if len(sample_obj) == 2 and sample_obj[0] == 'not':
        return True
    else:
        return False

def conjunction_check(sample_obj):
    if len(sample_obj) == 3 and sample_obj[0] == 'and':
        return True
    else:
        return False

def disjunction_check(sample_obj):
    if len(sample_obj) == 3 and sample_obj[0] == 'or':
        return True
    else:
        return False

def implication_check(sample_obj):
    if len(sample_obj) == 3 and sample_obj[0] == '=>':
        return True
    else:
        return False

def equivalence_check(sample_obj):
    if len(sample_obj) == 3 and sample_obj[0] == '<=>':
        return True
    else:
        return False

def eliminate_equivalence(sample_obj):
    """Change >>, <<, and <=> into &, |, and ~. That is, return an Expr
    that is equivalent to s, but has only &, |, and ~ as logical operators.
    >>> eliminate_implications(A >> (~B << C))
    ((~B | ~C) | ~A)
    """
    if isinstance(sample_obj, tuple):
        if sample_obj[0] == 'not':
            return sample_obj[0], eliminate_equivalence(sample_obj[1])
        else:
            first_part = eliminate_equivalence(sample_obj[1])
            second_part = eliminate_equivalence  (sample_obj[2])

            if sample_obj[0] == '<=>':
                return 'and', ('=>', first_part, second_part), ('=>', second_part, first_part)
            else:
                sample_obj[0], first_part, second_part
        return sample_obj
    else:
        #wrong format case
        return None

def eliminate_implications(sample_obj):
    """Change >>, <<, and <=> into &, |, and ~. That is, return an Expr
    that is equivalent to s, but has only &, |, and ~ as logical operators.
    >>> eliminate_implications(A >> (~B << C))
    ((~B | ~C) | ~A)
    """
    if isinstance(sample_obj, tuple):
        if sample_obj[0] == 'not':
            return sample_obj[0], eliminate_implications(sample_obj[1])
        else:
            first_part = eliminate_implications(sample_obj[1])
            second_part = eliminate_implications(sample_obj[2])

            if sample_obj[0] == '=>':
                return 'or', ('not', first_part), second_part
            else:
                sample_obj[0], first_part, second_part
        return sample_obj
    else:
        #wrong format case
        return None

def move_not_inwards(sample_obj):
    """Change >>, <<, and <=> into &, |, and ~. That is, return an Expr
    that is equivalent to s, but has only &, |, and ~ as logical operators.
    >>> eliminate_implications(A >> (~B << C))
    ((~B | ~C) | ~A)
    """
    if isinstance(sample_obj, tuple):
        if isinstance(sample_obj[1], str) != true:
            if sample_obj[1][0] == 'not' and isinstance(sample_obj[1][1], str):
                return sample_obj[1][1]

            if sample_obj[0] == 'not':
                first_part = move_not_inwards(sample_obj[1][1])
                second_part = move_not_inwards(sample_obj[1][2])
                if sample_obj[1][0] == 'and':
                    return 'or', ('not', first_part), ('not', second_part)
                else:
                    return 'and', ('not', first_part), ('not', second_part)
            else:
                return sample_obj[0], move_not_inwards(sample_obj[1]), move_not_inwards(sample_obj[2])

        return sample_obj
    else:
        #wrong format case
        return None


def distribute_and_over_or(sample_obj):
    """Given a sentence s consisting of conjunctions and disjunctions
    of literals, return an equivalent sentence in CNF.
    >>> distribute_and_over_or((A & B) | C)
    ((A | C) & (B | C))
    """
    if isinstance(sample_obj, tuple):
        if sample_obj[0] == 'or':
            if(len(sample_obj[1]<=2)) and (len(sample_obj[2]<=2)):
                return sample_obj
            elif len(sample_obj[1]<=2):
                if sample_obj[2][0] == 'and':
                    return 'and', ('or', sample_obj[1], distribute_and_over_or(sample_obj[2][1])), ('or', sample_obj[1], distribute_and_over_or(sample_obj[2][2]))
                else:
                    return sample_obj[0], sample_obj[1], distribute_and_over_or(sample_obj[2])
            elif len(sample_obj[2]<=2):
                if sample_obj[1][0] == 'and':
                    return 'and', ('or', sample_obj[2], distribute_and_over_or(sample_obj[1][1])), ('or', sample_obj[2], distribute_and_over_or(sample_obj[1][2]))
                else:
                    return sample_obj[0], distribute_and_over_or(sample_obj[1]), sample_obj[2]
            else:
                if sample_obj[1][0] == 'and' and sample_obj[2][0] == 'and':
                    return 'and', ('and',('or', distribute_and_over_or(sample_obj[1][1]), distribute_and_over_or(sample_obj[2][1])), ('or', distribute_and_over_or(sample_obj[1][1]), distribute_and_over_or(sample_obj[2][2]))), ('and', ('or', distribute_and_over_or(sample_obj[1][2]), distribute_and_over_or(sample_obj[2][1])), ('or', distribute_and_over_or(sample_obj[1][2]), distribute_and_over_or(sample_obj[2][2])))
                elif sample_obj[1][0] == 'and':
                    return 'and', ('or',('or',distribute_and_over_or(sample_obj[2][1]),distribute_and_over_or(sample_obj[2][2])),distribute_and_over_or(sample_obj[1][1])), ('or',('or',distribute_and_over_or(sample_obj[2][1]),distribute_and_over_or(sample_obj[2][2])),distribute_and_over_or(sample_obj[1][2]))
                elif sample_obj[2][0] == 'and':
                    return 'and', ('or',('or',distribute_and_over_or(sample_obj[1][1]),distribute_and_over_or(sample_obj[1][2])),distribute_and_over_or(sample_obj[2][1])), ('or',('or',distribute_and_over_or(sample_obj[1][1]),distribute_and_over_or(sample_obj[1][2])),distribute_and_over_or(sample_obj[2][2]))
                else:
                    return sample_obj[0], distribute_and_over_or(sample_obj[1]), distribute_and_over_or(sample_obj[2])

        return sample_obj
    else:
        #wrong format case
        return None

#simplification rules

def simplification1(sample_obj):    

#read file from stdin line by line
for line in fileinput.input():
    sample_obj = eval(line)

    if literal_check(sample_obj):
        print ('literal')
    elif negation_check(sample_obj):
        print('negation')
    elif conjunction_check(sample_obj):
        print('conjunction')
    elif disjunction_check(sample_obj):
        print('disjunction')
    elif implication_check(sample_obj):
        print('implication')
    elif equivalence_check(sample_obj):
        print('equivalence')
    else:
        print('wrong format')

sys.stdout.write('here send CNF sentece')
