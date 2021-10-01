var itemList = {};
var total = 0;
var taxes = 0;

// Add each item and product to the itemList dictionary if they have values
function addItem() {
    var item = document.getElementById("name-input").value;
    var price = document.getElementById("price-input").value;

    if (item && price != NaN) {
        itemList[item] = price;
    } else {
        alert("Please enter values")
    }
}

// Calculate tax buy looping through the dictionary and totaling up the prices
function calculateTax() {
    console.log("Items: ")
    for (const [key, value] of Object.entries(itemList)) {
        console.log(key + " $" + value)
        total = Number(total) + Number(value)
    }

    // Taxes are determined after the subtotal is calculated by multiplying the 6% tax rate
    taxes = total * 0.06

    // Taxes are added to total
    total = total + taxes

    console.log("Taxes: $" + taxes)

    console.log("Total: $" + total)

}