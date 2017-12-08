""" A set of functions that implement the rules of transformation from propositional
logic to conjunctive normal form (CNF).
This is done trough a recursive process that goes trough the nested tuple with
the propositional logic, and when the relation or condition that the function is looking for
is found the transformation is done. The functions are propagated from the original tuple until the literals. """

def eliminate_equivalence(sample_obj):
    """Change <=> into a conjunction of implications. That is, returns tuple object
    that is equivalent to sample_obj, but has only =>, &, |, and ~ as logical operators.
    >>> eliminate_implications(A <=> B)
    ( 'and', ( '=>' , A , B ), ( '=>' , B , A ) )
    """
    if isinstance(sample_obj, tuple):
        if sample_obj[0] == 'not':

            #not case, doesn't change anything, just propagate the function
            return sample_obj[0], eliminate_equivalence(sample_obj[1])
        else:
            if sample_obj[0] == '<=>':

                #modification case
                return 'and', ('=>', eliminate_equivalence(sample_obj[1]), eliminate_equivalence(sample_obj[2])), ('=>', eliminate_equivalence(sample_obj[2]), eliminate_equivalence(sample_obj[1]))
            else:

                #just propagate the function
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

            #not case, doesn't change anything, just propagate the function
            return sample_obj[0], eliminate_implications(sample_obj[1])
        else:
            if sample_obj[0] == '=>':

                #modification case
                return 'or', ('not', eliminate_implications(sample_obj[1])), eliminate_implications(sample_obj[2])
            else:

                #just propagate the function
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
            elif isinstance(sample_obj[1], tuple) and sample_obj[1][0] == 'not' :
                #two nested negations case, just propagate the function
                return move_not_inwards(sample_obj[1][1])
            else:
                if sample_obj[1][0] == 'and':

                    #'and' modification case
                    return 'or',  move_not_inwards(('not',sample_obj[1][1])), move_not_inwards(('not', sample_obj[1][2]))
                else:

                    #'or' modification case
                    return 'and', move_not_inwards(('not',sample_obj[1][1])), move_not_inwards(('not', sample_obj[1][2]))

        return sample_obj[0], move_not_inwards(sample_obj[1]), move_not_inwards(sample_obj[2])

    elif isinstance(sample_obj, str):

        #literal found
        return sample_obj
    else:

        #wrong format case
        return None


def distribute_and_over_or(sample_obj):
    """Given a sentence consisting of conjunctions and disjunctions
    of literals, return an equivalent sentence as conjunctions of disjunctions.
    >>> distribute_and_over_or( 'or' , ( 'and', 'A' , 'B' ) , 'C')
    ( 'and', ( 'or', 'A' , 'C' ) , ( 'or', 'B' , 'C' ) )
    """
    if isinstance(sample_obj, tuple):
        if sample_obj[0] == 'or':

            #doesn't change anything, or of literals (simple or negated)
            #No more relations, except not, nested
            if (len(sample_obj[1])<=2 and len(sample_obj[2])<=2) or (isinstance(sample_obj[1], str) and isinstance(sample_obj[2], str)):
                return sample_obj

            #first part of the relation its a literal or negated literals
            #the function only need to be propagated to the second part
            elif len(sample_obj[1]) <=2 or isinstance(sample_obj[1], str):
                if sample_obj[2][0] == 'and':

                    #distribute and over or case
                    return 'and', distribute_and_over_or(('or', sample_obj[1], sample_obj[2][1])), distribute_and_over_or(('or', sample_obj[1], sample_obj[2][2]))
                else:
                    return sample_obj[0], sample_obj[1], distribute_and_over_or(sample_obj[2])

            #second part of the relation its a literal or negated literals
            #the function only need to be propagated to the first part
            elif len(sample_obj[2])<=2 or isinstance(sample_obj[2], str):
                if sample_obj[1][0] == 'and':

                    #distribute and over or case
                    return 'and', distribute_and_over_or(('or', sample_obj[2], sample_obj[1][1])), distribute_and_over_or(('or', sample_obj[2], sample_obj[1][2]))
                else:
                    return sample_obj[0], distribute_and_over_or(sample_obj[1]), sample_obj[2]

            #its a relation of relation the function needs to be propagated to both parts
            else:
                if sample_obj[1][0] == 'and' and sample_obj[2][0] == 'and':

                    #distribute and over or case
                    return 'and', ('and', distribute_and_over_or(('or', sample_obj[1][1], sample_obj[2][1])), distribute_and_over_or(('or',sample_obj[1][1], sample_obj[2][2]))), ('and', distribute_and_over_or(('or', sample_obj[1][2], sample_obj[2][1])), distribute_and_over_or(('or', sample_obj[1][2], sample_obj[2][2])))
                elif sample_obj[1][0] == 'and':

                    #distribute and over or case
                    return 'and', distribute_and_over_or(('or', ('or', sample_obj[2][1], sample_obj[2][2]), sample_obj[1][1])), distribute_and_over_or(('or', ('or', sample_obj[2][1], sample_obj[2][2]), sample_obj[1][2]))
                elif sample_obj[2][0] == 'and':

                    #distribute and over or case
                    return 'and', distribute_and_over_or(('or',('or', sample_obj[1][1] , sample_obj[1][2]), sample_obj[2][1])), distribute_and_over_or(('or', ('or', sample_obj[1][1] , sample_obj[1][2]), sample_obj[2][2]))
                else:
                    return sample_obj[0], distribute_and_over_or(sample_obj[1]), distribute_and_over_or(sample_obj[2])

        #not case, just propagate the function
        elif sample_obj[0] == 'not':
            return sample_obj

        #and case, just propagate the function
        else:
            return sample_obj[0], distribute_and_over_or(sample_obj[1]), distribute_and_over_or(sample_obj[2])

    elif isinstance(sample_obj, str):
        #literal found
        return sample_obj
    else:
        #wrong format case
        return None

def check_or_after_and(sample_obj):
    """ Utility function that checks if the distributive prop. still need to be applied."""

    if isinstance(sample_obj,str):
        return False
    elif isinstance(sample_obj,tuple):
        if len(sample_obj) == 2:
            if isinstance(sample_obj[1],str):
                return False
            else:
                return check_or_after_and(sample_obj[1])
        elif sample_obj[0] == 'or':
            if sample_obj[1][0] == 'and' or sample_obj[2][0] == 'and':
                return True
            else:
                return check_or_after_and(sample_obj[1]) or check_or_after_and(sample_obj[2])
        else:
            return check_or_after_and(sample_obj[1]) or check_or_after_and(sample_obj[2])
    else:
        return False
