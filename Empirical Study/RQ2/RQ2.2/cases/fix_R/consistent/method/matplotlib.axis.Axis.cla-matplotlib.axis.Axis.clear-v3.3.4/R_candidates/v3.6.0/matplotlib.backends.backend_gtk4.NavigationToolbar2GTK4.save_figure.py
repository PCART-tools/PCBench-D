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
