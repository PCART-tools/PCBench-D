    def draw(self, renderer):
        # docstring inherited
        width, height, xdescent, ydescent, offsets = self.get_extent_offsets(
                                                        renderer)

        px, py = self.get_offset(width, height, xdescent, ydescent, renderer)

        for c, (ox, oy) in zip(self.get_visible_children(), offsets):
            c.set_offset((px + ox, py + oy))

        self.draw_frame(renderer)

        for c in self.get_visible_children():
            c.draw(renderer)

        #bbox_artist(self, renderer, fill=False, props=dict(pad=0.))
        self.stale = False
