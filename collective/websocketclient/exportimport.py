# -*- coding: utf-8 -*-
from persistent.interfaces import IPersistent
from zope.component import queryUtility
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import XMLAdapterBase

from collective.websocketclient.interfaces import IWebSocketConnectionConfig


class WebSocketClientConfigXMLAdapter(XMLAdapterBase):

    _LOGGER_ID = 'collective.websocketclient'

    def _exportNode(self):
        """ export the object as a DOM node """
        node = self._extractProperties()
        self._logger.info('settings exported.')
        return node

    def _importNode(self, node):
        """ import the object from the DOM node """
        if self.environ.shouldPurge():
            self._purgeProperties()
        self._initProperties(node)
        self._logger.info('settings imported.')

    def _purgeProperties(self):
        self.context.name = ''
        self.context.host = ''
        self.context.port = 0


    def _initProperties(self, node):
        elems = node.getElementsByTagName('connection')
        if elems:
            assert len(elems) == 1
            conn = elems[0]
            for child in conn.childNodes:
                if child.nodeName == 'port':
                    value = int(str(child.getAttribute('value')))
                    self.context.port = value
                elif child.nodeName == 'host':
                    self.context.host = str(child.getAttribute('value'))
                elif child.nodeName == 'name':
                    self.context.name = str(child.getAttribute('value'))


    def _createNode(self, name, value):
        node = self._doc.createElement(name)
        node.setAttribute('value', value)
        return node

    def _extractProperties(self):
        node = self._doc.createElement('object')
        node.setAttribute('name', 'websocketclient')
        conn = self._doc.createElement('connection')
        create = self._createNode
        node.appendChild(conn)
        conn.appendChild(create('name', self.context.name))
        conn.appendChild(create('host', self.context.host))
        conn.appendChild(create('port', str(self.context.port)))
        return node


def importWebSocketClientSettings(context):
    """ import settings for websocket client integration from an XML file """
    site = context.getSite()
    utility = queryUtility(IWebSocketConnectionConfig, context=site)
    if utility is None:
        logger = context.getLogger('collective.websocketclient')
        logger.info('Nothing to import.')
        return
    if IPersistent.providedBy(utility):
        importObjects(utility, '', context)


def exportWebSocketClientSettings(context):
    """ export settings for websocket client integration as an XML file """
    site = context.getSite()
    utility = queryUtility(IWebSocketConnectionConfig, context=site)
    if utility is None:
        logger = context.getLogger('collective.websocketclient')
        logger.info('Nothing to export.')
        return
    if IPersistent.providedBy(utility):
        exportObjects(utility, '', context)
