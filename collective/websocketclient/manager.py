# -*- coding: utf-8 -*-
from collective.websocketclient.interfaces import IWebSocketConnectionConfig
from collective.websocketclient.interfaces import IWebSocketConnectionManager
from collective.websocketclient.interfaces import IZCMLWebSocketConnectionConfig
from collective.websocketclient.local import getLocal
from collective.websocketclient.local import setLocal
from collective.websocketclient.client import WebSocketConnection

import logging

from persistent import Persistent
from socket import error
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import implements

from .client import WebSocketConnection

logger = logging.getLogger('collective.websocketclient.manager')
logger.setLevel(logging.DEBUG)

marker = object()


class WebSocketConnectionConfig(Persistent):

   implements(IWebSocketConnectionConfig)

   def __init__(self):
      self.name = None
      self.host = None
      self.port = None

   def getId(self):
      "return a unique id to be used with GenericSetup; determines xml file name"
      return 'websocketclient'


class ZCMLWebSocketConnectionConfig(object):
    "Connection values that can be configured through zcml"

    implements(IZCMLWebSocketConnectionConfig)

    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port


class WebSocketConnectionManager(object):
   "a thread-local connection manager for websocket connections"

   implements(IWebSocketConnectionManager)

   lock = False

   def setHost(self, name='', host='localhost', port=80):
      "set connection parameters"
      config = getUtility(IWebSocketConnectionConfig)
      config.name = name
      config.host = host
      config.port = port
      self.closeConnection(clearSchema=True)

   def closeConnection(self, clearSchema=False):
      "close the current connection, if any"
      logger.debug('closing connection')
      conn = getLocal('connection')
      if conn is not None:
         conn.close()
         setLocal('connection', None)

   def getConnection(self):
      "returns an existing connection or opens one"

      config = getUtility(IWebSocketConnectionConfig)
      conn = getLocal('connection')
      if conn is not None:
         logger.debug("returning existing websocket connection")
         return conn

      zcmlconfig = queryUtility(IZCMLWebSocketConnectionConfig)
      if zcmlconfig is not None:
         # use connection parameters defined in zcml...
         logger.debug('opening connection to %s', zcmlconfig.host)
         conn = WebSocketConnection(zcmlconfig.name, zcmlconfig.host, zcmlconfig.port)
         setLocal('connection', conn)
      elif config.host and config.port:
         # otherwise use connection parameters defined in control panel...
         logger.debug('opening connection to %s', config.host)
         conn = WebSocketConnection(config.name, config.host, config.port)
         setLocal('connection', conn)

      return conn


