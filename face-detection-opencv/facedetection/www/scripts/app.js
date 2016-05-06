(function (document) {
  'use strict';

  var app = document.querySelector('#app');
  app.data = [];
  app.connected = false;

  // imports are loaded and elements have been registered
  window.addEventListener('WebComponentsReady', function () {

    /* quit server */
    document.querySelector('#restartButton').addEventListener('click', function () {
       var msg = { topic: 'quit', content: '' };
       websocket.send(JSON.stringify(msg));
     });

    var mainchart = document.getElementById('mainchart');
    var screenimg = document.getElementById('screenimg');

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

          // we would use this.push in a Polymer() element to keep the databinding working
          app.data.push(message.content);
          break;
        case 'facesdetectlist':
          app.data = message.content;
          break;
        default:
          console.log('Unknown message');
      }

      // we need to make an array copy because it won't redraw with the same reference, even after a manual redraw call
      mainchart.rows = app.data.slice();
      screenimg.src = "dynamics/last_screen.png?" + new Date().getTime();
    };

  });

})(document);
