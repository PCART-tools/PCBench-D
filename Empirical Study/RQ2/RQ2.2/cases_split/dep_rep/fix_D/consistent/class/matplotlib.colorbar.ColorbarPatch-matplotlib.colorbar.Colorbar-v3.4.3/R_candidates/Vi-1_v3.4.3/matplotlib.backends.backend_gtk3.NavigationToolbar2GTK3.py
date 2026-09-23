class NavigationToolbar2GTK3(NavigationToolbar2, Gtk.Toolbar):
    ctx = _api.deprecated("3.3")(property(
        lambda self: self.canvas.get_property("window").cairo_create()))

    def __init__(self, canvas, window):
        self.win = window
        GObject.GObject.__init__(self)

        self.set_style(Gtk.ToolbarStyle.ICONS)

        self._gtk_ids = {}
        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.insert(Gtk.SeparatorToolItem(), -1)
                continue
            image = Gtk.Image.new_from_gicon(
                Gio.Icon.new_for_string(
                    str(cbook._get_data_path('images',
                                             f'{image_file}-symbolic.svg'))),
                Gtk.IconSize.LARGE_TOOLBAR)
            self._gtk_ids[text] = tbutton = (
                Gtk.ToggleToolButton() if callback in ['zoom', 'pan'] else
                Gtk.ToolButton())
            tbutton.set_label(text)
            tbutton.set_icon_widget(image)
            self.insert(tbutton, -1)
            # Save the handler id, so that we can block it as needed.
            tbutton._signal_handler = tbutton.connect(
                'clicked', getattr(self, callback))
            tbutton.set_tooltip_text(tooltip_text)

        toolitem = Gtk.SeparatorToolItem()
        self.insert(toolitem, -1)
        toolitem.set_draw(False)
        toolitem.set_expand(True)

        # This filler item ensures the toolbar is always at least two text
        # lines high. Otherwise the canvas gets redrawn as the mouse hovers
        # over images because those use two-line messages which resize the
        # toolbar.
        toolitem = Gtk.ToolItem()
        self.insert(toolitem, -1)
        label = Gtk.Label()
        label.set_markup(
            '<small>\N{NO-BREAK SPACE}\n\N{NO-BREAK SPACE}</small>')
        toolitem.add(label)

        toolitem = Gtk.ToolItem()
        self.insert(toolitem, -1)
        self.message = Gtk.Label()
        toolitem.add(self.message)

        self.show_all()

        NavigationToolbar2.__init__(self, canvas)

    def set_message(self, s):
        escaped = GLib.markup_escape_text(s)
        self.message.set_markup(f'<small>{escaped}</small>')

    def set_cursor(self, cursor):
        window = self.canvas.get_property("window")
        if window is not None:
            window.set_cursor(cursord[cursor])
            Gtk.main_iteration()

    def draw_rubberband(self, event, x0, y0, x1, y1):
        height = self.canvas.figure.bbox.height
        y1 = height - y1
        y0 = height - y0
        rect = [int(val) for val in (x0, y0, x1 - x0, y1 - y0)]
        self.canvas._draw_rubberband(rect)

    def remove_rubberband(self):
        self.canvas._draw_rubberband(None)

    def _update_buttons_checked(self):
        for name, active in [("Pan", "PAN"), ("Zoom", "ZOOM")]:
            button = self._gtk_ids.get(name)
            if button:
                with button.handler_block(button._signal_handler):
                    button.set_active(self.mode.name == active)

    def pan(self, *args):
        super().pan(*args)
        self._update_buttons_checked()

    def zoom(self, *args):
        super().zoom(*args)
        self._update_buttons_checked()

    def save_figure(self, *args):
        dialog = Gtk.FileChooserDialog(
            title="Save the figure",
            parent=self.canvas.get_toplevel(),
            action=Gtk.FileChooserAction.SAVE,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                     Gtk.STOCK_SAVE,   Gtk.ResponseType.OK),
        )
        for name, fmts \
                in self.canvas.get_supported_filetypes_grouped().items():
            ff = Gtk.FileFilter()
            ff.set_name(name)
            for fmt in fmts:
                ff.add_pattern("*." + fmt)
            dialog.add_filter(ff)
            if self.canvas.get_default_filetype() in fmts:
                dialog.set_filter(ff)

        @functools.partial(dialog.connect, "notify::filter")
        def on_notify_filter(*args):
            name = dialog.get_filter().get_name()
            fmt = self.canvas.get_supported_filetypes_grouped()[name][0]
            dialog.set_current_name(
                str(Path(dialog.get_current_name()).with_suffix("." + fmt)))

        dialog.set_current_folder(mpl.rcParams["savefig.directory"])
        dialog.set_current_name(self.canvas.get_default_filename())
        dialog.set_do_overwrite_confirmation(True)

        response = dialog.run()
        fname = dialog.get_filename()
        ff = dialog.get_filter()  # Doesn't autoadjust to filename :/
        fmt = self.canvas.get_supported_filetypes_grouped()[ff.get_name()][0]
        dialog.destroy()
        if response != Gtk.ResponseType.OK:
            return
        # Save dir for next time, unless empty str (which means use cwd).
        if mpl.rcParams['savefig.directory']:
            mpl.rcParams['savefig.directory'] = os.path.dirname(fname)
        try:
            self.canvas.figure.savefig(fname, format=fmt)
        except Exception as e:
            error_msg_gtk(str(e), parent=self)

    def set_history_buttons(self):
        can_backward = self._nav_stack._pos > 0
        can_forward = self._nav_stack._pos < len(self._nav_stack._elements) - 1
        if 'Back' in self._gtk_ids:
            self._gtk_ids['Back'].set_sensitive(can_backward)
        if 'Forward' in self._gtk_ids:
            self._gtk_ids['Forward'].set_sensitive(can_forward)
