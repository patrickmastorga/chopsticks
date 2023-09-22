import json

# map[a][b][c][d]
# generate map where a, b is the player who's turn it is hand and  c, d is the other player's hand
# principle win conditions are pre filled in with -1
map = [
    [
        [
            [
                -1 if a == b == 0 else None if c == d == 0 else 0 for d in range(5)
            ] for c in range(5)
        ] for b in range(5)
    ] for a in range(5)
]
map[0][0][0][0] = None

visited = []

def branch(a, b, c, d):
    if map[a][b][c][d]:
        return -map[a][b][c][d]
    if ([a, b, c, d] in visited):
        return 0
    visited.append([a, b, c, d])
    tie = False
    if a:
        check = branch((c + a) % 5, d, a, b)
        
        

      
for a in range(5):
    for b in range(5):
        for c in range(5):
            for d in range(5):
                if map[a][b][c][d] not is 0:
                    continue
                visited = []
                branch(a, b, c, d)

with open("chopsticks.json", "w") as out_file:
    json.dump(map, out_file)