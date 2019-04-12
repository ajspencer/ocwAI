def better_evaluate(board):
    myLongestChain = board.longest_chain(board.get_current_player_id())
    if(myLongestChain >= 4): return 1000
    theirLongestChain = board.longest_chain(board.get_other_player_id())
    if(theirLongestChain >= 4): return -1000
    c = 0
    for i in range(6):
        for j in range(7):
            c += count_at(i, j, board.get_current_player_id(), board)
            c -= count_at(i, j, board.get_other_player_id(), board)
    return c

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
        for player in p:
            if player == playerId:
                counts = True
                continue
            if player != 0 and player != playerId:
                counts = False
                break
        if counts:
            c += 1
    return c

