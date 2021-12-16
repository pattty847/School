let socket = new WebSocket("wss://fstream.binance.com/ws/btcusdt@aggTrade");

//                 Aggregate     Mark Stream      Market $/3s
const endPoints = ['@aggTrade', '@markPrice', '!markPrice@arr@1s']

let mCount = 0;
let roc = 0;
let time = 0;

socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    mCount++;
    console.log(`p: ${data.p}\nq: ${Number(data.q*data.p).toFixed(2)}\nMM: ${data.m}`);
    document.getElementById('mm').innerText = (`MM: ${mCount}`);
};

socket.onclose = function(event) {
    if (event.wasClean) {
        alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        alert('[close] Connection died');
    }
};

socket.onerror = function(error) {
    alert(`[error] ${error.message}`);
};