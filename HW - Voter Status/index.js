function getVoterStatus() {
    let age = prompt("Enter your age to continue: ")
    if (age != NaN && age >= 18) {
        let status = prompt("Have you registered to vote yet?")
        if (status == "no" || status == 'yes') {
            if (status == 'yes') {
                alert("You are already signed up to vote!")
            } else if (status == 'no') {
                alert("You must register to vote first")
            }
        } else {
            console.log("This is a 'yes' or 'no' question. Reload the webpage.")
        }
    } else {
        console.log("Make sure you enter a number and are 18 years or older.")
    }
}

getVoterStatus()