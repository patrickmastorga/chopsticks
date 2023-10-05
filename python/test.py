import json, math

with open('strength.json', 'r') as f:
    map = json.load(f)

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

MAX_BRANCH_DEPTH = 10

def branch(position: tuple[int], turn: int, depth: int, visited: set[tuple[int]]) -> int:
    """ Recursively calculates forced wins. Returns (p11, p12)'s outcome given the current position. 1 means win is forced, -1 means loss is inevitable """
    global MAX_BRANCH_DEPTH
    (p11, p12, p21, p22) = position

    # we only need to search where the map isnt already filled in
    if map[p11][p12][p21][p22] != None:
        return map[p11][p12][p21][p22]

    # dont search deeper than max depth
    if depth > MAX_BRANCH_DEPTH:
        return 0
    
    # if this player has already reached this exact position, game is a tie
    if (p11, p12, p21, p22, turn) in visited:
        return 0
    visited.add((p11, p12, p21, p22, turn))

    # recursive branching
    outcomes = [-1 * branch(move, turn * -1, depth + 1, visited.copy()) for move in legal_moves(position)]
    if len(outcomes) == 0:
        print("SOMETHING IS WIERD")
        print(position)
        return 0

    print(position, outcomes, legal_moves(position))
    return max(outcomes)