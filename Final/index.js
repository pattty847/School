"use strict";

// This is a copied function that will enable the GUI to be draggable.
function dragElement(elmnt) {
    var pos1 = 0,
        pos2 = 0,
        pos3 = 0,
        pos4 = 0;
    if (document.getElementById(elmnt.id + "card")) {
        // if present, the header is where you move the DIV from:
        document.getElementById(elmnt.id + "card").onmousedown = dragMouseDown;
    } else {
        // otherwise, move the DIV from anywhere inside the DIV:
        elmnt.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
    }
}


// This variable will store each card object in an array called 'watchlist'.
// When a user wants to add a particular coin to their watch list we will first create a card object and push it to this array.
let watchlist = [];
let webSocketList = [];

// This is where we create a barebones card object.
// The card object is a panel that displays each property.
// This function will be called with a 'card' object that will be used to create a table for the display.
function createCard(card) {

    var div = document.createElement('div');
    div.id = card["title"];
    div.style.position = 'absolute';

    // Declare a table variable that is initialized to a table element
    var table = document.createElement('table');
    table.className = 'card';
    table.id = card['title'] + "card";
    table.style.cursor = 'move';


    // We set our table's header and body with these functions
    var header = table.createTHead();
    var body = table.createTBody();

    // From here on out we will create a row and insert a cell in that row
    var headerRow = header.insertRow(0);
    var headerCell = headerRow.insertCell(0);
    // In this line we will update the cells value with the "card" object's title variable
    headerCell.innerHTML = card["title"];


    var priceRow = body.insertRow(0);
    var priceCell = priceRow.insertCell(0);
    priceCell.innerHTML = "Price";

    // This will create a second column in the same row when we use .insertCell(-1)
    var priceCellColumn2 = priceRow.insertCell(-1);
    priceCellColumn2.innerHTML = card["price"];
    // We track the price cell by setting the id to '(coin) + "price-cell"'
    priceCellColumn2.id = card['title'] + 'price-cell';

    // Append the table element to the 'container' div
    div.appendChild(table);
    document.getElementById('container').appendChild(div)

    dragElement(document.getElementById(div.id));
}


// This function loops through the watchlist and opens a websocket using the title of the coin in question, then
// adds event listener to loop listen for the stream of data and add those prices to the cards.
function updatePrices(watchList) {
    watchList.forEach(element => {
        let socket = new WebSocket('wss://stream.binance.com:9443/ws/' + element['title'].toLowerCase() + 'usdt@trade');
        socket.addEventListener('message', function(event) {
            let data = JSON.parse(event.data);

            // This is where we add the price data to the HTML
            document.getElementById(element['title'] + 'price-cell').innerHTML = Number(data.p).toFixed(3);
        });
    });
}


// This function will be called when the 'Add Coin' button is clicked and will append an input element to 'add-coin-input'.
function createAddCoinForm() {
    // First we check if there is already an input box in the 'add-coin-input' div.
    if (!document.getElementById('add-coin-input').hasChildNodes()) {
        var form = document.createElement('input');
        form.id = 'input';
        document.getElementById('add-coin-input').appendChild(form);
    }
}

// This function will be called when the 'Push to Watchlist' button is clicked and will create a card object that is passed to 
// createCard(card) function.
function createCardObject(coin) {
    let card = {
        title: coin == null ? document.getElementById('input').value : coin,
        change: 1,
        price: 1,
        high: 1,
        low: 1,
    }

    // Push the new 'card' object containing price info to watchList
    watchlist.push(card);

    // Function call
    createCard(card);
    updatePrices(watchlist);
}


// This function will create 4 default cards for the user to see something on the screen
function createDefaultCards() {
    let coins = ['BTC', 'ETH', 'LTC', 'DOGE'];
    let card = {}
    coins.forEach(c => {
        card = {
                title: c,
                change: 1,
                price: 1,
                high: 1,
                low: 1,
            }
            // Push the new 'card' object containing price info to watchList
        watchlist.push(card);

        // Function call
        createCard(card);
    });

}

// This will push to the body a 'dark' theme
function pushDark() {
    let body = document.getElementById("body");
    body.classList.add('dark');
    body.classList.remove('light');
    body.classList.remove('grad');
}

// This will push to the body a 'dradient' theme
function pushLight() {
    let body = document.getElementById("body");
    body.classList.add('light');
    body.classList.remove('dark');
    body.classList.remove('grad');
}

// This will push to the body a 'dark' theme
function pushGrad() {
    let body = document.getElementById("body");
    body.classList.add('grad');
    body.classList.remove('light');
    body.classList.remove('dark');
}


// Grab some elements by id
let gradButton = document.getElementById('grad-button');
let lightButton = document.getElementById('light-button');
let darkButton = document.getElementById('dark-button');

// Add event listeners for 'click's
gradButton.addEventListener('click', pushGrad);
lightButton.addEventListener('click', pushLight);
darkButton.addEventListener('click', pushDark);



// To show default cards we will card this function along with the 4 preset coins stored in 'ranges' dictionary.
createDefaultCards();
// This will loop through the watchlist and push the data from the websockets to the page.
updatePrices(watchlist);