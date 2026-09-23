class FileChooserDialog(Gtk.FileChooserDialog):
    """GTK+ file selector which remembers the last file/directory
    selected and presents the user with a menu of supported image formats
    """
    def __init__(self,
                 title   = 'Save file',
                 parent  = None,
                 action  = Gtk.FileChooserAction.SAVE,
                 buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                            Gtk.STOCK_SAVE,   Gtk.ResponseType.OK),
                 path    = None,
                 filetypes = [],
                 default_filetype = None
                ):
        super().__init__(title, parent, action, buttons)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_do_overwrite_confirmation(True)

        if not path:
            path = os.getcwd()

        # create an extra widget to list supported image formats
        self.set_current_folder(path)
        self.set_current_name('image.' + default_filetype)

        hbox = Gtk.Box(spacing=10)
        hbox.pack_start(Gtk.Label(label="File Format:"), False, False, 0)

        liststore = Gtk.ListStore(GObject.TYPE_STRING)
        cbox = Gtk.ComboBox()
        cbox.set_model(liststore)
        cell = Gtk.CellRendererText()
        cbox.pack_start(cell, True)
        cbox.add_attribute(cell, 'text', 0)
        hbox.pack_start(cbox, False, False, 0)

        self.filetypes = filetypes
        sorted_filetypes = sorted(filetypes.items())
        default = 0
        for i, (ext, name) in enumerate(sorted_filetypes):
            liststore.append(["%s (*.%s)" % (name, ext)])
            if ext == default_filetype:
                default = i
        cbox.set_active(default)
        self.ext = default_filetype

        def cb_cbox_changed(cbox, data=None):
            """File extension changed"""
            head, filename = os.path.split(self.get_filename())
            root, ext = os.path.splitext(filename)
            ext = ext[1:]
            new_ext = sorted_filetypes[cbox.get_active()][0]
            self.ext = new_ext

            if ext in self.filetypes:
                filename = root + '.' + new_ext
            elif ext == '':
                filename = filename.rstrip('.') + '.' + new_ext

            self.set_current_name(filename)
        cbox.connect("changed", cb_cbox_changed)

        hbox.show_all()
        self.set_extra_widget(hbox)

    @cbook.deprecated("3.0", alternative="sorted(self.filetypes.items())")
    def sorted_filetypes(self):
        return sorted(self.filetypes.items())

    def get_filename_from_user(self):
        if self.run() == int(Gtk.ResponseType.OK):
            return self.get_filename(), self.ext
        else:
            return None, self.ext
