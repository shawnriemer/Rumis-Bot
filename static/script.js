// Testing JavaScript
//function createParagraph() {
//  const para = document.createElement("p");
//  para.textContent = "You clicked the button!";
//  document.body.appendChild(para);
//}
//
//const buttons = document.querySelectorAll("button");
//
//for (const button of buttons) {
//  button.addEventListener("click", createParagraph);
//}


// Testing fetch
//document.getElementById("testbruh").addEventListener("click", sendData);
//
//function sendData() {
//    var value = document.getElementById('input').value;
//
//    fetch('/process', {
//        method: 'POST',
//        headers: {
//            'Content-Type': 'application/json',
//        },
//        body: JSON.stringify({ 'value': value })
//        }
//    )
//    .then((response) => {
//        if (!response.ok) {
//            throw new Error(`HTTP error: ${response.status}`);
//        }
//        return response.json();
//    })
//    .then((data) => {
//        console.log(data);
//        document.getElementById('output').innerHTML = data.result;
//    });
//}


// Iterate through computer turns
document.getElementById("nextTurn").addEventListener("click", nextTurn);
function nextTurn() {

    var image = document.getElementById("gameBoard");
    image.src = 'static/loading.gif'

    fetch('/nextturn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'piece': 'placeholder' })
        }
    )
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
    .then((data) => {
        console.log(data);
        document.getElementById('output').innerHTML = `Turns: ${data.turn}`;

        var timestamp = new Date().getTime();
        var image = document.getElementById("gameBoard");
        image.src = `static/test_0.png?t=${timestamp}`
    });

}


// Play human's turn
const pieces = ['4x1', '3x1', '2x1', 'L', 'square', 'corner', 'pipe', 'bend', 'archer', 'twistL', 'twistR']
for (const piece of pieces) {
    document.getElementById(`next_turn_${piece}`).addEventListener("click", nextTurn_human);
    document.getElementById(`next_turn_${piece}`).myParam = piece
}

function nextTurn_human(evt) {
    var image = document.getElementById("gameBoard");
    image.src = 'static/loading.gif'
    var piece = evt.currentTarget.myParam
    fetch('/nextturn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'piece': piece })
        }
    )
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
    .then((data) => {
        console.log(data);
        document.getElementById('output').innerHTML = `Turns: ${data.turn}`;
        var timestamp = new Date().getTime();
        var image = document.getElementById("gameBoard");
        image.src = `static/test_0.png?t=${timestamp}`
    });

}


// Rotate current game board
document.getElementById("rotate").addEventListener("click", rotate);

function rotate(){
    var timestamp = new Date().getTime();
    var image = document.getElementById("gameBoard");

    if (image.src.includes('_0')) {
        image.src = image.src.replace('_0', '_90')
    } else if (image.src.includes('_90')) {
        image.src = image.src.replace('_90', '_180')
    } else if (image.src.includes('_180')) {
        image.src = image.src.replace('_180', '_270')
    } else if (image.src.includes('_270')) {
        image.src = image.src.replace('_270', '_0')
    }
}


// Update visual of all playable pieces  # TODO: there has to be a better way to do this
const moves = ['right', 'left', 'away', 'towards', 'up', 'down', 'x', 'y', 'z']
for (const move of moves) {
    document.getElementById(`move_${move}`).addEventListener("click", movePieces);
    document.getElementById(`move_${move}`).myParam = move
}

function movePieces(evt) {
    var move = evt.currentTarget.myParam
    fetch('/movePiece', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'move': move })
            }
    )
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
    .then((data) => {
        var timestamp = new Date().getTime();
        // Loop through array of each piece
        const pieces = ['4x1', '3x1', '2x1', 'L', 'square', 'corner', 'pipe', 'bend', 'archer', 'twistL', 'twistR']
        for (const piece of pieces) {
            var image = document.getElementById(piece);
            image.src = `static/${piece}.png?t=${timestamp}`
        }
    });
}

