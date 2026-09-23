    def add_lines(self, levels, colors, linewidths, erase=True):
        '''
        Draw lines on the colorbar.

        *colors* and *linewidths* must be scalars or
        sequences the same length as *levels*.

        Set *erase* to False to add lines without first
        removing any previously added lines.
        '''
        y = self._locate(levels)
        igood = (y < 1.001) & (y > -0.001)
        y = y[igood]
        if cbook.iterable(colors):
            colors = np.asarray(colors)[igood]
        if cbook.iterable(linewidths):
            linewidths = np.asarray(linewidths)[igood]
        X, Y = np.meshgrid([0, 1], y)
        if self.orientation == 'vertical':
            xy = np.stack([X, Y], axis=-1)
        else:
            xy = np.stack([Y, X], axis=-1)
        col = collections.LineCollection(xy, linewidths=linewidths)

        if erase and self.lines:
            for lc in self.lines:
                lc.remove()
            self.lines = []
        self.lines.append(col)
        col.set_color(colors)
        self.ax.add_collection(col)
        self.stale = True
