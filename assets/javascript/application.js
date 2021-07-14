import $ from 'jquery';
window.jQuery = $;
window.$ = $;

function component() {
  const element = document.createElement('div');
  element.innerHTML = 'Hello webpack';
  return element;
}

document.addEventListener('DOMContentLoaded', (event) => {
  document.body.appendChild(component());
})

$( document ).ready(function(){
  closeMessages();
})

function closeMessages() {
  $('.ui.message .close.icon').on('click', function(event) {
    $(event.target).closest('.ui.message').addClass('hidden');
  })
}

alert('toto')