from classify import *
from math import log

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False
    variable = state.get_current_variable()
    if(variable == None): return True
    value = variable.get_assigned_value()
    constraints = state.get_constraints_by_name(variable.get_name())
    #for every constraint, get all possible values for the other constraint and check if they work
    for constraint in constraints:
        otherVariable = state.get_variable_by_name(constraint.get_variable_j_name())
        domain = otherVariable.get_domain()
        for otherVariableValue in domain:
            if not constraint.check(state, value, otherVariableValue):
                otherVariable.reduce_domain(otherVariableValue)
            if otherVariable.domain_size() == 0:
                return False
    return True


# Now Implement forward checking + (constraint) propagation through
# singleton domains.
#idk what's wrong with this one man
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False
    # Add your propagate singleton logic here.
    visited = []
    singleVariables = [x for x in state.get_all_variables() if x.domain_size() == 1 and visited.count(x) == 0]
    while len(singleVariables) > 0:
        variable = singleVariables[0]
        singleVariables.remove(singleVariables[0])
        value = variable.get_assigned_value()
        visited.append(variable)
        if(value == None): continue
        constraints = state.get_constraints_by_name(variable.get_name())
        for constraint in constraints:
            otherVariable = state.get_variable_by_name(constraint.get_variable_j_name())
            domain = otherVariable.get_domain()
            for otherVariableValue in domain:
                print("value: " + str(value) + " other variable value: " + str(otherVariableValue))
                print(otherVariableValue)
                #it's never reducing the domain and I'm not sure why
                if not constraint.check(state, value, otherVariableValue):
                    print("I reduced the domain")
                    otherVariable.reduce_domain(otherVariableValue)
                else:
                    print(constraint.check(state, value, otherVariableValue))
                if otherVariable.domain_size() == 0:
                    return False
        preLen = len(singleVariables)
        singleVariables.extend([x for x in state.get_all_variables() if x.domain_size() == 1 and visited.count(x) == 0 and singleVariables.count(x) == 0])
        print ("extended by: " + str(len(singleVariables) - preLen))
    return True

## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    # this is not the right solution!
    mySum = 0
    for item1, item2 in zip(list1, list2):
        mySum += (item1 - item2)**2
    return (mySum)**.5
#Once you have implemented euclidean_distance, you can check the results:
#evaluate(nearest_neighbors(euclidean_distance, 2), senate_group1, senate_group2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(euclidean_distance, 5)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    classes = [yes, no]
    disorder = 0
    for c in classes:
        numRep = 0
        numDem = 0
        for person in c:
            if(person == "Republican"): numRep += 1
            else: numDem += 1
        repDisorder = 0
        demDisorder = 0
        if(numRep > 0):
            repDisorder = -float(numRep)/len(c)*math.log(float(numRep)/float(len(c)),2)
        if(numDem > 0):
            demDisorder = -float(numDem)/len(c)*math.log(float(numDem)/float(len(c)),2)
        disorder += float(len(c))/(len(yes)+len(no)) * (repDisorder+demDisorder)
    return disorder

#print CongressIDTree(senate_people, senate_votes, information_disorder)
print(information_disorder(["Democrat", "Republican"], ["Republican",
    "Democrat"]))
#evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print

    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)


## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 50
rep_classified = limited_house_classifier(house_people, house_votes, N_1)
print(rep_classified)

## Find a value of n that classifies at least 90 senators correctly.
N_1 = 67
senator_classified = limited_house_classifier(senate_people, senate_votes, 67)
print(senator_classified)

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 24
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)


## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn


