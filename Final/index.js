"use strict";

// This variable will store each card object in an array called 'watchlist'.
// When a user wants to add a particular coin to their watch list we will first create a card object and push it to this array.
let watchlist = [];


// This is where we create a barebones card object.
// The card object is a panel that displays each property on a table.

// This function will be called with user input and will create a card object that will be pushed to the watchlist
function createCard(card) {



    // Declare a table variable that is initialized to a table element
    var table = document.createElement('table');
    table.className = 'card';

    // We set our table's header and body with these functions
    var header = table.createTHead();
    var body = table.createTBody();

    // From here on out we will create a row and insert a cell in that row
    var headerRow = header.insertRow(0);
    var headerCell = headerRow.insertCell(0);
    // In this line we will push an empty value that will later be updated
    headerCell.innerHTML = card["title"];


    var priceRow = body.insertRow(0);
    var priceCell = priceRow.insertCell(0);
    priceCell.innerHTML = "Price";

    var priceCellColumn2 = priceRow.insertCell(-1);
    priceCellColumn2.innerHTML = card["price"];


    var changeRow = body.insertRow(0);
    var changeCell = changeRow.insertCell(0);
    changeCell.innerHTML = "Change";

    var changeCellColumn2 = changeRow.insertCell(-1);
    changeCellColumn2.innerHTML = card["change"];


    var highRow = body.insertRow(0);
    var highCell = highRow.insertCell(0);
    highCell.innerHTML = "High";

    var highCellColumn2 = highRow.insertCell(-1);
    highCellColumn2.innerHTML = card["high"];


    var lowRow = body.insertRow(0);
    var lowCell = lowRow.insertCell(0);
    lowCell.innerHTML = "Low";

    var lowCellColumn2 = lowRow.insertCell(-1);
    lowCellColumn2.innerHTML = card["low"];

    // Append the table element to the 'container' div
    document.getElementById('container').appendChild(table);

    console.log(watchlist);
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
// createCard() function. It will use other functions to obtain price data.
function createCardObject() {
    var input = document.getElementById('input').value;
    var card = {
        title: input,
        price: 123,
        change: 10,
        high: 130,
        low: 100,
    };

    watchlist.push(card);
    // This is where I need to impliment CoinGecko Api and get initial coin data.
    createCard(card);
}