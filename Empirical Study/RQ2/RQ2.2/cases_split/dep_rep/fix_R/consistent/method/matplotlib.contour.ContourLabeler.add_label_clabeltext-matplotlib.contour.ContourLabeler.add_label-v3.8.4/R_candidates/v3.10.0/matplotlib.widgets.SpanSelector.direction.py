    @direction.setter
    def direction(self, direction):
        """Set the direction of the span selector."""
        _api.check_in_list(['horizontal', 'vertical'], direction=direction)
        if hasattr(self, '_direction') and direction != self._direction:
            # remove previous artists
            self._selection_artist.remove()
            if self._interactive:
                self._edge_handles.remove()
            self._direction = direction
            self.new_axes(self.ax)
            if self._interactive:
                self._setup_edge_handles(self._handle_props)
        else:
            self._direction = direction
