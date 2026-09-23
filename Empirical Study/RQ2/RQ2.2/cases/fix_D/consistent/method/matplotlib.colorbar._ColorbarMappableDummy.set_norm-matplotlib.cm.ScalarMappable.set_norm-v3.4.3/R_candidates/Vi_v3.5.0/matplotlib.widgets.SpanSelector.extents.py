    @extents.setter
    def extents(self, extents):
        # Update displayed shape
        self._draw_shape(*extents)
        if self._interactive:
            # Update displayed handles
            self._edge_handles.set_data(self.extents)
        self.set_visible(self.visible)
        self.update()
