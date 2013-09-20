from gi.repository import Gedit
from gi.repository import Gio
from gi.repository import GObject
import os

class LinkFileBrowserWithCurrentTab(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "LinkFileBrowserWithCurrentTab"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        self.handlers = []

    def do_activate(self):
        self.handlers = [
          self.window.connect("tab-added", self.on_tab_action),
          self.window.connect("tab-removed", self.on_tab_action),
          self.window.connect("active-tab-changed", self.on_tab_action),
        ]

    def do_deactivate(self):
        map(self.window.disconnect, self.handlers)

    def do_update_state(self):
        pass

    def on_tab_action(self, _window, _tab, _data=None):
        self.update_filebrowser_root()

    def update_filebrowser_root(self):
        current_document = self.window.get_active_document()
        if not current_document:
            return
        current_directory = os.path.dirname(current_document.get_uri_for_display())
        if not current_directory:
            return
        bus = self.window.get_message_bus()
        if not bus.is_registered('/plugins/filebrowser', 'set_root'):
            return
        gfile = Gio.file_new_for_uri('file://' + current_directory)
        # see gedit-file-browser-messages.c in gedit repository
        bus.send_sync('/plugins/filebrowser', 'set_root', location=gfile)

