"use strict";

const CoinGecko = require('coingecko-api');

//2. Initiate the CoinGecko API Client
const CoinGeckoClient = new CoinGecko();

//3. Make calls
var func = async() => {
    let data = await CoinGeckoClient.ping();
    console.log(data);
};