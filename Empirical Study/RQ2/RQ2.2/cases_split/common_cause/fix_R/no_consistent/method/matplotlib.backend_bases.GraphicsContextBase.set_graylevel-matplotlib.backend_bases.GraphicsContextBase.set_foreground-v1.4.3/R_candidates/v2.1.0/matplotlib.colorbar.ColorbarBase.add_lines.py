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
        N = len(y)
        x = np.array([0.0, 1.0])
        X, Y = np.meshgrid(x, y)
        if self.orientation == 'vertical':
            xy = [list(zip(X[i], Y[i])) for i in xrange(N)]
        else:
            xy = [list(zip(Y[i], X[i])) for i in xrange(N)]
        col = collections.LineCollection(xy, linewidths=linewidths)

        if erase and self.lines:
            for lc in self.lines:
                lc.remove()
            self.lines = []
        self.lines.append(col)
        col.set_color(colors)
        self.ax.add_collection(col)
        self.stale = True
