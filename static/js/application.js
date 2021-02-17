// Any JS code written here will be used in all pages of the app

$( document ).ready(function(){
  closeMessages();
})

function closeMessages() {
  $('.ui.message .close.icon').on('click', function(event) {
    $(event.target).closest('.ui.message').addClass('hidden');
  })
}
