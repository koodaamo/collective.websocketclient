# -*- extra stuff goes here -*-

from zope.i18n import MessageFactory
from websocket._exceptions import WebSocketException, \
                                  WebSocketTimeoutException, \
                                  WebSocketConnectionClosedException

_ = MessageFactory("collective.websocketclient")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


class WebSocketConfigException(WebSocketException):
   "raised when there is a problem with configuring the connection"
