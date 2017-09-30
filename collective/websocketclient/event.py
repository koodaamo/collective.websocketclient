import threading

from zope.component import adapter, getUtility, ComponentLookupError
from plone.registry.interfaces import IRecordModifiedEvent

from .interfaces import IWebSocketConnectionSchema, IWebSocketConnectionManager

from logging import getLogger
log = getLogger('collective.websocketclient')


#@adapter(IWebSocketConnectionSchema, IRecordModifiedEvent)
def onWebSocketConfigChange(event):
   "reconnect for the new settings to take effect"

   if event.record.interface == IWebSocketConnectionSchema:

      # we may get events even if the profile providing the manager is not
      # installed yet; so just fail silently if we cannot get the manager
      try:
         mgr = getUtility(IWebSocketConnectionManager)
      except ComponentLookupError:
         pass
      else:
         mgr.scheduleReconnect()
