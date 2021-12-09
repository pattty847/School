const CoinGecko = require('coingecko-api');

const CoinGeckoClient = new CoinGecko();

var func = async() => {
    let coin = await CoinGeckoClient.coins.fetch('bitcoin', {})
    console.log(coin)
};


let coins = {
    "btc-change": document.getElementById("btc-change"),
    "btc-price": document.getElementById("btc-price"),
};

function updateValues() {
    coins['btc-price'].innerHTML = func().coin
    coins['btc-change'].innerHTML = "1.4%";
}

updateValues();