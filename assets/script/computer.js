import moves from './moves.json' assert { type: "json" };
import strength from './strength.json' assert { type: "json" };

/**
 * Takes in an existing position and modifies it based on the computer's move
 * @param {number[]} position [a, b, c, d] where (a, b) is the human's hands and (c, d) is the computer's hands (both pairs in descending order)
 * @param {number=} difficulty number in range (0, 1] represnting the accuracy of the cumputer's move
 * @return {number[]} [e, f, g, h] where (e, f) is the human's new hands and (g, h) is the computer's new hands (both pairs in descending order)
 */
export function computerMove(position, difficulty=1.0) {
    console.log("--------------------------");
    console.log("POSITION: ", position)
    
    let [h1, h2, c1, c2] = position;
    let computerMoves = moves[c1][c2][h1][h2]

    for (let move of computerMoves) {
        if (move.length > 4) {
            continue;
        }
        let [a, b, c, d] = move;
        move.push(strength[a][b][c][d]);
    }

    computerMoves.sort((a, b) => a[4] - b[4]);

    for (let move of computerMoves) {
        console.log(move);
    }
    console.log("--------------------------");

    return computerMoves[generateIndex(computerMoves.length, difficulty)].slice(0, 4);
}

/**
 * Generates the index of the move to play based on the player selcected difficulty
 * @param {number} length the number of options available
 * @param {number} difficulty the sqrt of the probability that the best move will be selected, every next best move afterwards
 * @returns the index of the move to be played
 */
function generateIndex(length, difficulty) {
    let p = difficulty ** 2;

    let spread = [p,];
    for (let i = 1; i < length; ++i) {
        let sum = spread.reduce((a, b) => a + b);
        spread.push(p - p * sum);
    }

    let sum = spread.reduce((a, b) => a + b);
    let target = Math.random() * sum;
    for (let i = 0; i < length; ++i) {
        target -= spread[i];
        if (target <= 0) {
            return i;
        }
    }
    return length - 1;
}