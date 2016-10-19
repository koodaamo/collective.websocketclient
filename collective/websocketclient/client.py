import time

from zope.component import getUtility
from websocket import create_connection, setdefaulttimeout
from websocket._exceptions import WebSocketConnectionClosedException

from .interfaces import IWebSocketConnectionManager


class WebSocketConnection():

   TIMEOUT = 5

   def __init__(self, name, host, port, timeout=None):
      self.name = name
      self.host = host
      self.port = port
      self.timeout = timeout or self.TIMEOUT
      self.active = False

   def connect(self):
      connstr = "ws://%s:%s" % (self.host, self.port)
      self.connection = create_connection(connstr, timeout=self.timeout)
      self.active = True

   def send(self, data):
      try:
         return self.connection.send(data)
      except:
         self.connection = None
         self.active = False
         raise

   def receive(self):
      try:
         return self.connection.recv()
      except WebSocketConnectionClosedException:
         self.connection = None
         self.active = False
         raise

   def close(self):
      self.connection.close()
      self.connection = None
      self.active = False

   def settimeout(self, seconds):
      self.timeout = timeout


def transmit(msg, mgr=None, conn=None):
   "blocking sender that tries to reconnect upon failure"

   connection = conn or (mgr or getUtility(IWebSocketConnectionManager)).getConnection()

   try:
      connection.send(msg)
      return connection.receive()
   except:
      time.sleep(0.1)
      connection = manager.getConnection()
      try:
         connection.send(msg)
         return connection.receive()
      except:
         raise Exception("could not send/receive over websocket")
