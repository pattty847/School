var prices = [];

function getPrices() {
    alert("Enter the prices to your grocery items 1 at a time. When finished type 'stop'.")
    while (true) {
        input = prompt('Item Price: ')
        if (input == 'stop') { break } else {
            prices.push(input)
        }
    }
    let total = 0
    for (let i = 0; i < prices.length; i++) {
        total += Number(prices[i])
    }



    alert("Total: " + total)
    alert("Count: " + prices.length)
    alert("Average: " + total / prices.length)
    alert("Minimum: " + Math.min.apply(Math, prices))
    alert("Maximum: " + Math.max.apply(Math, prices))
}