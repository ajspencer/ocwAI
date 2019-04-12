# 6.034 Fall 2010 Lab 3: Games
# Name: <Your Name>
# Email: <Your Email>

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
##
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """
    #We decide to optimize for trying to get the longest chain, so we score the board based on the value of the longest chain
    myChain = board.longest_chain(board.get_current_player_id())
    if(myChain == 4): return 1000
    theirChain = board.longest_chain(board.get_other_player_id())
    if(theirChain == 4): return -1000
    return myChain if myChain >= theirChain else -theirChain


## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)


def alpha_beta_helper(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn, alpha, beta, isMax):
    #If we are at a leaf, we run the static evaluator
    if(is_terminal_fn(depth, board)):
        #if we are at a minimizing level, update our master's alpha by returning a beta and do the reverse if we are at a max
        return (-alpha, -eval_fn(board)) if not isMax else (-eval_fn(board), -beta)

    #If we are not at a leaf: we continue if we are a max level only if our alpha < beta, if we are a min level we continue only if our beta < alpha
    #if it's a maximizer, we pass down updated values of alpha, if it's a minimizer we pass down updated values of beta
    for move, new_board in get_next_moves_fn(board):
        if( (isMax and alpha >= beta) or (not isMax and beta <= alpha)): return (-alpha, -beta)
        newAlphaBeta = alpha_beta_helper(new_board, depth -1, eval_fn, get_next_moves_fn, is_terminal_fn, alpha, beta, not isMax)
        #print "newAlpha: " + str(newAlphaBeta[0]) + "newbeta: " + str(newAlphaBeta[1]) + "ismax: " + str(isMax)
        if(isMax and newAlphaBeta[1] > alpha): alpha = newAlphaBeta[1]
        elif(not isMax and newAlphaBeta[0] < beta): beta = newAlphaBeta[0]
        #print("nowAlphaIs: " + str(alpha) + "nowBetaIS: " + str(beta))
    return (-alpha, -beta)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.
def alpha_beta_search(board, depth, eval_fn, get_next_moves_fn=get_all_next_moves, is_terminal_fn=is_terminal):

    alpha = -100000
    beta = 100000
    bestPosition = (alpha, None, None)
    for move, new_board in get_next_moves_fn(board):
        score = alpha_beta_helper(new_board, depth - 1, eval_fn, get_next_moves_fn, is_terminal_fn, alpha, beta, False)
        bestPosition = bestPosition if bestPosition[0] >= score[1] else (score[1], move, new_board)
        alpha = bestPosition[0]
    return bestPosition[1]


## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

def better_evaluate(board):
    myLongestChain = board.longest_chain(board.get_current_player_id())
    if(myLongestChain >= 4): return 1000
    theirLongestChain = board.longest_chain(board.get_other_player_id())
    if(theirLongestChain >= 4): return -1000
    c = 0
    for i in range(6):
        for j in range(7):
            c += count_at(i, j, board.get_current_player_id(), board)
            c -= count_at(i, j, board.get_other_player_id(), board) * 1.5
    #score = board.longest_chain(board.get_current_player_id()) * 10
    score = 0
    # Prefer having your pieces in the center of the board.
    for row in range(6):
        for col in range(7):
            if board.get_cell(row, col) == board.get_current_player_id():
                score -= abs(3-col)
            elif board.get_cell(row, col) == board.get_other_player_id():
                score += abs(3-col)
    return c+ (score*5 )

def count_at(x, y, playerId, board):
    #create a mapping of all possible connect fours from the current location
    possible = [[(x, y), (x + 1, y), (x + 2, y), (x + 3, y)],
                [(x, y), (x, y + 1), (x, y + 2), (x, y + 3)],
                [(x, y), (x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)],
                [(x, y), (x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)]]

    #Get the player at that position for every possible connect 4
    possible = map(lambda possibility: map(lambda pos: board.get_cell(pos[0], pos[1]) if pos[0] >= 0 and pos[0] < 6 and pos[1] >= 0 and pos[1] < 7 else -1,  possibility) , possible)

    c = 0
    #for every possible connect 4
    for p in possible:
        #Keep track of if there is a connect 4 in this one
        counts = False
        inARow = 0
        for player in p:
            if player == playerId:
                inARow += 1
                counts = True
                continue
            if player != 0 and player != playerId:
                counts = False
                break
        if counts:
            c += 1
            if inARow == 3: c+=10
    return c
def okayEvalute(board):
    myLongestChain = board.longest_chain(board.get_current_player_id())
    if(myLongestChain >= 4): return 1000
    theirLongestChain = board.longest_chain(board.get_other_player_id())
    if(theirLongestChain >= 4): return -1000
    c = 0
    for i in range(6):
        for j in range(7):
            c += count_at(i, j, board.get_current_player_id(), board)
            c -= count_at(i, j, board.get_other_player_id(), board) * 1.5
    return c

# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if True:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

your_player = lambda board: alpha_beta_search(board, depth=4,
                                              eval_fn=better_evaluate)
new_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=okayEvalute)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
run_game(basic_player, your_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])

def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)

## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (True)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "4"
WHAT_I_FOUND_INTERESTING = "having to write my own AI"
WHAT_I_FOUND_BORING = "THE INSTRUCTIONS WEREN'T AS CLEAR AS BEFORE THE HINTS FOR ALPHA BETA WERE WAY AFTER WHEN IT TOLD ME TO MAKE IT"
NAME = "Andrew Spencer"
EMAIL = "nope@nope.com"

