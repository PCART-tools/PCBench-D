    def _add_solids_pcolormesh(self, X, Y, C):
        _log.debug('Setting pcolormesh')
        if C.shape[0] == Y.shape[0]:
            # trim the last one to be compatible with old behavior.
            C = C[:-1]
        self.solids = self.ax.pcolormesh(
            X, Y, C, cmap=self.cmap, norm=self.norm, alpha=self.alpha,
            edgecolors='none', shading='flat')
        if not self.drawedges:
            if len(self._y) >= self.n_rasterize:
                self.solids.set_rasterized(True)
