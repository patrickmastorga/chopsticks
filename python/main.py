import json, math

# map[a][b][c][d]
# generate map where p11, p12 is the player who's turn it is hand and  p21, p22 is the other player's hand
# hadns for each player are in descending order
map = [
    [
        [
            [
                (float("-inf") if (p11, p12) == (0, 0) else None) for p22 in range(p21 + 1)
            ] if p21 > 0 else None for p21 in range(5)
        ] for p12 in range(p11 + 1)
    ] for p11 in range(5)
]


def legal_moves(position: tuple[int]) -> set[tuple[int]]:
    """ Returns all new positions possible from a given one """
    (p11, p12, p21, p22) = position
    moves = set()
    
    # transfers
    for i in range(1, (p11 - p12) // 2 + 1):
        moves.add((p21, p22, p11 - i, p12 + i))
    for i in range(1, p12 + 1):
    #    if p11 + i < 5: ARE YOU ALLOWED TO ROLL OVER ON TRANSFERS??
    #        moves.add((p21, p22, p11 + i, p12 - i))
        if p11 + i != 5:
            moves.add((p21, p22, max((p11 + i) % 5, p12 - i), min((p11 + i) % 5, p12 - i)))

    # attacks
    if p11 != 0:
        if p21 != 0:
            moves.add((max((p21 + p11) % 5, p22), min((p21 + p11) % 5, p22), p11, p12))
        if p22 != 0:
            moves.add((max(p21, (p22 + p11) % 5), min(p21, (p22 + p11) % 5), p11, p12))
    if p12 != 0:
        if p21 != 0:
            moves.add((max((p21 + p12) % 5, p22), min((p21 + p12) % 5, p22), p11, p12))
        if p22 != 0:
            moves.add((max(p21, (p22 + p12) % 5), min(p21, (p22 + p12) % 5), p11, p12))

    return moves


###############################################################
# Forced wins and losses
###############################################################

def branch(position: tuple[int], turn: int, visited: set[tuple[int]]) -> int:
    """ Recursively calculates forced wins. Returns (p11, p12)'s outcome given the current position. 1 means win is forced, -1 means loss is inevitable """
    (p11, p12, p21, p22) = position

    # we only need to search where the map isnt already filled in
    if map[p11][p12][p21][p22] != None:
        return map[p11][p12][p21][p22]
    
    # if this player has already reached this exact position, game is a tie
    if (p11, p12, p21, p22, turn) in visited:
        return 0
    visited.add((p11, p12, p21, p22, turn))

    # recursive branching
    outcomes = [-1 * branch(move, turn * -1, visited.copy()) for move in legal_moves(position)]
    if len(outcomes) == 0:
        print("SOMETHING IS WIERD")
        print(position)
        return 0

    map[p11][p12][p21][p22] = max(outcomes)
    return max(outcomes)


# fill map with absolute wins and losses (forced victories)
for p11 in range(5):
    for p12 in range(p11 + 1):
        for p21 in range(1, 5):
            for p22 in range(p21 + 1):
                if map[p11][p12][p21][p22] == None:
                    branch((p11, p12, p21, p22), 1, set())


###############################################################
# Relative win potential
###############################################################

win_potential = 0

def tally_branch(position: tuple[int], turn: int, depth: int) -> None:
    """ Recursiveley counts the number of forced wins vs forced losses from a given position """
    global MAX_DEPTH, win_potential
    (p11, p12, p21, p22) = position

    # only recurse if position is still a tie
    if math.isinf(map[p11][p12][p21][p22]):
        if map[p11][p12][p21][p22] > 0:
            win_potential += turn / depth ** 5
        else:
            win_potential -= turn / depth ** 5
        return

    # dont recurse futher than the maximum depth
    if depth >= MAX_DEPTH:
        return

    # recursive branching
    for move in legal_moves(position):
        tally_branch(move, turn * -1, depth + 1)

# update the map with the relative strength of each position (based on number of forced wins compared to forced losses in subtree)
MAX_DEPTH = 10
for p11 in range(5):
    for p12 in range(p11 + 1):
        for p21 in range(1, 5):
            for p22 in range(p21 + 1):
                if map[p11][p12][p21][p22] == 0:
                    win_potential = 0
                    tally_branch((p11, p12, p21, p22), 1, 0)
                    print((p11, p12, p21, p22), round(win_potential, 4))
                    map[p11][p12][p21][p22] = round(win_potential, 4)
                    
with open("chopsticks.json", "w") as out_file:
    json.dump(map, out_file)

print("Success!!")