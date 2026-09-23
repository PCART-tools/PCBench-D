    def draw(self, renderer):
        """
        Update the location of children if necessary and draw them
        to the given *renderer*.
        """
        w, h, xdescent, ydescent, offsets = self.get_extent_offsets(renderer)
        px, py = self.get_offset(w, h, xdescent, ydescent, renderer)
        for c, (ox, oy) in zip(self.get_visible_children(), offsets):
            c.set_offset((px + ox, py + oy))
            c.draw(renderer)
        bbox_artist(self, renderer, fill=False, props=dict(pad=0.))
        self.stale = False
