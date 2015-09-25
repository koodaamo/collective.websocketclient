import socket
from zope.component import getUtility
from Products.Five import BrowserView

from websocket._exceptions import WebSocketConnectionClosedException

from .interfaces import IWebSocketConnectionManager

class WebSocketSender(BrowserView):

   def __init__(self, context, request):
      self.context = context
      self.request = request
      self.manager = getUtility(IWebSocketConnectionManager)
      self.connection = self.manager.getConnection()

   def send_and_receive(self, msg):
      self.connection.send(msg)
      return self.connection.receive()

   def __call__(self):
      connection = self.connection or self.manager.getConnection()
      if connection is None:
         return "No connection & could not reconnect :("

      form = self.request.form
      message = form.get("msg", "Hello World!")

      try:
         return self.send_and_receive(message)
      except (WebSocketConnectionClosedException, socket.error):
         # retry once
         self.connection = self.manager.getConnection()
         if self.connection:
            try:
               return self.send_and_receive(message)
            except (WebSocketConnectionClosedException, socket.error):
               return "Connection was closed, no reply received!"
