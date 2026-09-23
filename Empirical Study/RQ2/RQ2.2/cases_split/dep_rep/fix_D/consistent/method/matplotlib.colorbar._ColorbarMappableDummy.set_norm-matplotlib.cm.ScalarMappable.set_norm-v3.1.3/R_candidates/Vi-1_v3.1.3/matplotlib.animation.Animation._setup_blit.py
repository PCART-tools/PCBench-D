    def _setup_blit(self):
        # Setting up the blit requires: a cache of the background for the
        # axes
        self._blit_cache = dict()
        self._drawn_artists = []
        for ax in self._fig.axes:
            ax.callbacks.connect('xlim_changed',
                                 lambda ax: self._blit_cache.pop(ax, None))
            ax.callbacks.connect('ylim_changed',
                                 lambda ax: self._blit_cache.pop(ax, None))
        self._resize_id = self._fig.canvas.mpl_connect('resize_event',
                                                       self._handle_resize)
        self._post_draw(None, self._blit)
