    def get_window_extent(self, renderer=None):
        # make sure the location is updated so that transforms etc are
        # correct:
        self._adjust_location()
        return super().get_window_extent(renderer=renderer)
