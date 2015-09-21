# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from zope.component.zcml import utility

from collective.websocketclient.interfaces import IZCMLWebSocketConnectionConfig
from collective.websocketclient.manager import ZCMLWebSocketConnectionConfig


class IWebSocketConfigDirective(Interface):
    """Directive which registers a websocket connection config"""

    name = schema.ASCIILine(
        title=u"Name",
        description=u"The name of the websocket connection to be used.",
        required=True,
    )

    host = schema.ASCIILine(
        title=u"Host",
        description=u"The host name of the websocket server to be used.",
        required=True,
    )

    port = schema.Int(
        title=u"Port",
        description=u"The port of the websocket server to be used.",
        required=True,
    )


def websocketConnectionConfigDirective(_context, name, host, port):
   "register the config utility"
   utility(_context,
           provides=IZCMLWebSocketConnectionConfig,
           component=ZCMLWebSocketConnectionConfig(name, host, port))
