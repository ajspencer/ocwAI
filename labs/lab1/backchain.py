from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

def backchain_to_goal_tree(rules, hypothesis):
    treeNode = OR(hypothesis)
    #For every rule in the tree, see which ones have consequents that match my hypothesis
    matches = []
    #iterate through every rule and collect the ones whose consequents match my hypothesis
    for rule in rules:
        #Fill in each consequent of the rule with the correct name of the antecendents
        for consequent in rule.consequent():
            matchAttempt = match(consequent, hypothesis)
            #If we can match one of the consequents, we want to fill in the atecedents with the appropriate hypothesis
            if(matchAttempt != None and not rule in matches):
                for i, expression in enumerate(rule.antecedent()):
                    rule.antecedent()[i] = populate(expression, matchAttempt)
                matches.append(rule)
    #At this point  we have a list of the rules that match, and all of the antecendents are filled in with the variable names we can fill them in with
    treeNode = OR(hypothesis)
    for ruleMatch in matches:
        antecedent = ruleMatch.antecedent()
        if( isinstance(antecedent, AND)):
            node = AND()
        else:
            node = OR()
        for newHypothesis in antecedent:
            node.append(backchain_to_goal_tree(rules, newHypothesis))
        treeNode.append(node)
    return simplify(treeNode)



# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
