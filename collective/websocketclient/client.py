from websocket import create_connection


class WebSocketConnection():

   TIMEOUT = 5

   def __init__(self, name, host, port):
      self.name = name
      self.host = host
      self.port = port

   def connect(self):
      self.connection = create_connection("ws://%s:%s" % (self.host, self.port))

   def send(self, data):
      return self.connection.send(data)

   def receive(self):
      return self.connection.recv()

   def close(self):
      self.connection.close()

