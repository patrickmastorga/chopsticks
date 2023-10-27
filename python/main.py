import json
import copy

# Cutoff for when a move is considered absolutely winning
MAX_CUTOFF = 1e2

# map[p11][p12][p21[p22]
# generate map where p11, p12 is the player who's turn it is hand and  p21, p22 is the other player's hand
# hands for each player are in descending order
strength_map = [
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


###############################################################
# Forced wins and losses (in place minimax tree fill)
###############################################################

# How deep to go when calculating the search
ITERATIONS = 225 # Max depth of 225 because only 225 functionally distinct position (way overkill: technically a depth of 14 reaches all of the forced wins)

def update_absolute_wins(position: tuple[int], map: list[list[list[list[float]]]]) -> None:
    """ Updates the value of a position based on if a win is forced from that position """
    (p11, p12, p21, p22) = position

    # branching
    best = max(-1 * map[p11][p12][p21][p22] for p11, p12, p21, p22 in moves[p11][p12][p21][p22])

    # decrement the win value for every move away from victory
    if abs(best) > MAX_CUTOFF:
        if best > 0:
            best -= 1
        else:
            best += 1
    
    map[p11][p12][p21][p22] = best

print("CALCULATING FORCED WINS")
# fill map with absolute wins and losses (forced victories)
for i in range(ITERATIONS):
    for p11 in range(5):
        for p12 in range(p11 + 1):
            for p21 in range(1, 5):
                for p22 in range(p21 + 1):
                    if strength_map[p11][p12][p21][p22] == 0:
                        update_absolute_wins((p11, p12, p21, p22), strength_map)

for p11 in range(5):
    for p12 in range(p11 + 1):
        for p21 in range(1, 5):
            for p22 in range(p21 + 1):
                if abs(strength_map[p11][p12][p21][p22]) >= MAX_CUTOFF:
                    print((p11, p12, p21, p22), "W" if strength_map[p11][p12][p21][p22] > 0 else "L")

###############################################################
# Relative Strength (geometric win sum) (in place sum)
###############################################################

# Rate of decay of the geoemtric sum of win/losses as depth increases 
DECAY_RATE = 1 / 5
# How deep to go when calculating the sum
ITERATIONS = 24

def update_win_sum(position: tuple[int], map: list[list[list[list[float]]]], old_map: list[list[list[list[float]]]]) -> None:
    """ Updates the value of a position based on if a win is forced from that position """
    (p11, p12, p21, p22) = position

    win_sum = sum(-1 * old_map[p11][p12][p21][p22] for (p11, p12, p21, p22) in moves[p11][p12][p21][p22] if abs(old_map[p11][p12][p21][p22]) > MAX_CUTOFF)
    geometric_sum = sum(-1 * old_map[p11][p12][p21][p22] for (p11, p12, p21, p22) in moves[p11][p12][p21][p22] if abs(old_map[p11][p12][p21][p22]) < MAX_CUTOFF)

    map[p11][p12][p21][p22] = (win_sum / MAX_CUTOFF + geometric_sum * DECAY_RATE) / len(moves[p11][p12][p21][p22])

print("CALCULATING WIN SUM")
# fills map with win sum
for i in range(ITERATIONS):
    prev = copy.deepcopy(strength_map)
    for p11 in range(5):
        for p12 in range(p11 + 1):
            for p21 in range(1, 5):
                for p22 in range(p21 + 1):
                    if abs(strength_map[p11][p12][p21][p22]) < MAX_CUTOFF:
                        update_win_sum((p11, p12, p21, p22), strength_map, prev)

# Print data to console and round to 4 digits
for p11 in range(5):
    for p12 in range(p11 + 1):
        for p21 in range(1, 5):
            for p22 in range(p21 + 1):
                if abs(strength_map[p11][p12][p21][p22]) < MAX_CUTOFF:
                    print((p11, p12, p21, p22), strength_map[p11][p12][p21][p22])


###############################################################
# Minimax Search (in place minimax tree fill)
###############################################################

# How deep to go when calculating the search
ITERATIONS = 4

def minimax_update(position: tuple[int], map: list[list[list[list[float]]]], old_map: list[list[list[list[float]]]]) -> None:
    """ Updates the value of a position based on the best move from that position """
    (p11, p12, p21, p22) = position

    # branching
    best = max(-1 * old_map[p11][p12][p21][p22] for p11, p12, p21, p22 in moves[p11][p12][p21][p22] if abs(old_map[p11][p12][p21][p22]) < MAX_CUTOFF)
    
    map[p11][p12][p21][p22] = best

print("CALCULATING MINIMAX VALUES")
# fill map according to minimax tree search
for i in range(10): # Max depth of 225 because only 225 functionally distinct position (way overkill: technically a depth of 14 reaches all of the forced wins)
    prev = copy.deepcopy(strength_map)
    for p11 in range(5):
        for p12 in range(p11 + 1):
            for p21 in range(1, 5):
                for p22 in range(p21 + 1):
                    if abs(strength_map[p11][p12][p21][p22]) < MAX_CUTOFF:
                        minimax_update((p11, p12, p21, p22), strength_map, prev)

avg = 0
count = 0
for p11 in range(5):
    for p12 in range(p11 + 1):
        for p21 in range(1, 5):
            for p22 in range(p21 + 1):
                if abs(strength_map[p11][p12][p21][p22]) < MAX_CUTOFF:
                    avg += strength_map[p11][p12][p21][p22]
                    count += 1
avg /= count

# Print data to console and round to 4 digits
for p11 in range(5):
    for p12 in range(p11 + 1):
        for p21 in range(1, 5):
            for p22 in range(p21 + 1):
                strength_map[p11][p12][p21][p22] = round(strength_map[p11][p12][p21][p22] - avg, 4)
                if abs(strength_map[p11][p12][p21][p22]) < MAX_CUTOFF:
                    print((p11, p12, p21, p22), strength_map[p11][p12][p21][p22])


###############################################################
# File Output
###############################################################

#with open("strength.json", "w") as out_file:
#    json.dump(strength_map, out_file)

#with open("moves.json", "w") as out_file:
#    json.dump(moves, out_file)