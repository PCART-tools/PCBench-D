    def draw(self):
        """Render the figure, and queue a request for a Qt draw.
        """
        # The renderer draw is done here; delaying causes problems with code
        # that uses the result of the draw() to update plot elements.
        if self._is_drawing:
            return
        with cbook._setattr_cm(self, _is_drawing=True):
            super().draw()
        self._erase_before_paint = True
        self.update()
