""" A set of functions that implement the rules of transformation from propositional
logic to conjunctive normal form (CNF).
This is done trough a recursive process that goes trough the nested tuple with
the propositional logic, and when the relation or condition that the function is looking for
is found the transformation is done. The functions are propagated from the original tuple until the literals. """

#all this check functions are obsolote by now...
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
    """Change <=> into a conjunction of implications. That is, returns tuple object
    that is equivalent to sample_obj, but has only =>, &, |, and ~ as logical operators.
    >>> eliminate_implications(A <=> B)
    ( 'and', ( '=>' , A , B ), ( '=>' , B , A ) )
    """
    if isinstance(sample_obj, tuple):
        if sample_obj[0] == 'not':
            #not case, doesn't change anything
            return sample_obj[0], eliminate_equivalence(sample_obj[1])
        else:
            if sample_obj[0] == '<=>':
                #modification case
                return 'and', ('=>', eliminate_equivalence(sample_obj[1]), eliminate_equivalence(sample_obj[2])), ('=>', eliminate_equivalence(sample_obj[2]), eliminate_equivalence(sample_obj[1]))
            else:
                return sample_obj[0], eliminate_equivalence(sample_obj[1]), eliminate_equivalence(sample_obj[2])
    elif isinstance(sample_obj, str):
        #literal found
        return sample_obj
    else:
        #wrong format case
        return None

def eliminate_implications(sample_obj):
    """Change => into a disjunctions of literals. That is, returns tuple object
    that is equivalent to sample_obj, but has only &, |, and ~ as logical operators.
    >>> eliminate_implications(A => B)
    ( 'or' , ( 'not', A ) , B )
    """
    if isinstance(sample_obj, tuple):
        if sample_obj[0] == 'not':
            #not case, doesn't change anything
            return sample_obj[0], eliminate_implications(sample_obj[1])
        else:
            if sample_obj[0] == '=>':
                #modification case
                return 'or', ('not', eliminate_implications(sample_obj[1])), eliminate_implications(sample_obj[2])
            else:
                return sample_obj[0], eliminate_implications(sample_obj[1]), eliminate_implications(sample_obj[2])
    elif isinstance(sample_obj, str):
        #literal found
        return sample_obj
    else:
        #wrong format case
        return None

def move_not_inwards(sample_obj):
    """ Moves negations inside all relations. That is, returns tuple object
    that is equivalent to sample_obj, but has only negations on literals (not on disjunctions or conjunctions).
    >>> eliminate_implications( 'not' , ( 'not' , ( 'A' ) ) )
    'A'
    >>> eliminate_implications( 'not', ( 'and', 'A' , 'B' ) )
    ( 'or' , ( 'not' , 'A' ) , ( 'not' , 'B') )
    >>> eliminate_implications( 'not', ( 'or', 'A' , 'B' ) )
    ( 'and' , ( 'not' , 'A' ) , ( 'not' , 'B') )
    """
    if isinstance(sample_obj, tuple):
        if sample_obj[0] == 'not':
            if isinstance(sample_obj[1], str):
                #doesn't change anything
                return sample_obj
            elif len(sample_obj[1]) == 2:
                return move_not_inwards(sample_obj[1][1])
            else:
                if sample_obj[1][0] == 'and':
                    #'and' modification case
                    return 'or', ('not', move_not_inwards(sample_obj[1][1])), ('not', move_not_inwards(sample_obj[1][2]))
                else:
                    #'or' modification case
                    return 'and', ('not', move_not_inwards(sample_obj[1][1])), ('not', move_not_inwards(sample_obj[1][2]))

        return sample_obj[0], move_not_inwards(sample_obj[1]), move_not_inwards(sample_obj[2])

    elif isinstance(sample_obj, str):
        #literal found
        return sample_obj
    else:
        #wrong format case
        return None


def distribute_and_over_or(sample_obj):
    """Given a sentence s consisting of conjunctions and disjunctions
    of literals, return an equivalent sentence in CNF.
    >>> distribute_and_over_or( 'or' , ( 'and', 'A' , 'B' ) , 'C')
    ( 'and', ( 'or', 'A' , 'C' ) , ( 'or', 'B' , 'C' ) )
    """
    if isinstance(sample_obj, tuple):
        if sample_obj[0] == 'or':
            if(len(sample_obj[1])<=2) and (len(sample_obj[2])<=2):
                #doesn't change anything
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
        elif sample_obj[0] == 'not':
            return sample_obj[0], distribute_and_over_or(sample_obj[1])
        else:
            return sample_obj[0], distribute_and_over_or(sample_obj[1]), distribute_and_over_or(sample_obj[2])

    elif isinstance(sample_obj, str):
        #literal found
        return sample_obj
    else:
        #wrong format case
        return None
