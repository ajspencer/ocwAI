# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    #for BFS we use a queue and insure that we follow FIFO
    queue = [ [start ] ]
    current = [start]
    while(current[len(current) - 1] != goal):
        #pick from the front of the line
        current = queue.pop(0)
        for child in graph.get_connected_nodes(current[len(current) - 1]):
            if(child in current): continue
            newPath = current + [child];
            #add to the back
            queue.append(newPath)
    return current

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    stack = [ [start ] ]
    current = [start]
    while(current[len(current) - 1] != goal):
        #pick from the back of the line
        current = stack.pop()
        #print "current: " + current + "goal: " + goal
        for child in graph.get_connected_nodes(current[len(current) - 1]):
            if(child in current): continue
            newPath = current + [child];
            #add to the back
            stack.append(newPath)
    return current


## Now we're going to add some heuristics into the search.
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    stack = [ [start ] ]
    current = [start]
    while(current[len(current) - 1] != goal):
        #pick from the back of the line
        current = stack.pop()
        #print "current: " + current + "goal: " + goal
        childrenToAdd = []
        for child in graph.get_connected_nodes(current[len(current) - 1]):
            if(child in current): continue
            newPath = current + [child];
            childrenToAdd.append(newPath)
        #sort the children we are adding based on the heuristic
        childrenToAdd.sort(key=lambda child: graph.get_heuristic(child[len(child)-1], goal))
        for child in childrenToAdd[::-1]:
            stack.append(child)
    return current

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    queue = [ [start ] ]
    current = [start]
    paths = [ [], [start] ]
    while(current[len(current) - 1] != goal):
        #pick from the front of the line
        if(len(queue) == 0): return []
        current = queue.pop(0)
        #print("\nour current path is " + str(current))
        pathsToAdd = []
        #Get all of the child nodes
        for child in graph.get_connected_nodes(current[len(current) - 1]):
            if(child in current): continue
            newPath = current + [child];
            pathsToAdd.append(newPath)
        #If there are already paths at this level, add them to our list
        if(len(paths) > len(current) + 1):
            pathsToAdd = pathsToAdd + paths.pop(len(current) + 1)
        #sort the children we are adding based on the heuristic
        pathsToAdd = list(pathsToAdd)
        pathsToAdd.sort(key=lambda child: graph.get_heuristic(child[len(child)-1], goal))
        #REALLY IMPORTANT STEP YO
        values = [graph.get_heuristic(child[len(child) - 1], goal) for child in pathsToAdd]
        for child in pathsToAdd[0:beam_width]:
                queue.append(child)
        paths.insert(len(current)+ 1,  pathsToAdd[0:beam_width])
        queue = [path for path in queue if path in paths[len(path)]]
    #Remove all paths we don't want to see anymore from the queue
    return current

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    return sum([graph.get_edge(node_names[i], node_names[i+1]).length for i in range(len(node_names)-1)])


def branch_and_bound(graph, start, goal):
    queue = [ [start] ]
    #while the shortest path doesn't end at the goal
    while(queue[0][len(queue[0]) -1] != goal):
        current = queue.pop(0)
        for child in graph.get_connected_nodes(current[len(current) - 1]):
            if child in current: continue
            newPath = current + [child]
            queue.append(newPath)
        queue.sort(key=lambda path: path_length(graph, path))
        if(len(queue) == 0): return []
    return queue[0]
def a_star(graph, start, goal):
    queue = [ [start] ]
    extendedList = set([])
    #while the shortest path doesn't end at the goal
    while(queue[0][len(queue[0]) -1] != goal):
        current = queue.pop(0)
        for child in graph.get_connected_nodes(current[len(current) - 1]):
            if child in extendedList: continue
            newPath = current + [child]
            queue.append(newPath)
            extendedList.add(child)
        queue.sort(key=lambda path: path_length(graph, path) + graph.get_heuristic(path[len(path)-1], goal))
        if(len(queue) == 0): return []
    return queue[0]


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    distances = {}
    for node in graph.nodes:
        path = a_star(graph, node, goal)
        distances[node] = path_length(graph, path)
    for node, distance in distances.iteritems():
        if(distance < graph.get_heuristic(node, goal)):
            return False
    return True

def is_consistent(graph, goal):
    return False not in [False if abs(graph.get_heuristic(edge.node1, goal) - graph.get_heuristic(edge.node2, goal)) > edge.length else True for edge in graph.edges]

HOW_MANY_HOURS_THIS_PSET_TOOK = '4'
WHAT_I_FOUND_INTERESTING = 'Finally making myself code all these searches'
WHAT_I_FOUND_BORING = 'I had a lot of stupid bugs I had to debug'
