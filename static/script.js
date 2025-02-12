// Testing JavaScript
function createParagraph() {
  const para = document.createElement("p");
  para.textContent = "You clicked the button!";
  document.body.appendChild(para);
}

const buttons = document.querySelectorAll("button");

for (const button of buttons) {
  button.addEventListener("click", createParagraph);
}


// Testing fetch
document.getElementById("testbruh").addEventListener("click", sendData);

function sendData() {
    var value = document.getElementById('input').value;

    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'value': value })
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
        document.getElementById('output').innerHTML = data.result;
    });
}



// Iterate through Rumis turns
document.getElementById("nextTurn").addEventListener("click", nextTurn);

function nextTurn() {
    var value = document.getElementById('input2').value;

    fetch('/nextturn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'value': value })
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
        image.src = `static/test.png?t=${timestamp}`
    });

}
