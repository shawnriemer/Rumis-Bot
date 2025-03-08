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



// Iterate through Rumis turns
document.getElementById("nextTurn").addEventListener("click", nextTurn);
function nextTurn() {

    var image = document.getElementById("gameBoard");
    image.src = 'static/loading.gif'

//    var piece = document.getElementById('piece').value;
//    var x = document.getElementById('x').value;
//    var y = document.getElementById('y').value;
//    var z = document.getElementById('z').value;

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

//document.getElementById("next_turn_2x1").addEventListener("click", nextTurn_3x1);
//document.getElementById("next_turn_2x1").myParam = '2x1'
//
//document.getElementById("next_turn_3x1").addEventListener("click", nextTurn_3x1);
//document.getElementById("next_turn_3x1").myParam = '3x1'
//
//document.getElementById("next_turn_4x1").addEventListener("click", nextTurn_3x1);
//document.getElementById("next_turn_4x1").myParam = '4x1'

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


// Rotate board
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
document.getElementById("move_right").addEventListener("click", moveRight);
function moveRight() {
    fetch('/movePiece', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'move': 'right' })
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

document.getElementById("move_left").addEventListener("click", moveLeft);
function moveLeft() {
    fetch('/movePiece', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'move': 'left' })
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

document.getElementById("move_up").addEventListener("click", moveUp);
function moveUp() {
    fetch('/movePiece', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'move': 'up' })
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

document.getElementById("move_down").addEventListener("click", moveDown);
function moveDown() {
    fetch('/movePiece', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'move': 'down' })
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

document.getElementById("move_away").addEventListener("click", moveAway);
function moveAway() {
    fetch('/movePiece', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'move': 'away' })
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

document.getElementById("move_towards").addEventListener("click", moveTowards);
function moveTowards() {
    fetch('/movePiece', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'move': 'towards' })
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
