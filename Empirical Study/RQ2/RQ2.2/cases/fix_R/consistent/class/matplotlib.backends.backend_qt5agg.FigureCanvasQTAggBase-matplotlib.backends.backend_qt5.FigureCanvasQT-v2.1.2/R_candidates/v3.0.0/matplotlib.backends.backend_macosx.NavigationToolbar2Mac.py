class NavigationToolbar2Mac(_macosx.NavigationToolbar2, NavigationToolbar2):

    def __init__(self, canvas):
        NavigationToolbar2.__init__(self, canvas)

    def _init_toolbar(self):
        basedir = os.path.join(rcParams['datapath'], "images")
        _macosx.NavigationToolbar2.__init__(self, basedir)

    def draw_rubberband(self, event, x0, y0, x1, y1):
        self.canvas.set_rubberband(int(x0), int(y0), int(x1), int(y1))

    def release(self, event):
        self.canvas.remove_rubberband()

    def set_cursor(self, cursor):
        _macosx.set_cursor(cursor)

    def save_figure(self, *args):
        filename = _macosx.choose_save_file('Save the figure',
                                            self.canvas.get_default_filename())
        if filename is None: # Cancel
            return
        self.canvas.figure.savefig(filename)

    def prepare_configure_subplots(self):
        toolfig = Figure(figsize=(6,3))
        canvas = FigureCanvasMac(toolfig)
        toolfig.subplots_adjust(top=0.9)
        tool = SubplotTool(self.canvas.figure, toolfig)
        return canvas

    def set_message(self, message):
        _macosx.NavigationToolbar2.set_message(self, message.encode('utf-8'))
