(function (document) {
  'use strict';

  var app = document.querySelector('#app');
  app.data = [['', 31],['', 28],['', 31],['', 31],['', 28],['', 31],['', 31],['', 28],['', 31],['', 31],['', 28],['', 31]];
  app.connected = false;
  setTimeout(function () {
    app.data.push(['', 100]);
    document.getElementById('mainchart').rows = app.data;
  }, 5000);

  /* quit server */
  /*document.querySelector('#restartButton').addEventListener('click', function () {
     var msg = { topic: 'quit', content: '' };
     websocket.send(JSON.stringify(msg));
   });*/

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
      document.getElementById('mainchart').rows = app.data;
    }
  };

})(document);
