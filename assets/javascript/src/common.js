import $ from 'jquery';
window.jQuery = $;
window.$ = $;

$( document ).ready(function(){
  closeMessages();
})

function closeMessages() {
  $('.ui.message .close.icon').on('click', function(event) {
    $(event.target).closest('.ui.message').addClass('hidden');
  })
}
