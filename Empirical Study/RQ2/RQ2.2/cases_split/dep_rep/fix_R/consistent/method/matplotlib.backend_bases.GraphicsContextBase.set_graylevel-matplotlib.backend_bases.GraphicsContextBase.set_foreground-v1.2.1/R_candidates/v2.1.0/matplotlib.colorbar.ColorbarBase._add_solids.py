    def _add_solids(self, X, Y, C):
        '''
        Draw the colors using :meth:`~matplotlib.axes.Axes.pcolormesh`;
        optionally add separators.
        '''
        if self.orientation == 'vertical':
            args = (X, Y, C)
        else:
            args = (np.transpose(Y), np.transpose(X), np.transpose(C))
        kw = dict(cmap=self.cmap,
                  norm=self.norm,
                  alpha=self.alpha,
                  edgecolors='None')
        # Save, set, and restore hold state to keep pcolor from
        # clearing the axes. Ordinarily this will not be needed,
        # since the axes object should already have hold set.
        _hold = self.ax._hold
        self.ax._hold = True
        col = self.ax.pcolormesh(*args, **kw)
        self.ax._hold = _hold
        #self.add_observer(col) # We should observe, not be observed...

        if self.solids is not None:
            self.solids.remove()
        self.solids = col
        if self.dividers is not None:
            self.dividers.remove()
            self.dividers = None
        if self.drawedges:
            linewidths = (0.5 * mpl.rcParams['axes.linewidth'],)
            self.dividers = collections.LineCollection(self._edges(X, Y),
                                    colors=(mpl.rcParams['axes.edgecolor'],),
                                    linewidths=linewidths)
            self.ax.add_collection(self.dividers)
        elif len(self._y) >= self.n_rasterize:
            self.solids.set_rasterized(True)
