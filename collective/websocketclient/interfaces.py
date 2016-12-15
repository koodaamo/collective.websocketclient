from zope.interface import Interface
from zope.schema import TextLine, Int

from . import _

class IWebSocketConnectionSchema(Interface):
   "connection data schema"

   name = TextLine(
      title=_('label_name', default=u'Name'),
      description=_(
         'help_name',
         default=u'The name of the websocket server to be used.'
      ),
      required = True
   )

   host = TextLine(
      title=_('label_host', default=u'Host'),
      description=_(
         'help_host',
         default=u'The host name of the websocket server to be used.'
      ),
      required = True
   )

   port = Int(
      title=_('label_port', default=u'Port'),
      description=_(
         'help_port',
         default=u'The port of the websocket server to be used.'
      ),
      required = True
   )


class IWebSocketConnectionConfig(IWebSocketConnectionSchema):
   """Utility to hold the connection configuration for the connection"""


class IZCMLWebSocketConnectionConfig(Interface):
   """Connection settings configured through ZCML."""


class IWebSocketConnectionManager(Interface):
    """a thread-local connection manager for a websocket connection"""

    def setHost(name="", host='localhost', port=80):
        """ set connection parameters """

    def closeConnection():
        """ close the current connection, if any """

    def getConnection():
        """ returns an existing connection or opens one """


