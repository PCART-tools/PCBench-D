    def __init__ (self,
                  title   = 'Save file',
                  parent  = None,
                  action  = gtk.FILE_CHOOSER_ACTION_SAVE,
                  buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                             gtk.STOCK_SAVE,   gtk.RESPONSE_OK),
                  path    = None,
                  filetypes = [],
                  default_filetype = None
                  ):
        super(FileChooserDialog, self).__init__(title, parent, action, buttons)
        super(FileChooserDialog, self).set_do_overwrite_confirmation(True)
        self.set_default_response(gtk.RESPONSE_OK)

        if not path:
            path = os.getcwd() + os.sep

        # create an extra widget to list supported image formats
        self.set_current_folder (path)
        self.set_current_name ('image.' + default_filetype)

        hbox = gtk.HBox(spacing=10)
        hbox.pack_start(gtk.Label ("File Format:"), expand=False)

        liststore = gtk.ListStore(gobject.TYPE_STRING)
        cbox = gtk.ComboBox(liststore)
        cell = gtk.CellRendererText()
        cbox.pack_start(cell, True)
        cbox.add_attribute(cell, 'text', 0)
        hbox.pack_start(cbox)

        self.filetypes = filetypes
        self.sorted_filetypes = sorted(six.iteritems(filetypes))
        default = 0
        for i, (ext, name) in enumerate(self.sorted_filetypes):
            cbox.append_text("%s (*.%s)" % (name, ext))
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

            self.set_current_name(filename)
        cbox.connect("changed", cb_cbox_changed)

        hbox.show_all()
        self.set_extra_widget(hbox)
