import threading

from zope.component import adapter, getUtility
from plone.registry.interfaces import IRecordModifiedEvent

from .interfaces import IWebSocketConnectionSchema, IWebSocketConnectionManager

from logging import getLogger
log = getLogger('collective.websocketclient')


#@adapter(IWebSocketConnectionSchema, IRecordModifiedEvent)
def onWebSocketConfigChange(event):
   #log.info(event.record)
   #log.info(event.oldValue)
   #log.info(event.newValue)
   mgr = getUtility(IWebSocketConnectionManager)
   mgr.scheduleReconnect()
