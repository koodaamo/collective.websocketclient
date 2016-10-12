Introduction
============

Send test messages via the `@@websocketsend` view, using either GET or POST. Pass a single
argument called `msg`, containing the message to be sent.

Code usage example::

   import socket
   from zope.component import getUtility
   from websocket._exceptions import WebSocketConnectionClosedException
   from .interfaces import IWebSocketConnectionManager

   manager = getUtility(IWebSocketConnectionManager)
   connection = manager.getConnection()
   
   if connection is None:
      print "could not connect!"
   else:
      try:
         connection.send(msg)
         print self.connection.receive()
      except (WebSocketConnectionClosedException, socket.error):
         # failed; if you want to retry, do so by first getting a new connection, ie. call manager.getConnection()
         print "failure!"
  
