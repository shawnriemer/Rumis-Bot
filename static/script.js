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

    var piece = document.getElementById('piece').value;
    var x = document.getElementById('x').value;
    var y = document.getElementById('y').value;
    var z = document.getElementById('z').value;

    fetch('/nextturn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'piece': piece, 'x': x, 'y': y, 'z': z })
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

// Update visual of all playable pieces
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
        var image = document.getElementById("4x1");
        image.src = `static/4x1.png?t=${timestamp}`
    });

}
