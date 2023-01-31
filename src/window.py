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

@Gtk.Template(resource_path='/org/demo/OdooMigration/window.ui')
class OdoomigrationtoolWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'OdoomigrationtoolWindow'

    label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@Gtk.Template(resource_path='/org/demo/OdooMigration/new_session_dialog.ui')
class NewSessionDialog(Adw.MessageDialog):
    __gtype_name__ = 'NewSessionDialog'


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_response('cancel', 'Cancel')
        self.add_response('connect', 'Connect')