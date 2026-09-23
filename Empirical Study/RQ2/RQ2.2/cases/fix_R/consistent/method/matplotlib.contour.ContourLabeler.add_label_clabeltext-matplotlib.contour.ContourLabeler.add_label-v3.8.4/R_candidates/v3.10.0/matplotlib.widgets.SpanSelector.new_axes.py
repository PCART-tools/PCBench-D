    def new_axes(self, ax, *, _props=None, _init=False):
        """Set SpanSelector to operate on a new Axes."""
        reconnect = False
        if _init or self.canvas is not ax.get_figure(root=True).canvas:
            if self.canvas is not None:
                self.disconnect_events()
            reconnect = True
        self.ax = ax
        if reconnect:
            self.connect_default_events()

        # Reset
        self._selection_completed = False

        if self.direction == 'horizontal':
            trans = ax.get_xaxis_transform()
            w, h = 0, 1
        else:
            trans = ax.get_yaxis_transform()
            w, h = 1, 0
        rect_artist = Rectangle((0, 0), w, h, transform=trans, visible=False)
        if _props is not None:
            rect_artist.update(_props)
        elif self._selection_artist is not None:
            rect_artist.update_from(self._selection_artist)

        self.ax.add_patch(rect_artist)
        self._selection_artist = rect_artist
