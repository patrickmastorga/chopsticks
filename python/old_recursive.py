import json

MAX_CUTOFF = 1e2
MAX_BRANCH_DEPTH = 10

# map[a][b][c][d]
# generate map where p11, p12 is the player who's turn it is hand and  p21, p22 is the other player's hand
# hadns for each player are in descending order
map = [
    [
        [
            [
                (-MAX_CUTOFF * 10 if (p11, p12) == (0, 0) else 0) for p22 in range(p21 + 1)
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
# Forced wins and losses (in place recursion)
###############################################################

def update(position: tuple[int], map: list[list[list[list[float]]]]) -> int:
    """ Recursively calculates forced wins. Returns (p11, p12)'s outcome given the current position. 1 means win is forced, -1 means loss is inevitable """
    global MAX_BRANCH_DEPTH
    (p11, p12, p21, p22) = position

    # branching
    outcomes = [-1 * map[p11][p12][p21][p22] for p11, p12, p21, p22 in legal_moves(position)]

    best = max(outcomes)

    # decrement the win value for every move away from victory
    if abs(best) > MAX_CUTOFF:
        if best > 0:
            best -= 1
        else:
            best += 1
    
    map[p11][p12][p21][p22] = best

print("CALCULATING FORCED WINS")
# fill map with absolute wins and losses (forced victories)
for i in range(225): # Max depth of 225 because only 225 functionally distinct position (way overkill: technically a depth of 14 reaches all of the forced wins)
    for p11 in range(5):
        for p12 in range(p11 + 1):
            for p21 in range(1, 5):
                for p22 in range(p21 + 1):
                    if map[p11][p12][p21][p22] == 0:
                        update((p11, p12, p21, p22), map)

###############################################################
# Relative win potential
###############################################################

win_potential = 0
MAX_TALLY_DEPTH = 10

def tally_branch(position: tuple[int], turn: int, depth: int, branches: int) -> None:
    """ Recursiveley counts the number of forced wins vs forced losses from a given position """
    global MAX_TALLY_DEPTH, win_potential
    (p11, p12, p21, p22) = position

    # only recurse if position is still a tie
    if abs(map[p11][p12][p21][p22]) >= MAX_CUTOFF:
        # 1 / depth ** 4 because the amount of legal moves is on average less than 4 (total magnitude deimishes as depth increases)
        if map[p11][p12][p21][p22] > 0:
            win_potential += turn / (branches * depth)
        else:
            win_potential -= turn / (branches * depth)
        return

    # dont recurse futher than the maximum depth
    if depth >= MAX_TALLY_DEPTH:
        return

    # recursive branching
    moves = legal_moves(position)
    for move in moves:
        tally_branch(move, turn * -1, depth + 1, branches * len(moves))


print("CALCULATING REALTIVE WIN POTENTIAL")
# update the map with the relative strength of each position (based on number of forced wins compared to forced losses in subtree)
for p11 in range(5):
    for p12 in range(p11 + 1):
        for p21 in range(1, 5):
            for p22 in range(p21 + 1):
                if map[p11][p12][p21][p22] == 0:
                    win_potential = 0
                    tally_branch((p11, p12, p21, p22), 1, 0, 1)
                    print((p11, p12, p21, p22), round(win_potential, 4))
                    map[p11][p12][p21][p22] = round(win_potential, 4)


###############################################################
# Final Strength
###############################################################

strength = [
    [
        [
            [
                (map[p11][p12][p21][p22] if abs(map[p11][p12][p21][p22]) >= MAX_CUTOFF else None) for p22 in range(p21 + 1)
            ] if p21 > 0 else None for p21 in range(5)
        ] for p12 in range(p11 + 1)
    ] for p11 in range(5)
]

MAX_SEARCH_DEPTH = 4

def strength_branch(position: tuple[int], depth: int) -> int:
    """ Recursively calculates forced wins. Returns (p11, p12)'s outcome given the current position. 1 means win is forced, -1 means loss is inevitable """
    global MAX_BRANCH_DEPTH
    (p11, p12, p21, p22) = position
    
    if p11 == p12 == 0:
        return -MAX_CUTOFF * 10

    # dont search deeper than max depth
    if depth > MAX_SEARCH_DEPTH:
        return map[p11][p12][p21][p22]

    # recursive branching
    return max(-1 * strength_branch(move, depth + 1) for move in legal_moves(position))

print("CALCULATING STRENGTH")
# update the map with the relative strength of each position (based on number of forced wins compared to forced losses in subtree)
for p11 in range(5):
    for p12 in range(p11 + 1):
        for p21 in range(1, 5):
            for p22 in range(p21 + 1):
                if abs(map[p11][p12][p21][p22]) < MAX_CUTOFF:
                    strength[p11][p12][p21][p22] = strength_branch((p11, p12, p21, p22), 1, 0)
                    print((p11, p12, p21, p22), strength[p11][p12][p21][p22])

with open("strength.json", "w") as out_file:
    json.dump(strength, out_file)

"""
###############################################################
# Legal Move Table
###############################################################

moves = [
    [
        [
            [
                (None if p11 == p12 == 0 else list(legal_moves((p11, p12, p21, p22)))) for p22 in range(p21 + 1)
            ] if p21 > 0 else None for p21 in range(5)
        ] for p12 in range(p11 + 1)
    ] for p11 in range(5)
]

with open("moves.json", "w") as out_file:
    json.dump(moves, out_file)
"""

print("Success!!")