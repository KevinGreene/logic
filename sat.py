from random import randint
from random import sample
from copy import deepcopy

class SatClause:
    def __init__(self, *args):
        '''
        *args is expected to be the variables in the clause
        '''

        self.clause = set()
        for arg in args:
            self.clause.add(arg)

    def __str__(self):
        '''
        Represents the variable in (x v y v z) form
        '''

        s = str(self.clause)
        s = s.replace(", ", " v ")
        s = s.replace("{", "(")
        s = s.replace("}", ")")
        return s

    def __eq__(self, other):
        '''
        Two SAT clauses are equal if they have the same variables
        '''

        return self.clause == other.clause

    def evaluate(self, variableMap):
        '''
        Evaluates the SAT clause based on the given variable map.

        The variable map is expected to have both true and false values, i.e.
        if x: True is present, then !x: False should also be present.

        This evaluate reduces it as much as possible, then returns
        whether it is already satisfied by the variable map.
        Note that this is not the same as satisfiable!
        '''

        false_vars = []
        for v in self.clause:
            if v in variableMap:
                if variableMap[v]:
                    return True
                else:
                    false_vars.append(v)
        for v in false_vars:
            self.clause.remove(v)
        return False

    def isEmpty(self):
        return len(clause)==0

def generateClause(n, length = 3):
    '''
    Generates a SAT clause by randomly selecting variables without replacement
    from the first n letters (starting with ASCII A).
    Default length of SAT is 3, due to the prevalence of 3-SAT in computing
    '''

    vars_in_clause = []
    clause = SatClause()
    while len(vars_in_clause) < length:
        x = chr(randint(65, 65+n))
        if(not (x in vars_in_clause)):
            vars_in_clause.append(x)
            if randint(0,1):
                clause.clause.add("!" + x)
            else:
                clause.clause.add(x)
    return clause

def dpll(clauses, variable_map):
    '''
    Returns the satisfiability of a SAT problem.

    Args:
        clauses: The given SatClause objects to be satisfied
        variable_map: The map of variables that are already determined
    Returns:
        The satisfiability of the given input, and if so, the variable map
    '''

    satisfied_clauses = []
    new_clauses = []
    for clause in clauses:
        if clause.evaluate(variable_map):
            satisfied_clauses.append(clause)
        else:
            if len(clause.clause)==0:
                return False
            new_clauses.append(clause)

    if(len(new_clauses)==0):
        return True

    first = new_clauses[0]
    elem = sample(first.clause,1)[0]
    not_elem = elem
    if elem[0] == "!":
        not_elem = elem[1]
    else:
        not_elem = "!" + elem

    positive_map = deepcopy(variable_map)
    positive_map[elem] = True
    positive_map[not_elem] = False

    negative_map = deepcopy(variable_map)
    negative_map[elem] = False
    negative_map[not_elem] = True

    pos = dpll(deepcopy(new_clauses), positive_map)
    neg = dpll(deepcopy(new_clauses), negative_map)
    return pos or neg





if __name__ == "__main__":
    clauses = []
    for i in range(5):
        clauses.append(generateClause(26))
    for clause in clauses:
        print(clause)
    print(dpll(clauses, {}))
    clauses = []
    for i in range(26):
        clauses.append(generateClause(3))
    print(dpll(clauses,{}))
    clauses = []

# This represents an unsatisfiable set of clauses
    clauses.append(SatClause("A","B","C"))
    clauses.append(SatClause("A","B","!C"))
    clauses.append(SatClause("A","!B","C"))
    clauses.append(SatClause("A","!B","!C"))
    clauses.append(SatClause("!A","B","C"))
    clauses.append(SatClause("!A","B","!C"))
    clauses.append(SatClause("!A","!B","C"))
    clauses.append(SatClause("!A","!B","!C"))

    print(dpll(clauses,{}))

