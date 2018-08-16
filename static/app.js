const dropdown = document.querySelector("#userDropdown");

document.addEventListener("DOMContentLoaded", function(event) {
  const localStorageValue = localStorage.getItem('otherUser');
  if (localStorageValue) {
    dropdown.value = localStorageValue;
  }
  refreshMessages();
  document.querySelector('#myButton').addEventListener('click', sendMessageClicked);
});

dropdown.addEventListener('change', () => {
  const otherUser = dropdown.options[dropdown.selectedIndex].value;
  localStorage.setItem('otherUser', otherUser);
  refreshMessages();
});

function getReceiver() {
  return localStorage.getItem('otherUser') ||
    dropdown.options[dropdown.selectedIndex].value;
}

function sendMessageClicked() {
  postMessage().then(function() {
    refreshMessages();
  })
}

function postMessage() {
  // Call fetch on the chat api.
  const textarea = document.querySelector('#message');
  const receiver = getReceiver();
  const sender = document.querySelector("#username").innerHTML;
  const message = textarea.value;

  return fetch(`./chat?from=${encodeURI(sender)}&to=${encodeURI(receiver)}&content=${encodeURI(message)}`, {
    method: 'POST'
  }).then(function() {
    textarea.value = '';
  });
}


function refreshMessages() {
  const other = getReceiver();
  const me = document.querySelector("#username").innerHTML;
  fetch(`./chat?me=${encodeURI(me)}&other=${encodeURI(other)}`)
      .then(function(response) {
        return response.json();
      })
      .then(function(messages) {
        console.log('REFRESHING');
        const messagesDiv = document.querySelector('#messages');
        messagesDiv.innerHTML = '';
        messages.forEach(function(message) {
          const li = document.createElement('li');
          li.classList.add(message.sender === me ? "fromMe" : "fromThem");
          li.innerHTML = `${message.content}`;
          messagesDiv.append(li);
        });
      });
}
