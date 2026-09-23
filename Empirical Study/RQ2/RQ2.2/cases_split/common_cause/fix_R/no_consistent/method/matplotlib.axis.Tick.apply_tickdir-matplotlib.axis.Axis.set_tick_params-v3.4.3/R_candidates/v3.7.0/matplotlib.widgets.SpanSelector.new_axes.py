    def new_axes(self, ax):
        """Set SpanSelector to operate on a new Axes."""
        self.ax = ax
        if self.canvas is not ax.figure.canvas:
            if self.canvas is not None:
                self.disconnect_events()

            self.canvas = ax.figure.canvas
            self.connect_default_events()

        # Reset
        self._selection_completed = False

        if self.direction == 'horizontal':
            trans = ax.get_xaxis_transform()
            w, h = 0, 1
        else:
            trans = ax.get_yaxis_transform()
            w, h = 1, 0
        rect_artist = Rectangle((0, 0), w, h,
                                transform=trans,
                                visible=False,
                                **self._props)

        self.ax.add_patch(rect_artist)
        self._selection_artist = rect_artist
