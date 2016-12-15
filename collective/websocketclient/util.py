"""

Utilities for using the websocket-to-wamp proxy for RPC calls & PUBSUB events.

"""

import json
from zope.component import getUtility
from . import WebSocketTimeoutException, WebSocketConnectionClosedException
from .interfaces import IWebSocketConnectionManager


def transmit(msg):
   "convenience function for sending and receiving"
   mgr = getUtility(IWebSocketConnectionManager)
   connection = mgr.getConnection()
   try:
      connection.send(msg)
      return connection.receive()
   except (WebSocketTimeoutException, IOError, WebSocketConnectionClosedException):
      connection = mgr.reConnect()
      connection.send(msg)
      return connection.receive()

def call(realm, method, *args, **kwargs):
   "send a websocket JSON message that can be translated to a WAMP RPC call by wwproxy"
   msg = {"realm":realm, "method":method, "args":args, "kwargs":kwargs}
   try:
      response = transmit(json.dumps(msg))
   except Exception as exc:
      print(exc.__class__.__name__ + ": " + str(exc))
      return (501, str(exc))
   return json.loads(response)

def publish(realm, event, *args, **kwargs):
   "send a websocket JSON message that can be translated to a WAMP PUBSUB event by wwproxy"
   msg = {"realm": realm, "event":event,  "args":args, "kwargs":kwargs}
   try:
      response = transmit(json.dumps(msg))
   except Exception as exc:
      return (501, str(exc))
   return json.loads(response)
