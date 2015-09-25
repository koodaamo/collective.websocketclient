from websocket import create_connection, setdefaulttimeout
from websocket._exceptions import WebSocketConnectionClosedException

class WebSocketConnection():

   TIMEOUT = 5

   def __init__(self, name, host, port, timeout=None):
      self.name = name
      self.host = host
      self.port = port
      self.timeout = timeout
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
