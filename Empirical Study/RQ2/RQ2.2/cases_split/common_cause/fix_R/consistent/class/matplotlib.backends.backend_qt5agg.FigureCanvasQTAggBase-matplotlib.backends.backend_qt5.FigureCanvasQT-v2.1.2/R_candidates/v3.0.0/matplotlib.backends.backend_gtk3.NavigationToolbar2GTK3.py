class NavigationToolbar2GTK3(NavigationToolbar2, Gtk.Toolbar):
    def __init__(self, canvas, window):
        self.win = window
        GObject.GObject.__init__(self)
        NavigationToolbar2.__init__(self, canvas)
        self.ctx = None

    def set_message(self, s):
        self.message.set_label(s)

    def set_cursor(self, cursor):
        self.canvas.get_property("window").set_cursor(cursord[cursor])
        Gtk.main_iteration()

    def draw_rubberband(self, event, x0, y0, x1, y1):
        'adapted from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/189744'
        self.ctx = self.canvas.get_property("window").cairo_create()

        # todo: instead of redrawing the entire figure, copy the part of
        # the figure that was covered by the previous rubberband rectangle
        self.canvas.draw()

        height = self.canvas.figure.bbox.height
        y1 = height - y1
        y0 = height - y0
        w = abs(x1 - x0)
        h = abs(y1 - y0)
        rect = [int(val) for val in (min(x0, x1), min(y0, y1), w, h)]

        self.ctx.new_path()
        self.ctx.set_line_width(0.5)
        self.ctx.rectangle(rect[0], rect[1], rect[2], rect[3])
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.stroke()

    def _init_toolbar(self):
        self.set_style(Gtk.ToolbarStyle.ICONS)
        basedir = os.path.join(rcParams['datapath'], 'images')

        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.insert(Gtk.SeparatorToolItem(), -1)
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

    def get_filechooser(self):
        fc = FileChooserDialog(
            title='Save the figure',
            parent=self.win,
            path=os.path.expanduser(rcParams['savefig.directory']),
            filetypes=self.canvas.get_supported_filetypes(),
            default_filetype=self.canvas.get_default_filetype())
        fc.set_current_name(self.canvas.get_default_filename())
        return fc

    def save_figure(self, *args):
        chooser = self.get_filechooser()
        fname, format = chooser.get_filename_from_user()
        chooser.destroy()
        if fname:
            startpath = os.path.expanduser(rcParams['savefig.directory'])
            # Save dir for next time, unless empty str (i.e., use cwd).
            if startpath != "":
                rcParams['savefig.directory'] = os.path.dirname(fname)
            try:
                self.canvas.figure.savefig(fname, format=format)
            except Exception as e:
                error_msg_gtk(str(e), parent=self)

    def configure_subplots(self, button):
        toolfig = Figure(figsize=(6, 3))
        canvas = self._get_canvas(toolfig)
        toolfig.subplots_adjust(top=0.9)
        tool =  SubplotTool(self.canvas.figure, toolfig)

        w = int(toolfig.bbox.width)
        h = int(toolfig.bbox.height)

        window = Gtk.Window()
        try:
            window.set_icon_from_file(window_icon)
        except Exception:
            # we presumably already logged a message on the
            # failure of the main plot, don't keep reporting
            pass
        window.set_title("Subplot Configuration Tool")
        window.set_default_size(w, h)
        vbox = Gtk.Box()
        vbox.set_property("orientation", Gtk.Orientation.VERTICAL)
        window.add(vbox)
        vbox.show()

        canvas.show()
        vbox.pack_start(canvas, True, True, 0)
        window.show()

    def _get_canvas(self, fig):
        return self.canvas.__class__(fig)
