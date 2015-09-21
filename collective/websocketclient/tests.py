import os, unittest, multiprocessing

from zope.component import getUtility
from zope.component import getGlobalSiteManager
from zope.component import getUtilitiesFor
from zope.component import queryUtility
from zope.configuration import xmlconfig

from plone.testing import z2, Layer
from plone.app.testing import PloneSandboxLayer, PloneWithPackageLayer
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles, applyProfile, quickInstallProduct
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import login

from plone import api

import collective.websocketclient
from collective.websocketclient.interfaces import IWebSocketConnectionConfig
from collective.websocketclient.interfaces import IZCMLWebSocketConnectionConfig
from collective.websocketclient.interfaces import IWebSocketConnectionManager

from websocket_server import WebsocketServer


def start_wss(port):
   "start the websocket test server"

   def reply_back(client, server, msg):
       server.send_message(client, "You sent: %s" % msg)

   server = WebsocketServer(port)
   server.set_fn_message_received(reply_back)
   server.run_forever()

#
# Layer definitions
#

class WebSocketServerFixture(Layer):

   def setUp(self):
      self._wss_process = multiprocessing.Process(target=start_wss, args=(9000,))
      self._wss_process.start()

   def tearDown(self):
      self._wss_process.terminate()
      self._wss_process.join()


class PkgFixture(PloneSandboxLayer):

   def setUpZope(self, app, configurationContext):
      self.loadZCML("meta.zcml", package=collective.websocketclient)
      self.loadZCML("configure.zcml", package=collective.websocketclient)

   def tearDownZope(self, app):
      gsm = getGlobalSiteManager()
      zcmlconfig = queryUtility(IZCMLWebSocketConnectionConfig)
      gsm.unregisterUtility(zcmlconfig, IZCMLWebSocketConnectionConfig)


class ConnectionSetupFixture(PkgFixture):

   def setUpPloneSite(self, portal):
      applyProfile(portal, "collective.websocketclient:testing")
      manager = queryUtility(IWebSocketConnectionManager)
      self["websocket_connection"] = manager.getConnection()


class LoggedInProfileFixture(PkgFixture):

   def setUpPloneSite(self, portal):
      applyProfile(portal, "collective.websocketclient")
      setRoles(portal, TEST_USER_ID, ['Member', 'Manager'])
      login(portal, TEST_USER_NAME)


#
# Fixture instances
#

WEBSOCKETSERVERFIXTURE = WebSocketServerFixture()
PKGFIXTURE = PkgFixture()
PROFILEFIXTURE = PloneWithPackageLayer(
   zcml_package=collective.websocketclient,
   zcml_filename='configure.zcml',
   gs_profile_id='collective.websocketclient:testing',
   name="Fixture: WebSockeClientPloneInstalled"
)
CONNECTIONSETUPFIXTURE = ConnectionSetupFixture()

#
# Layer instances
#

PKGTESTING = IntegrationTesting(bases=(PKGFIXTURE,), name="Fixture:WebSocketClientZopeInstalled")
PROFILETESTING = IntegrationTesting(bases=(PROFILEFIXTURE,), name="Fixture:WebSocketClientPloneInstalled")
CONNECTIONTESTING = IntegrationTesting(bases=(WEBSOCKETSERVERFIXTURE, CONNECTIONSETUPFIXTURE), name="Fixture:Connection")

#
# TESTS
#

class TestWebSocketConfigImport(unittest.TestCase):

   layer = PKGTESTING

   def test_gs_import_settings_fails(self):
      cfg = queryUtility(IWebSocketConnectionConfig)
      self.assertEqual(cfg, None)

   def test_gs_import_settings_works(self):
      applyProfile(api.portal.get(), "collective.websocketclient:testing")
      cfg = queryUtility(IWebSocketConnectionConfig)
      self.assertEqual((cfg.name, cfg.host, cfg.port), ("test", "127.0.0.1", 9000))

   def test_zcml_import_settings_works(self):
      context = xmlconfig.file('meta.zcml', collective.websocketclient)
      xmlconfig.string('''
         <configure xmlns:websocketclient="http://namespaces.plone.org/websocketclient">
             <websocketclient:connection name="test" host="127.0.0.1" port="9000"/>
         </configure>
      ''', context=context)
      cfg = queryUtility(IZCMLWebSocketConnectionConfig)
      self.assertEqual((cfg.name, cfg.host, cfg.port), ('test', '127.0.0.1',9000))


class TestWebSocketConnectionConfiguration(unittest.TestCase):

   layer = PROFILETESTING

   def test_profileconfigured_connection_creation(self):
      manager = queryUtility(IWebSocketConnectionManager)
      wsc_connection = manager.getConnection()
      self.assertEqual((wsc_connection.host, wsc_connection.port), ('127.0.0.1',9000))

   def test_ZCMLconfigured_connection_creation(self):
      context = xmlconfig.file('meta.zcml', collective.websocketclient)
      xmlconfig.string('''
         <configure xmlns:websocketclient="http://namespaces.plone.org/websocketclient">
             <websocketclient:connection name="test" host="127.0.0.1" port="9000"/>
         </configure>
      ''', context=context)
      manager = queryUtility(IWebSocketConnectionManager)
      wsc_connection = manager.getConnection()
      self.assertEqual((wsc_connection.host, wsc_connection.port), ('127.0.0.1',9000))


class TestWebSocketConnection(unittest.TestCase):

   layer = CONNECTIONTESTING

   def setUp(self):
      self.connection = self.layer["websocket_connection"]
      self.connection.connect()

   def tearDown(self):
      self.connection.close()

   def test_01_sending(self):
      self.connection.send("Hello World!")

   def test_02_sending_and_receiving(self):
      self.connection.send("Hello World!")
      self.assertEqual("You sent: Hello World!", self.connection.receive())
