    def _add_solids(self, X, Y, C):
        """
        Draw the colors using :class:`~matplotlib.patches.Patch`;
        optionally add separators.
        """
        kw = {'alpha': self.alpha, }

        n_segments = len(C)

        # ensure there are sufficient hatches
        hatches = self.mappable.hatches * n_segments

        patches = []
        for i in range(len(X) - 1):
            val = C[i][0]
            hatch = hatches[i]

            xy = np.array([[X[i][0], Y[i][0]],
                           [X[i][1], Y[i][0]],
                           [X[i + 1][1], Y[i + 1][0]],
                           [X[i + 1][0], Y[i + 1][1]]])

            if self.orientation == 'horizontal':
                # if horizontal swap the xs and ys
                xy = xy[..., ::-1]

            patch = mpatches.PathPatch(mpath.Path(xy),
                                       facecolor=self.cmap(self.norm(val)),
                                       hatch=hatch, linewidth=0,
                                       antialiased=False, **kw)
            self.ax.add_patch(patch)
            patches.append(patch)

        if self.solids_patches:
            for solid in self.solids_patches:
                solid.remove()

        self.solids_patches = patches

        if self.dividers is not None:
            self.dividers.remove()
            self.dividers = None

        if self.drawedges:
            self.dividers = collections.LineCollection(
                    self._edges(X, Y),
                    colors=(mpl.rcParams['axes.edgecolor'],),
                    linewidths=(0.5 * mpl.rcParams['axes.linewidth'],))
            self.ax.add_collection(self.dividers)
