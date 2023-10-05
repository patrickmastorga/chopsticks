import { computerMove } from "./assets/script/computer.js";

const topLeft = document.getElementById("top-left");
const topRight = document.getElementById("top-right");
const bottomLeft = document.getElementById("bottom-left");
const bottomRight = document.getElementById("bottom-right");

const transferWindow = document.getElementById("transfer-window");
const transferOptions = document.getElementById("options");

const turnIndicator = document.getElementById("turn-indicator");
const leftIndicator = document.getElementById("left-indicator");
const rightIndicator = document.getElementById("right-indicator");

const winText = document.getElementById("win-text");
const loseText = document.getElementById("lose-text");

let bottomLeftSelected = false;
let bottomRightSelected = false;
let currentPosition;
let buttonsEnabled;

let computerStart = false;

function init() {
    if (bottomLeftSelected) {
        bottomLeftClick(true);
    }
    if (bottomRightSelected) {
        bottomRightClick(true);
    }
    currentPosition = [1, 1, 1, 1];
    buttonsEnabled = true;

    winText.style.display = "none";
    loseText.style.display = "none";
    
    turnIndicator.style.opacity = 0;
    if (computerStart) {
        playMove();
    }
    else {
        turnIndicator.style.opacity = 1;
        updateHands();
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function topLeftClick() {
    if (!buttonsEnabled || currentPosition[2] == 0) {
        return;
    }
    if (bottomLeftSelected) {
        currentPosition[2] = (currentPosition[2] + currentPosition[0]) % 5;
        bottomLeftClick();
        playMove();
        return;
    }
    if (bottomRightSelected) {
        currentPosition[2] = (currentPosition[2] + currentPosition[1]) % 5;
        bottomRightClick();
        playMove();
        return;
    }
}

function topRightClick() {
    if (!buttonsEnabled || currentPosition[3] == 0) {
        return;
    }
    if (bottomLeftSelected) {
        currentPosition[3] = (currentPosition[3] + currentPosition[0]) % 5;
        bottomLeftClick();
        playMove();
        return;
    }
    if (bottomRightSelected) {
        currentPosition[3] = (currentPosition[3] + currentPosition[1]) % 5;
        bottomRightClick();
        playMove();
        return;
    }
}

function bottomLeftClick(force=false) {
    if (!force && (!buttonsEnabled || (currentPosition[0] == 0 && !bottomRightSelected))) {
        return;
    }
    if (bottomLeftSelected) {
        bottomLeftSelected = false;
        bottomLeft.style.filter = "none";
        leftIndicator.style.opacity = 0;
        if (currentPosition[1] == 0 && currentPosition[0] > 1) {
            bottomRight.setAttribute("src", "./assets/images/zero_fingers.png");
        }
        return;
    }
    if (!bottomRightSelected) {
        bottomLeftSelected = true;
        bottomLeft.style.filter = "brightness(0.5)";
        leftIndicator.style.opacity = 1;
        if (currentPosition[1] == 0 && currentPosition[0] > 1) {
            bottomRight.setAttribute("src", "./assets/images/outline_fingers.png");
        }
    }
    else {
        bottomLeft.style.filter = "brightness(0.5)";
        showTransferWindow();
    }
}

function bottomRightClick(force=false) {
    if (!force && (!buttonsEnabled || (currentPosition[1] == 0 && !bottomLeftSelected))) {
        return;
    }
    if (bottomRightSelected) {
        bottomRightSelected = false;
        bottomRight.style.filter = "none";
        rightIndicator.style.opacity = 0;
        if (currentPosition[0] == 0 && currentPosition[1] > 1) {
            bottomLeft.setAttribute("src", "./assets/images/zero_fingers.png");
        }
        return;
    }
    if (!bottomLeftSelected) {
        bottomRightSelected = true;
        bottomRight.style.filter = "brightness(0.5)";
        rightIndicator.style.opacity = 1;
        if (currentPosition[0] == 0 && currentPosition[1] > 1) {
            bottomLeft.setAttribute("src", "./assets/images/outline_fingers.png");
        }
        return;
    }
    else {
        bottomRight.style.filter = "brightness(0.5)";
        showTransferWindow();
    }
}

function showTransferWindow() {
    let [bl, br, tl, tr] = currentPosition;
    let one, two, three, four;
    
    if (bottomLeftSelected) {
        one = (br + 1 != bl) && (br + 1 != 5);
        two = (bl > 1) && (br + 2 != bl) && (br + 2 != 5); 
        three = (bl > 2) && (br + 3 != bl) && (br + 3 != 5); 
        four = (bl == 4) && (br + 4 != bl) && (br + 4 != 5); 
    }
    else {
        one = (bl + 1 != br) && (bl + 1 != 5);
        two = (br > 1) && (bl + 2 != br) && (bl + 2 != 5); 
        three = (br > 2) && (bl + 3 != br) && (bl + 3 != 5); 
        four = (br == 4) && (bl + 4 != br) && (bl + 4 != 5); 
    }

    if (one || two || three || four) {
        addTransferOptions(one, two, three, four);
        transferWindow.style.display = "block";
        buttonsEnabled = false;
    }
    else {
        if (bottomLeftSelected) {
            bottomRight.style.filter = "none";
        }
        else {
            bottomLeft.style.filter = "none";
        }
    }
}

function addTransferOptions(one, two, three, four) {
    const options = [null,
        '<div class="col-4 option" onclick="window.transfer(1)"><h3>1</h3></div>',
        '<div class="col-4 option" onclick="window.transfer(2)"><h3>2</h3></div>',
        '<div class="col-4 option" onclick="window.transfer(3)"><h3>3</h3></div>',
        '<div class="col-4 option" onclick="window.transfer(4)"><h3>4</h3></div>'
    ];

    let inner = ""
    if (one) {
        inner += options[1];
    }
    if (two) {
        inner += options[2];
    }
    if (three) {
        inner += options[3];
    }
    if (four) {
        inner += options[4];
    }
    transferOptions.innerHTML = inner;
}

function hideTransferWindow() {
    if (bottomLeftSelected) {
        bottomLeftClick(true);
        bottomRight.style.filter = "none";
    }
    else {
        bottomRightClick(true);
        bottomLeft.style.filter = "none";
    }
    buttonsEnabled = true;
    transferWindow.style.display = "none"
}

function transfer(amount) {
    if (bottomLeftSelected) {
        currentPosition[0] -= amount;
        currentPosition[1] = (currentPosition[1] + amount) % 5;
    }
    else {
        currentPosition[1] -= amount;
        currentPosition[0] = (currentPosition[0] + amount) % 5;
    }
    hideTransferWindow()
    playMove()
}

async function playMove() {
    updateHands();

    let [bl, br, tl, tr] = currentPosition;

    if (tl == 0 && tr == 0) {
        win();
        return;
    }

    let [h1, h2, c1, c2] = computerMove([bl>br?bl:br, bl>br?br:bl, tl>tr?tl:tr, tl>tr?tr:tl]);

    if (bl == h1 && br == h2) {
        currentPosition = [h1, h2, c1, c2];
    }
    else if (br == h1 && bl == h2) {
        currentPosition = [h2, h1, c1, c2];
    }
    else if (bl == h1 || br == h2) {
        if (tl > tr) {
            currentPosition = [h1, h2, c1>c2?c1:c2, c1>c2?c2:c1];
        } else {
            currentPosition = [h1, h2, c1>c2?c2:c1, c1>c2?c1:c2];
        }
    }
    else if (bl == h2 || br == h1) {
        if (tl > tr) {
            currentPosition = [h2, h1, c1>c2?c1:c2, c1>c2?c2:c1];
        } else {
            currentPosition = [h2, h1, c1>c2?c2:c1, c1>c2?c1:c2];
        }
    }

    turnIndicator.style.opacity = 0;

    buttonsEnabled = false;
    await sleep(1000);
    buttonsEnabled = true;

    updateHands();
    if (h1 == 0 && h2 == 0) {
        lose();
        return;
    }

    turnIndicator.style.opacity = 1;   
}

function updateHands() {
    const hands = ["./assets/images/zero_fingers.png", "./assets/images/one_fingers.png", "./assets/images/two_fingers.png", "./assets/images/three_fingers.png", "./assets/images/four_fingers.png"];

    let [bl, br, tl, tr] = currentPosition;
    
    bottomLeft.setAttribute("src", hands[bl]);
    bottomRight.setAttribute("src", hands[br]);
    topLeft.setAttribute("src", hands[tl]);
    topRight.setAttribute("src", hands[tr]);
}

function win() {
    buttonsEnabled = false;
    winText.style.display = "block";
}

function lose() {
    buttonsEnabled = false;
    loseText.style.display = "block";
}

// set functions as window attributes so they are accesible as html attribute
window.topLeftClick = topLeftClick;
window.topRightClick = topRightClick;
window.bottomLeftClick = bottomLeftClick;
window.bottomRightClick = bottomRightClick;
window.hideTransferWindow = hideTransferWindow;
window.transfer = transfer;
window.init = init;

init()