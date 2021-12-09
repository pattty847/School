"use strict";
// This variable will store each card in an array called 'watchlist'.
// When a user wants to add a particular coin to their watch list we will first create a card object and push it to this array.
let watchlist = [];


// This is where we create a barebones card object.
// The card object is a panel that displays each property on a table.
let card = {
    title: "",
    price: "",
    change: "",
    high: "",
    low: "",
}

// This function will be called with user input and will create a card object that will be pushed to the watchlist
function createCard(card) {
    var table = document.getElementById('table');

    var header = table.createTHead();
    var body = table.createTBody();

    var headerRow = header.insertRow(0);
    var headerCell = headerRow.insertCell(0);
    headerCell.innerHTML = "<b>Coin</b>";


    var priceRow = body.insertRow(0);
    var priceCell = priceRow.insertCell(0);
    priceCell.innerHTML = "<b>Price</b>";

    var priceCellColumn2 = priceRow.insertCell(-1);
    priceCellColumn2.innerHTML = "0";


    var changeRow = body.insertRow(0);
    var changeCell = changeRow.insertCell(0);
    changeCell.innerHTML = "<b>Change</b>";

    var changeCellColumn2 = changeRow.insertCell(-1);
    changeCellColumn2.innerHTML = "0";


    var highRow = body.insertRow(0);
    var highCell = highRow.insertCell(0);
    highCell.innerHTML = "<b>High</b>";

    var highCellColumn2 = highRow.insertCell(-1);
    highCellColumn2.innerHTML = "0";


    var lowRow = body.insertRow(0);
    var lowCell = lowRow.insertCell(0);
    lowCell.innerHTML = "<b>Low</b>";

    var lowCellColumn2 = lowRow.insertCell(-1);
    lowCellColumn2.innerHTML = "0";
}

createCard();