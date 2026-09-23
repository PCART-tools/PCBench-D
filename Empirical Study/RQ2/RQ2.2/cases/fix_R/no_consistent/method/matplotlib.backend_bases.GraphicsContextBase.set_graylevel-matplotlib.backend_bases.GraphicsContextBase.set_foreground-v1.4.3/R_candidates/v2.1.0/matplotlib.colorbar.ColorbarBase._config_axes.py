    def _config_axes(self, X, Y):
        '''
        Make an axes patch and outline.
        '''
        ax = self.ax
        ax.set_frame_on(False)
        ax.set_navigate(False)
        xy = self._outline(X, Y)
        ax.update_datalim(xy)
        ax.set_xlim(*ax.dataLim.intervalx)
        ax.set_ylim(*ax.dataLim.intervaly)
        if self.outline is not None:
            self.outline.remove()
        self.outline = mpatches.Polygon(
            xy, edgecolor=mpl.rcParams['axes.edgecolor'],
            facecolor='none',
            linewidth=mpl.rcParams['axes.linewidth'],
            closed=True,
            zorder=2)
        ax.add_artist(self.outline)
        self.outline.set_clip_box(None)
        self.outline.set_clip_path(None)
        c = mpl.rcParams['axes.facecolor']
        if self.patch is not None:
            self.patch.remove()
        self.patch = mpatches.Polygon(xy, edgecolor=c,
                                      facecolor=c,
                                      linewidth=0.01,
                                      zorder=-1)
        ax.add_artist(self.patch)

        self.update_ticks()
