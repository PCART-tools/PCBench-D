class NavigationToolbar2GTK3(_NavigationToolbar2GTK, Gtk.Toolbar):
    @_api.delete_parameter("3.6", "window")
    def __init__(self, canvas, window=None):
        self._win = window
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
            self._gtk_ids[text] = button = (
                Gtk.ToggleToolButton() if callback in ['zoom', 'pan'] else
                Gtk.ToolButton())
            button.set_label(text)
            button.set_icon_widget(image)
            # Save the handler id, so that we can block it as needed.
            button._signal_handler = button.connect(
                'clicked', getattr(self, callback))
            button.set_tooltip_text(tooltip_text)
            self.insert(button, -1)

        # This filler item ensures the toolbar is always at least two text
        # lines high. Otherwise the canvas gets redrawn as the mouse hovers
        # over images because those use two-line messages which resize the
        # toolbar.
        toolitem = Gtk.ToolItem()
        self.insert(toolitem, -1)
        label = Gtk.Label()
        label.set_markup(
            '<small>\N{NO-BREAK SPACE}\n\N{NO-BREAK SPACE}</small>')
        toolitem.set_expand(True)  # Push real message to the right.
        toolitem.add(label)

        toolitem = Gtk.ToolItem()
        self.insert(toolitem, -1)
        self.message = Gtk.Label()
        self.message.set_justify(Gtk.Justification.RIGHT)
        toolitem.add(self.message)

        self.show_all()

        _NavigationToolbar2GTK.__init__(self, canvas)

    win = _api.deprecated("3.6")(property(lambda self: self._win))

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
                ff.add_pattern(f'*.{fmt}')
            dialog.add_filter(ff)
            if self.canvas.get_default_filetype() in fmts:
                dialog.set_filter(ff)

        @functools.partial(dialog.connect, "notify::filter")
        def on_notify_filter(*args):
            name = dialog.get_filter().get_name()
            fmt = self.canvas.get_supported_filetypes_grouped()[name][0]
            dialog.set_current_name(
                str(Path(dialog.get_current_name()).with_suffix(f'.{fmt}')))

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
            dialog = Gtk.MessageDialog(
                parent=self.canvas.get_toplevel(), message_format=str(e),
                type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK)
            dialog.run()
            dialog.destroy()
