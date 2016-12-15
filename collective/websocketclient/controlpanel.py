#from z3c.form import form
#from plone.z3cform import layout
from plone.app.registry.browser import controlpanel

from .interfaces import IWebSocketConnectionSchema


class WebsocketConnectionForm(controlpanel.RegistryEditForm):

    schema = IWebSocketConnectionSchema


class WebsocketConnectionControlPanel(controlpanel.ControlPanelFormWrapper):

    form = WebsocketConnectionForm
