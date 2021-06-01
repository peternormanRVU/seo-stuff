//
console.log(data);

//

var value = 1
var loc = 'screenshots/' + value + '.png'

document.getElementById('content').innerText = document.getElementById('content-' + value).innerText;
document.getElementById('words').innerText = document.getElementById('words-' + value).innerText;
document.getElementById('images').innerText = document.getElementById('images-' + value).innerText;
document.getElementById('link').href = document.getElementById('link-' + value).innerText;
document.getElementById('page-h1').innerText = document.getElementById('h1-' + value).innerText;
document.getElementById('page-title').innerText = document.getElementById('title-' + value).innerText;
document.getElementById('page-description').innerText = document.getElementById('description-' + value).innerText;
document.getElementById('page-h2').innerHTML = document.getElementById('h2-' + value).innerHTML;
document.getElementById('page-h3').innerHTML = document.getElementById('h2-' + value).innerHTML;
document.getElementById('h3-num').innerText = document.getElementById('len-h3-' + value).innerText;
document.getElementById('h2-num').innerText = document.getElementById('len-h2-' + value).innerText;

function changeValue() {
  if (value > 9) {
    value = 1;
    loc = 'screenshots/' + value + '.png'
   } else {
    value = value + 1;
    loc = 'screenshots/' + value + '.png'
   }
   document.getElementById('image').src = loc;
   document.getElementById('rank').innerText = value;
   document.getElementById('words').innerText = document.getElementById('words-' + value).innerText;
   document.getElementById('images').innerText = document.getElementById('images-' + value).innerText;
   document.getElementById('content').innerText = document.getElementById('content-' + value).innerText;
   document.getElementById('link').href = document.getElementById('link-' + value).innerText;
   document.getElementById('page-h1').innerText = document.getElementById('h1-' + value).innerText;
   document.getElementById('page-title').innerText = document.getElementById('title-' + value).innerText;
   document.getElementById('page-description').innerText = document.getElementById('description-' + value).innerText;
   document.getElementById('page-h2').innerHTML = document.getElementById('h2-' + value).innerHTML;
   document.getElementById('page-h3').innerHTML = document.getElementById('h3-' + value).innerHTML;
   document.getElementById('h3-num').innerText = document.getElementById('len-h3-' + value).innerText;
   document.getElementById('h2-num').innerText = document.getElementById('len-h2-' + value).innerText;
}

