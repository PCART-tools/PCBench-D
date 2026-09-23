    def update_view(self):
        """
        Update the view limits and position for each Axes from the current
        stack position. If any Axes are present in the figure that aren't in
        the current stack position, use the home view limits for those Axes and
        don't update *any* positions.
        """

        views = self.views[self.figure]()
        if views is None:
            return
        pos = self.positions[self.figure]()
        if pos is None:
            return
        home_views = self.home_views[self.figure]
        all_axes = self.figure.get_axes()
        for a in all_axes:
            if a in views:
                cur_view = views[a]
            else:
                cur_view = home_views[a]
            a._set_view(cur_view)

        if set(all_axes).issubset(pos):
            for a in all_axes:
                # Restore both the original and modified positions
                a._set_position(pos[a][0], 'original')
                a._set_position(pos[a][1], 'active')

        self.figure.canvas.draw_idle()
