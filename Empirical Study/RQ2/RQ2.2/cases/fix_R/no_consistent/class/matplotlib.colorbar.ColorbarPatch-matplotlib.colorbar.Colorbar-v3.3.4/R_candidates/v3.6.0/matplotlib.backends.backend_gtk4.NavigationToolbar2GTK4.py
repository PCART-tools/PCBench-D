class NavigationToolbar2GTK4(_NavigationToolbar2GTK, Gtk.Box):
    @_api.delete_parameter("3.6", "window")
    def __init__(self, canvas, window=None):
        self._win = window
        Gtk.Box.__init__(self)

        self.add_css_class('toolbar')

        self._gtk_ids = {}
        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.append(Gtk.Separator())
                continue
            image = Gtk.Image.new_from_gicon(
                Gio.Icon.new_for_string(
                    str(cbook._get_data_path('images',
                                             f'{image_file}-symbolic.svg'))))
            self._gtk_ids[text] = button = (
                Gtk.ToggleButton() if callback in ['zoom', 'pan'] else
                Gtk.Button())
            button.set_child(image)
            button.add_css_class('flat')
            button.add_css_class('image-button')
            # Save the handler id, so that we can block it as needed.
            button._signal_handler = button.connect(
                'clicked', getattr(self, callback))
            button.set_tooltip_text(tooltip_text)
            self.append(button)

        # This filler item ensures the toolbar is always at least two text
        # lines high. Otherwise the canvas gets redrawn as the mouse hovers
        # over images because those use two-line messages which resize the
        # toolbar.
        label = Gtk.Label()
        label.set_markup(
            '<small>\N{NO-BREAK SPACE}\n\N{NO-BREAK SPACE}</small>')
        label.set_hexpand(True)  # Push real message to the right.
        self.append(label)

        self.message = Gtk.Label()
        self.message.set_justify(Gtk.Justification.RIGHT)
        self.append(self.message)

        _NavigationToolbar2GTK.__init__(self, canvas)

    win = _api.deprecated("3.6")(property(lambda self: self._win))

    def save_figure(self, *args):
        dialog = Gtk.FileChooserNative(
            title='Save the figure',
            transient_for=self.canvas.get_root(),
            action=Gtk.FileChooserAction.SAVE,
            modal=True)
        self._save_dialog = dialog  # Must keep a reference.

        ff = Gtk.FileFilter()
        ff.set_name('All files')
        ff.add_pattern('*')
        dialog.add_filter(ff)
        dialog.set_filter(ff)

        formats = []
        default_format = None
        for i, (name, fmts) in enumerate(
                self.canvas.get_supported_filetypes_grouped().items()):
            ff = Gtk.FileFilter()
            ff.set_name(name)
            for fmt in fmts:
                ff.add_pattern(f'*.{fmt}')
            dialog.add_filter(ff)
            formats.append(name)
            if self.canvas.get_default_filetype() in fmts:
                default_format = i
        # Setting the choice doesn't always work, so make sure the default
        # format is first.
        formats = [formats[default_format], *formats[:default_format],
                   *formats[default_format+1:]]
        dialog.add_choice('format', 'File format', formats, formats)
        dialog.set_choice('format', formats[default_format])

        dialog.set_current_folder(Gio.File.new_for_path(
            os.path.expanduser(mpl.rcParams['savefig.directory'])))
        dialog.set_current_name(self.canvas.get_default_filename())

        @functools.partial(dialog.connect, 'response')
        def on_response(dialog, response):
            file = dialog.get_file()
            fmt = dialog.get_choice('format')
            fmt = self.canvas.get_supported_filetypes_grouped()[fmt][0]
            dialog.destroy()
            self._save_dialog = None
            if response != Gtk.ResponseType.ACCEPT:
                return
            # Save dir for next time, unless empty str (which means use cwd).
            if mpl.rcParams['savefig.directory']:
                parent = file.get_parent()
                mpl.rcParams['savefig.directory'] = parent.get_path()
            try:
                self.canvas.figure.savefig(file.get_path(), format=fmt)
            except Exception as e:
                msg = Gtk.MessageDialog(
                    transient_for=self.canvas.get_root(),
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK, modal=True,
                    text=str(e))
                msg.show()

        dialog.show()
