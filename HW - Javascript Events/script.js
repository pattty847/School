function push_dark() {
    let body = document.getElementById("body");
    body.classList.add('dark');
    body.classList.remove('light')
    body.classList.remove('grad')
}

function push_light() {
    let body = document.getElementById("body");
    body.classList.add('light');
    body.classList.remove('dark')
    body.classList.remove('grad')
}

function push_grad() {
    let body = document.getElementById("body");
    body.classList.add('grad');
    body.classList.remove('light')
    body.classList.remove('dark')
}


let grad_button = document.getElementById('grad-button');
let light_button = document.getElementById('light-button');
let dark_button = document.getElementById('dark-button');

grad_button.addEventListener('click', push_grad);
light_button.addEventListener('click', push_light);
dark_button.addEventListener('click', push_dark);