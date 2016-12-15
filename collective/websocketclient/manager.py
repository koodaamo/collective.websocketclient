# -*- coding: utf-8 -*-

import socket, logging
from collections import namedtuple
import threading
from threading import Lock

from websocket._exceptions import WebSocketException
from persistent import Persistent
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import implements
from plone.registry.interfaces import IRegistry

from .interfaces import IWebSocketConnectionConfig
from .interfaces import IWebSocketConnectionManager
from .interfaces import IZCMLWebSocketConnectionConfig
from .local import getLocal, setLocal
from .client import WebSocketConnection
from . import WebSocketConfigException

logger = logging.getLogger('collective.websocketclient.manager')

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
   "thread-local connections manager for websocket connections"

   implements(IWebSocketConnectionManager)

   lock = False

   reconnect = [] # track reconnects due to connection change
   lock = Lock()

   def setHost(self, name='', host='localhost', port=80):
      "set connection parameters"
      config = getUtility(IWebSocketConnectionConfig)
      config.name = name
      config.host = host
      config.port = port
      self.closeConnection()

   def closeConnection(self):
      "close the current connection, if any"
      logger.info('closing connection')
      conn = getLocal('connection')
      if conn is not None:
         conn.close()
         setLocal('connection', None)

   def scheduleReconnect(self):
      "schedue reconnect for this thread"
      logger.info("scheduling reconnect")
      for t in threading.enumerate():
         if "zeo" in t.name and t.ident not in self.reconnect:
            self.reconnect.append(t.ident) # thread-safe

   def getControlPanelConfig(self):
      "get config from control panel (registry)"

      registry = getUtility(IRegistry)
      prefix = 'collective.websocketclient.interfaces.IWebSocketConnectionSchema'
      name = registry.get(prefix+'.'+"name")
      host = registry.get(prefix+'.'+"host")
      port = registry.get(prefix+'.'+"port")

      # only return complete config
      if name and host and port:
         ControlPanelConfig = namedtuple('ControlPanelConfig', 'name host port')
         return ControlPanelConfig(name, host, port)
      else:
         return None

   def getZCMLConfig(self):
      "get ZCML config or None"
      return queryUtility(IZCMLWebSocketConnectionConfig)

   def reConnect(self):
      self.closeConnection()
      return self.getConnection()

   def getConnection(self):
      "returns an existing connection or opens and connects one"

      # if we have an existing connection
      existing_connection = getLocal('connection')
      if existing_connection is not None and existing_connection.active:

         # if reconnect flag is not set
         if threading.current_thread().ident not in self.reconnect:
            logger.info("returning existing websocket connection")
            return existing_connection

         # if it's set, close connection, clear flag and create new connection
         else:
            self.closeConnection()
            with self.lock:
               self.reconnect.remove(threading.current_thread().ident)
            logger.info("reconnect flag set; closing, clearing flag & creating new")

      # connection config from control panel (registry) or ZCML
      cfg = self.getControlPanelConfig() or self.getZCMLConfig()
      if not cfg:
         raise WebSocketConfigException("proper websocket config not provided")

      # create connection
      logger.info("opening new connection '%s' to %s:%i" % (cfg.name, cfg.host, cfg.port))
      connection = WebSocketConnection(cfg.name, cfg.host, cfg.port)

      # open connection
      try:
         connection.connect()
      except (socket.error, WebSocketException) as exc:
         logger.error("failure opening '%s' to %s:%i: %s" % (cfg.name, cfg.host, cfg.port, str(exc)))
         setLocal('connection', None)
         raise

      setLocal('connection', connection)
      return connection


