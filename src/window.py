# window.py
#
# Copyright 2023 Axel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from .session import Session

@Gtk.Template(resource_path='/org/demo/OdooMigration/window.ui')
class OdoomigrationtoolWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'OdoomigrationtoolWindow'

    models_stack = Gtk.Template.Child()
    models_list = Gtk.Template.Child()
    fields_list = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.models_list.connect('row-selected', self.on_model_selected)

    @Gtk.Template.Callback()
    def new_session(self, widget):
        dialog = NewSessionDialog(parent=self)
        dialog.connect('response', self.on_new_sesion_reponse)
        dialog.show()

    def on_new_sesion_reponse(self, dialog, response):
        if response == 'connect':
            self.models_stack.set_visible_child_name('models')
            url = dialog.url_entry.get_text()
            print(url)
            db_name = dialog.db_entry.get_text()
            username = dialog.username_entry.get_text()
            password = dialog.password_entry.get_text()
            
            #TODO: Validate fields
            self.session = Session(username, password, url, db_name)
            self.session.authenticate()

            models = self.session.get_db_models()
            
            for model in models:
                row = Adw.ActionRow()
                row.set_icon_name('image')
                row.set_title(model['name'])
                row.set_subtitle(model['model'])
                self.models_list.append(row)

    def on_model_selected(self, box, row):
        model = row.get_subtitle()
        fields = self.session.get_model_fields(model)

        child = self.field_list.get_first_child()

        while child is not None:
            self.fields_list.remove(child)

        for field in fields:
                row = Adw.EntryRow()
                row.set_title(field['label'])
                row.set_text(field['name'])
                self.fields_list.append(row)


@Gtk.Template(resource_path='/org/demo/OdooMigration/new-session-dialog.ui')
class NewSessionDialog(Adw.MessageDialog):
    __gtype_name__ = 'NewSessionDialog'

    url_entry = Gtk.Template.Child()
    db_entry = Gtk.Template.Child()
    username_entry = Gtk.Template.Child()
    password_entry = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_response('cancel', 'Cancel')
        self.add_response('connect', 'Connect')
        self.set_response_appearance('connect', Adw.ResponseAppearance.SUGGESTED)