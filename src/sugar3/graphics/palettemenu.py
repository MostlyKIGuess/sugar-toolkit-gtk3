# Copyright 2012 One Laptop Per Child
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''
The palettemenu module is the main port of call for making palettes.  It
covers creating menu items, separators and placing them in a box.

Example:

    Create a palette menu with 2 items with a separator in the middle.

    .. code-block:: python

        from gi.repository import Gtk
        from gettext import gettext as _

        from sugar3.graphics.palette import Palette
        from sugar3.graphics.palettemenu import PaletteMenuBox
        from sugar3.graphics.palettemenu import PaletteMenuItem
        from sugar3.graphics.palettemenu import PaletteMenuItemSeparator


        class ItemPalette(Palette):
            def __init__(self):
                Palette.__init__(
                    self, primary_text='List Item')
                box = PaletteMenuBox()
                self.set_content(box)
                box.set_visible(True)

                menu_item = PaletteMenuItem(
                    _('Edit'), icon_name='toolbar-edit')
                menu_item.connect('activate', self.__edit_cb)
                box.append_item(menu_item)
                menu_item.set_visible(True)

                sep = PaletteMenuItemSeparator()
                box.append_item(sep)
                sep.set_visible(True)

                menu_item = PaletteMenuItem(
                    _('Delete'), icon_name='edit-delete')
                box.append_item(menu_item)
                menu_item.set_visible(True)

            def __edit_cb(self, menu_item):
                print('Edit...')

        # Usually the Palette instance is returned in a create_palette function
        p = ItemPalette()
        p.popup()
        Gtk.main()

    Add a palettebox to a toolbutton:

    .. code-block:: python

        image = ToolButton('insert-picture')
        image.set_tooltip(_('Insert Image'))
        self._image_id = image.connect('clicked', self.__image_cb)
        toolbar_box.toolbar.insert(image, -1)

        palette = image.get_palette()
        box = PaletteMenuBox()
        palette.set_content(box)
        box.set_visible(True)

        menu_item = PaletteMenuItem(_('Floating'))
        menu_item.connect('activate', self.__image_cb, True)
        box.append_item(menu_item)
        menu_item.set_visible(True)
'''

from gi.repository import GObject
from gi.repository import Gtk

from sugar3.graphics.icon import Icon
from sugar3.graphics import style

class PaletteMenuBox(Gtk.Box):
    '''
    The PaletteMenuBox is a box that is useful for making palettes.  It
    supports adding :class:`sugar3.graphics.palettemenu.PaletteMenuItem`,
    :class:`sugar3.graphics.palettemenu.PaletteMenuItemSeparator` and
    it automatically adds padding to other widgets.
    '''

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

    def append_item(self, item_or_widget, horizontal_padding=None,
                    vertical_padding=None):
        '''
        Add a menu item, separator or other widget to the end of the palette
        (similar to `Gtk.Box.pack_start`).

        If an item is appended
        (a :class:`sugar3.graphics.palettemenu.PaletteMenuItem` or a
        :class:`sugar3.graphics.palettemenu.PaletteMenuItemSeparator`) no
        padding will be added, as that is handled by the item.  If a widget is
        appended (:class:`Gtk.Widget` subclass) padding will be added.

        Args:
            item_or_widget (:class:`Gtk.Widget` or menu item or separator):
                item or widget to add the palette
            horizontal_padding (int):  by default,
                :class:`sugar3.graphics.style.DEFAULT_SPACING` is applied
            vertical_padding (int):  by default,
                :class:`sugar3.graphics.style.DEFAULT_SPACING` is applied

        Returns:
            None
        '''
        if (isinstance(item_or_widget, PaletteMenuItem) or
                isinstance(item_or_widget, PaletteMenuItemSeparator)):
            self.append(item_or_widget)
        else:
            item = self._wrap_widget(item_or_widget, horizontal_padding,
                                     vertical_padding)
            self.append(item)

    def _wrap_widget(self, widget, horizontal_padding, vertical_padding):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.set_visible(True)

        if horizontal_padding is None:
            horizontal_padding = style.DEFAULT_SPACING
        if vertical_padding is None:
            vertical_padding = style.DEFAULT_SPACING

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_visible(True)
        
        widget.set_margin_start(horizontal_padding)
        widget.set_margin_end(horizontal_padding)
        hbox.set_margin_top(vertical_padding)
        hbox.set_margin_bottom(vertical_padding)
        
        hbox.append(widget)
        vbox.append(hbox)
        
        return vbox


class PaletteMenuItemSeparator(Gtk.Separator):
    '''
    Horizontal separator to put in a palette
    '''

    __gtype_name__ = 'SugarPaletteMenuItemSeparator'

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_margin_top(style.DEFAULT_SPACING)
        self.set_margin_bottom(style.DEFAULT_SPACING)
        self.set_visible(True)


class PaletteMenuItem(Gtk.Box):
    '''
    A palette menu item is a line of text, and optionally an icon, that the
    user can activate.

    The `activate` signal is usually emitted when the item is clicked.  It has
    no arguments.  When a menu item is activated, the palette is also closed.

    Args:
        text_label (str):  a text to display in the menu

        icon_name (str):  the name of a sugar icon to be displayed. Takes
            precedence over file_name

        text_maxlen (int):  the desired maximum width of the label, in
            characters.  By default set to 60 chars

        xo_color (:class:`sugar.graphics.XoColor`):  the color to be applied to
            the icon

        file_name (str):  the path to a svg file used as icon

        accelerator (str):  a text used to display the keyboard shortcut
            associated to the menu
    '''

    __gtype_name__ = 'SugarPaletteMenuItem'

    __gsignals__ = {
        'activate': (GObject.SignalFlags.RUN_FIRST, None, [])
    }

    def __init__(self, text_label=None, icon_name=None, text_maxlen=60,
                 xo_color=None, file_name=None, accelerator=None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_above_child(True)

        self.icon = None
        self._hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append(vbox)
        vbox.set_visible(True)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.append(hbox)
        hbox.set_margin_top(style.DEFAULT_PADDING)
        hbox.set_margin_bottom(style.DEFAULT_PADDING)
        hbox.set_visible(True)

        hbox.append(self._hbox)

        if icon_name is not None:
            self.icon = Icon(icon_name=icon_name,
                             pixel_size=style.SMALL_ICON_SIZE)
            if xo_color is not None:
                self.icon.props.xo_color = xo_color
            self._hbox.append(self.icon)
        elif file_name is not None:
            self.icon = Icon(file=file_name,
                             pixel_size=style.SMALL_ICON_SIZE)
            if xo_color is not None:
                self.icon.props.xo_color = xo_color
            self._hbox.append(self.icon)

        self.label = Gtk.Label(label=text_label)
        if text_maxlen > 0:
            self.label.set_max_width_chars(text_maxlen)
            self.label.set_ellipsize(style.ELLIPSIZE_MODE_DEFAULT)
        self._hbox.append(self.label)

        self._accelerator_label = Gtk.Label(label='')
        if accelerator is not None:
            self._accelerator_label.set_text(accelerator)
        self._hbox.append(self._accelerator_label)

        self.id_bt_release_cb = self.connect('button-release-event',
                                             self.__button_release_cb)
        self.id_enter_notify_cb = self.connect('enter-notify-event',
                                               self.__enter_notify_cb)
        self.id_leave_notify_cb = self.connect('leave-notify-event',
                                               self.__leave_notify_cb)

        self.set_visible(True)

    def __button_release_cb(self, widget, event):
        alloc = self.get_allocation()
        if 0 < event.x < alloc.width and 0 < event.y < alloc.height:
            self.emit('activate')

    def __enter_notify_cb(self, widget, event):
        self.set_state_flags(Gtk.StateFlags.PRELIGHT, clear=False)

    def __leave_notify_cb(self, widget, event):
        self.unset_state_flags(Gtk.StateFlags.PRELIGHT)

    def set_label(self, text_label):
        '''
        Sets the text to display in the menu.

        Args:
            text_label (str):  text label
        '''
        text = '<span foreground="%s">' % style.COLOR_WHITE.get_html() + \
            text_label + '</span>'
        self.label.set_markup(text)

    def set_image(self, icon):
        '''
        Sets the icon widget.  Usually this will be a
        :class:`sugar3.graphics.icon.Icon`.

        Args:
            icon (:class:`Gtk.Widget`):  icon widget
        '''
        self._hbox.append(icon)
        self._hbox.reorder_child(icon, 0)

    def set_accelerator(self, text):
        '''
        Sets the text used to display the keyboard shortcut associated with
        the menu.

        Args:
            text (str): accelerator text
        '''
        self._accelerator_label.set_text(text)

    def set_sensitive(self, sensitive):
        '''
        Sets whether the widget should be activatable by the user and changes
        the widget's appearance to the appropriate state.

        Args:
            sensitive (bool):  if `True`, the widget will be activatable by
                the user. Otherwise, it will not be activatable
        '''
        is_sensitive = bool(not self.get_state_flags() &
                            Gtk.StateFlags.INSENSITIVE)
        if is_sensitive == sensitive:
            return

        if sensitive:
            self.handler_unblock(self.id_bt_release_cb)
            self.handler_unblock(self.id_enter_notify_cb)
            self.handler_unblock(self.id_leave_notify_cb)
            self.unset_state_flags(Gtk.StateFlags.INSENSITIVE)
        else:
            self.handler_block(self.id_bt_release_cb)
            self.handler_block(self.id_enter_notify_cb)
            self.handler_block(self.id_leave_notify_cb)
            self.set_state_flags(Gtk.StateFlags.INSENSITIVE)            
