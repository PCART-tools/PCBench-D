    def _add_solids(self, X, Y, C):
        """
        Draw the colors using `~.axes.Axes.pcolormesh`;
        optionally add separators.
        """
        if self.orientation == 'vertical':
            args = (X, Y, C)
        else:
            args = (np.transpose(Y), np.transpose(X), np.transpose(C))
        kw = dict(cmap=self.cmap,
                  norm=self.norm,
                  alpha=self.alpha,
                  edgecolors='None')
        _log.debug('Setting pcolormesh')
        col = self.ax.pcolormesh(*args, **kw, shading='flat')
        # self.add_observer(col) # We should observe, not be observed...

        if self.solids is not None:
            self.solids.remove()
        self.solids = col
        if self.dividers is not None:
            self.dividers.remove()
            self.dividers = None
        if self.drawedges:
            linewidths = (0.5 * mpl.rcParams['axes.linewidth'],)
            self.dividers = collections.LineCollection(
                    self._edges(X, Y),
                    colors=(mpl.rcParams['axes.edgecolor'],),
                    linewidths=linewidths)
            self.ax.add_collection(self.dividers)
        elif len(self._y) >= self.n_rasterize:
            self.solids.set_rasterized(True)
