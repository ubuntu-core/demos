# -*- coding: utf-8 -*-
# Copyright (C) 2016 Canonical
#
# Authors:
#  Didier Roche
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import json
import logging
import posixpath
import urllib
import os
import sys
import threading

# enable importing SimpleWebSocketServer as if it was an external module
sys.path.insert(0, os.path.dirname(__file__))
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

from tools import Singleton

logger = logging.getLogger(__name__)


class WebClientsCommands(WebSocket):

    clients = []
    server = None
    faces_detect_data_list = []

    def handleMessage(self):
        """Message received from a client"""
        logger.debug("Received from {}: {}".format(self.address[0], self.data))
        data = json.loads(self.data)
        topic = data["topic"]
        message = data["content"]

        if topic == "quit":
            logger.info("Exit requested")
            os._exit(0)

    def handleConnected(self):
        """New client connected"""
        logger.info("New client: {}".format(self.address[0]))
        WebClientsCommands.clients.append(self)
        self._sendFacesDetect()

    def handleClose(self):
        """Client disconnected"""
        logger.info("Client disconnected: {}".format(self.address[0]))
        WebClientsCommands.clients.remove(self)

    @staticmethod
    def sendFacesDetectAll(new_faces_detect_data_list):
        """Send face detect list to all clients"""
        WebClientsCommands.faces_detect_data_list = new_faces_detect_data_list
        for client in WebClientsCommands.clients:
            client._sendFacesDetect()

    def _sendFacesDetect(self):
        """Send face detection list points"""
        self.__sendMessage("facesdetectlist", self.faces_detect_data_list)

    @staticmethod
    def sendNewFacesEntryAll(new_faces_detect_data_list, new_entry):
        """Send new face detection entry to all clients"""
        WebClientsCommands.faces_detect_data_list = new_faces_detect_data_list
        for client in WebClientsCommands.clients:
            client._sendNewFacesEntry(new_entry)

    def _sendNewFacesEntry(self, new_entry):
        """Send new face detection entry"""
        self.__sendMessage("newentry", new_entry)

    def __sendMessage(self, topic, content):
        """Wrap object and message in a json payload"""
        message_obj = {'topic': topic, 'content': content}
        msg = unicode(json.dumps(message_obj))
        logger.debug("Sending: " + msg)
        self.sendMessage(msg)


class CommandSocketServer(threading.Thread):
    """Threaded Command websocket"""

    def __init__(self, port, *args, **kwargs):
        super(CommandSocketServer, self).__init__(*args, **kwargs)
        self.port = port

    def run(self):
        """Start this websocket server in a separate thread"""
        WebClientsCommands.server = SimpleWebSocketServer('', self.port, WebClientsCommands)
        logger.info("Command socket server is on {}".format(self.port))
        WebClientsCommands.server.serveforever()


class OurHttpRequestHandler(SimpleHTTPRequestHandler):

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Stolen from SimpleHTTPSRequestHandler with a different base path

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'www')
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path


class SocketCommands(object):
    """Contain the list commands to send to clients"""
    __metaclass__ = Singleton

    def __init__(self, server):
        self.clients = []
        self.server = server


class StaticServer(threading.Thread):
    """Threaded Static http server"""

    def __init__(self, port, *args, **kwargs):
        super(StaticServer, self).__init__(*args, **kwargs)
        self.port = port

    def run(self):
        """Start this http server in a separate thread"""
        server_address = ('', self.port)

        httpd = HTTPServer(server_address, OurHttpRequestHandler)

        sa = httpd.socket.getsockname()
        logger.info("Serving static files on {} port {}".format(sa[0], sa[1]))
        httpd.serve_forever()
