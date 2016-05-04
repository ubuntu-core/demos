(function (document) {
  'use strict';

  var app = document.querySelector('#app');

  app.connected = false;

    /* quit server */
    document.querySelector('#restartButton').addEventListener('click', function () {
       var msg = { topic: 'quit', content: '' };
       websocket.send(JSON.stringify(msg));
     });

    // only here get the websocket status back and toggle values if needed
    var websocket = new ReconnectingWebSocket('ws://' + window.location.hostname + ':8043/');
    websocket.onopen = function () {
      console.log('websocket connected');
      app.connected = true;
    };

    websocket.onclose = function () {
      console.log('websocket disconnected');
      app.connected = false;
    };

    websocket.onerror = function (e) {
      console.log('Error in websocket: ' + e.data);
    };

    websocket.onmessage = function (e) {
      console.log('Message received: ' + e.data);
      var message = JSON.parse(e.data);
      switch (message.topic) {
        case 'newentry':
          //message.content;
          break;
        case 'facesdetectlist':
          // message.content;
          break;
        default:
          console.log('Unknown message');
      }
    };

  });

})(document);
