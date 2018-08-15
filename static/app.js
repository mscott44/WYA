document.addEventListener("DOMContentLoaded", function(event) {
  refreshMessages();
  document.querySelector('#myButton').addEventListener('click', sendMessageClicked);
});

function sendMessageClicked() {
  postMessage().then(function() {
    refreshMessages();
  })
}


function postMessage() {
  // Call fetch on the chat api.
  const textarea = document.querySelector('#message');
  const message = textarea.value;
  return fetch('./chat?from=213&to=562&content=' + encodeURI(message), {
    method: 'POST'
  }).then(function() {
    textarea.value = '';
  });
}


function refreshMessages(from, to) {
  fetch('./chat?from=213&to=562')
      .then(function(response) {
        return response.json();
      })
      .then(function(messages) {
        const messagesDiv = document.querySelector('#messages');
        messagesDiv.innerHTML = '';
        messages.forEach(function(message) {
          const li = document.createElement('li');
          li.innerHTML = message.content;
          messagesDiv.append(li);
        });
      });
}
