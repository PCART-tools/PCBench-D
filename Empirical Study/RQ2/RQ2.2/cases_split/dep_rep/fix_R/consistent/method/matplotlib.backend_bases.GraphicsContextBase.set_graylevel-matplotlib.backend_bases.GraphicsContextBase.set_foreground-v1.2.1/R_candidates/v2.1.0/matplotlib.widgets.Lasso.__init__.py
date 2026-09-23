    def __init__(self, ax, xy, callback=None, useblit=True):
        AxesWidget.__init__(self, ax)

        self.useblit = useblit and self.canvas.supports_blit
        if self.useblit:
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)

        x, y = xy
        self.verts = [(x, y)]
        self.line = Line2D([x], [y], linestyle='-', color='black', lw=2)
        self.ax.add_line(self.line)
        self.callback = callback
        self.connect_event('button_release_event', self.onrelease)
        self.connect_event('motion_notify_event', self.onmove)
