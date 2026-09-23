    def add_figure(self, figure):
        """Add the current figure to the stack of views and positions."""

        if figure not in self.views:
            self.views[figure] = cbook._Stack()
            self.positions[figure] = cbook._Stack()
            self.home_views[figure] = WeakKeyDictionary()
            # Define Home
            self.push_current(figure)
            # Make sure we add a home view for new Axes as they're added
            figure.add_axobserver(lambda fig: self.update_home_views(fig))
