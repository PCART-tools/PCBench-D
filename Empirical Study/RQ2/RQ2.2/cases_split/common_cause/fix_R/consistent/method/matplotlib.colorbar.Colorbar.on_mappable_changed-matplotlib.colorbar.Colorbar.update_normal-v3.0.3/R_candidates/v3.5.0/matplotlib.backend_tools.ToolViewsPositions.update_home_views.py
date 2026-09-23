    def update_home_views(self, figure=None):
        """
        Make sure that ``self.home_views`` has an entry for all axes present
        in the figure.
        """

        if not figure:
            figure = self.figure
        for a in figure.get_axes():
            if a not in self.home_views[figure]:
                self.home_views[figure][a] = a._get_view()
