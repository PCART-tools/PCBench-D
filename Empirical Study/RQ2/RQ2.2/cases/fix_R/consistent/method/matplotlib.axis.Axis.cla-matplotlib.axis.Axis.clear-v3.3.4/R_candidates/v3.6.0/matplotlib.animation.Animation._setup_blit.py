    def _setup_blit(self):
        # Setting up the blit requires: a cache of the background for the Axes
        self._blit_cache = dict()
        self._drawn_artists = []
        # _post_draw needs to be called first to initialize the renderer
        self._post_draw(None, self._blit)
        # Then we need to clear the Frame for the initial draw
        # This is typically handled in _on_resize because QT and Tk
        # emit a resize event on launch, but the macosx backend does not,
        # thus we force it here for everyone for consistency
        self._init_draw()
        # Connect to future resize events
        self._resize_id = self._fig.canvas.mpl_connect('resize_event',
                                                       self._on_resize)
