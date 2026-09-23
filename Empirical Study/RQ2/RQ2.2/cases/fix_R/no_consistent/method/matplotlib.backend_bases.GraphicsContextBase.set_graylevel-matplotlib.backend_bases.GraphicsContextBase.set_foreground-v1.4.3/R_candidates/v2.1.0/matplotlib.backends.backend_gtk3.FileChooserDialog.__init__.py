    def __init__ (self,
                  title   = 'Save file',
                  parent  = None,
                  action  = Gtk.FileChooserAction.SAVE,
                  buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_SAVE,   Gtk.ResponseType.OK),
                  path    = None,
                  filetypes = [],
                  default_filetype = None
                  ):
        super (FileChooserDialog, self).__init__ (title, parent, action,
                                                  buttons)
        self.set_default_response (Gtk.ResponseType.OK)

        if not path: path = os.getcwd() + os.sep

        # create an extra widget to list supported image formats
        self.set_current_folder (path)
        self.set_current_name ('image.' + default_filetype)

        hbox = Gtk.Box(spacing=10)
        hbox.pack_start(Gtk.Label(label="File Format:"), False, False, 0)

        liststore = Gtk.ListStore(GObject.TYPE_STRING)
        cbox = Gtk.ComboBox() #liststore)
        cbox.set_model(liststore)
        cell = Gtk.CellRendererText()
        cbox.pack_start(cell, True)
        cbox.add_attribute(cell, 'text', 0)
        hbox.pack_start(cbox, False, False, 0)

        self.filetypes = filetypes
        self.sorted_filetypes = sorted(six.iteritems(filetypes))
        default = 0
        for i, (ext, name) in enumerate(self.sorted_filetypes):
            liststore.append(["%s (*.%s)" % (name, ext)])
            if ext == default_filetype:
                default = i
        cbox.set_active(default)
        self.ext = default_filetype

        def cb_cbox_changed (cbox, data=None):
            """File extension changed"""
            head, filename = os.path.split(self.get_filename())
            root, ext = os.path.splitext(filename)
            ext = ext[1:]
            new_ext = self.sorted_filetypes[cbox.get_active()][0]
            self.ext = new_ext

            if ext in self.filetypes:
                filename = root + '.' + new_ext
            elif ext == '':
                filename = filename.rstrip('.') + '.' + new_ext

            self.set_current_name (filename)
        cbox.connect ("changed", cb_cbox_changed)

        hbox.show_all()
        self.set_extra_widget(hbox)
