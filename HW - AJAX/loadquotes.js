function loadQuotes() {

    var ajaxRequest = new XMLHttpRequest();
    ajaxRequest.onreadystatechange = function() {
        
        if(ajaxRequest.readyState == 4) {
            if(ajaxRequest.status == 200) {
                var responseObject = JSON.parse(ajaxRequest.responseText);

                var randomQuoteArray = responseObject.quotes;
                var randomIndex = Math.floor(Math.random() * randomQuoteArray.length);
                var quote = randomQuoteArray[randomIndex];

                document.getElementById("quote").innerHTML = quote.q;
            }else{
                console.log("Status error: " + ajaxRequest.status);
            }
        }else{
            console.log("Ignored readyState: " + ajaxRequest.readyState);
        }
    }
    ajaxRequest.open("GET", "data.json");
    ajaxRequest.send();
}