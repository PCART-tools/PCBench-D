    def new_axes(self, ax):
        """Set SpanSelector to operate on a new Axes."""
        self.ax = ax
        if self.canvas is not ax.figure.canvas:
            if self.canvas is not None:
                self.disconnect_events()

            self.canvas = ax.figure.canvas
            self.connect_default_events()

        if self.direction == 'horizontal':
            trans = blended_transform_factory(self.ax.transData,
                                              self.ax.transAxes)
            w, h = 0, 1
        else:
            trans = blended_transform_factory(self.ax.transAxes,
                                              self.ax.transData)
            w, h = 1, 0
        self.rect = Rectangle((0, 0), w, h,
                              transform=trans,
                              visible=False,
                              **self.rectprops)
        if self.span_stays:
            self.stay_rect = Rectangle((0, 0), w, h,
                                       transform=trans,
                                       visible=False,
                                       **self.rectprops)
            self.stay_rect.set_animated(False)
            self.ax.add_patch(self.stay_rect)

        self.ax.add_patch(self.rect)
        self.artists = [self.rect]
