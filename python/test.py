import json, math

with open('chopsticks.json', 'r') as f:
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

sum = 0
count = 0
for p11 in range(5):
    for p12 in range(p11 + 1):
        for p21 in range(1, 5):
            for p22 in range(p21 + 1):
                if math.isinf(map[p11][p12][p21][p22]) and map[p11][p12][p21][p22] > 0:
                    print((p11, p12, p21, p22), (1, 0, 3, 0) in legal_moves((p11, p12, p21, p22)))