    def __init__(self, canvas, num):
        FigureManagerBase.__init__(self, canvas, num)

        self.window = gtk.Window()
        self.window.set_wmclass("matplotlib", "Matplotlib")
        self.set_window_title("Figure %d" % num)
        if window_icon:
            try:
                self.window.set_icon_from_file(window_icon)
            except:
                # some versions of gtk throw a glib.GError but not
                # all, so I am not sure how to catch it.  I am unhappy
                # diong a blanket catch here, but an not sure what a
                # better way is - JDH
                verbose.report('Could not load matplotlib icon: %s' % sys.exc_info()[1])

        self.vbox = gtk.VBox()
        self.window.add(self.vbox)
        self.vbox.show()

        self.canvas.show()

        self.vbox.pack_start(self.canvas, True, True)

        self.toolbar = self._get_toolbar(canvas)

        # calculate size for window
        w = int (self.canvas.figure.bbox.width)
        h = int (self.canvas.figure.bbox.height)

        if self.toolbar is not None:
            self.toolbar.show()
            self.vbox.pack_end(self.toolbar, False, False)

            tb_w, tb_h = self.toolbar.size_request()
            h += tb_h
        self.window.set_default_size (w, h)

        def destroy(*args):
            Gcf.destroy(num)
        self.window.connect("destroy", destroy)
        self.window.connect("delete_event", destroy)
        if matplotlib.is_interactive():
            self.window.show()
            self.canvas.draw_idle()

        def notify_axes_change(fig):
            'this will be called whenever the current axes is changed'
            if self.toolbar is not None: self.toolbar.update()
        self.canvas.figure.add_axobserver(notify_axes_change)

        self.canvas.grab_focus()
