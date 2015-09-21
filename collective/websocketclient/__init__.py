# -*- extra stuff goes here -*-

from zope.i18n import MessageFactory

_ = MessageFactory("collective.websocketclient")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
