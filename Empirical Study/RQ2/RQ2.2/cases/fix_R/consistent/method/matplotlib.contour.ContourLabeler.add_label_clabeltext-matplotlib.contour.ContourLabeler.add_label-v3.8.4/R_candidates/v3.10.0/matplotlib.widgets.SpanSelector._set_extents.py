    def _set_extents(self, extents):
        # Update displayed shape
        if self.snap_values is not None:
            extents = tuple(self._snap(extents, self.snap_values))
        self._draw_shape(*extents)
        if self._interactive:
            # Update displayed handles
            self._edge_handles.set_data(self.extents)
        self.set_visible(self._visible)
        self.update()
