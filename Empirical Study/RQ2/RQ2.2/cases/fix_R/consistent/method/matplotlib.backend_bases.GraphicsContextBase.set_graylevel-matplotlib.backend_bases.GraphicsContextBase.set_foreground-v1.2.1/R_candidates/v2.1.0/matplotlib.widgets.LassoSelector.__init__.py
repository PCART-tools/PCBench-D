    def __init__(self, ax, onselect=None, useblit=True, lineprops=None,
                 button=None):
        _SelectorWidget.__init__(self, ax, onselect, useblit=useblit,
                                 button=button)

        self.verts = None

        if lineprops is None:
            lineprops = dict()
        if useblit:
            lineprops['animated'] = True
        self.line = Line2D([], [], **lineprops)
        self.line.set_visible(False)
        self.ax.add_line(self.line)
        self.artists = [self.line]
