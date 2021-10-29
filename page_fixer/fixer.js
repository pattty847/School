'use strict';

// Leave this line alone.
document.addEventListener("DOMContentLoaded", function() {

    let title = document.getElementById('main-title');
    title.innerHTML = 'Fix <em>this</em> Page'


    let image = document.getElementsByTagName('img')[0]
    image.src = 'mars.jpg'
    image.width = 500
    image.height = 500

    document.getElementsByTagName('ol')[0].className = 'engage'

    document.getElementsByTagName('h3')[0].textContent = 'List of things we need to learn about JavaScript'


    let knowledge_list = document.getElementsByTagName('ul')[0]
    let knowledge_items = knowledge_list.children
    knowledge_list.id = 'knowledge-list'

    let first_item = knowledge_list.firstChild

    let new_line_1 = document.createElement('li')
    new_line_1.appendChild(document.createTextNode('Relation to HTML'))
    knowledge_list.insertBefore(new_line_1, first_item)

    let new_line_2 = document.createElement('li')
    new_line_2.appendChild(document.createTextNode('Using the DOM'))
    knowledge_list.appendChild(new_line_2)

    let conditionals = knowledge_items[2]

    let new_line_3 = document.createElement('li')
    new_line_3.appendChild(document.createTextNode('Syntax'))
    knowledge_list.insertBefore(new_line_3, conditionals)

    let deleted_line = knowledge_items[4]
    knowledge_list.removeChild(deleted_line)

    let extra_credit = document.getElementsByTagName('p')[0]
    let new_line_4 = document.createElement('h6')
    new_line_4.appendChild(document.createTextNode('For extra credit change this tag to an h6 tag.'))
    extra_credit.replaceWith(new_line_4)

    let new_line_5 = document.createElement('aside')
    new_line_5.appendChild(document.createTextNode('JavaScript is only fun when we can use it to manipulate HTML!'))
    document.body.appendChild(new_line_5)

    // Leave this line alone.
});