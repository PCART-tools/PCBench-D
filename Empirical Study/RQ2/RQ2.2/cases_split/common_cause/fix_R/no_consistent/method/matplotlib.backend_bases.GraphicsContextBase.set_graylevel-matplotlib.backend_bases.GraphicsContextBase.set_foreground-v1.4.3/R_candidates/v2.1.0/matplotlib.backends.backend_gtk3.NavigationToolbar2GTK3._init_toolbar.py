    def _init_toolbar(self):
        self.set_style(Gtk.ToolbarStyle.ICONS)
        basedir = os.path.join(rcParams['datapath'],'images')

        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.insert( Gtk.SeparatorToolItem(), -1 )
                continue
            fname = os.path.join(basedir, image_file + '.png')
            image = Gtk.Image()
            image.set_from_file(fname)
            tbutton = Gtk.ToolButton()
            tbutton.set_label(text)
            tbutton.set_icon_widget(image)
            self.insert(tbutton, -1)
            tbutton.connect('clicked', getattr(self, callback))
            tbutton.set_tooltip_text(tooltip_text)

        toolitem = Gtk.SeparatorToolItem()
        self.insert(toolitem, -1)
        toolitem.set_draw(False)
        toolitem.set_expand(True)

        toolitem = Gtk.ToolItem()
        self.insert(toolitem, -1)
        self.message = Gtk.Label()
        toolitem.add(self.message)

        self.show_all()
