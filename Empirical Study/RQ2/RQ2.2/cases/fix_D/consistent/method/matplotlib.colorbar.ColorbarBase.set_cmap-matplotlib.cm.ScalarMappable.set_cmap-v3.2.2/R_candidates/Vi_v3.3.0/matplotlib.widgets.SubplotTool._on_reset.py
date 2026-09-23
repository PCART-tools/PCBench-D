    def _on_reset(self, event):
        with ExitStack() as stack:
            # Temporarily disable drawing on self and self's sliders.
            stack.enter_context(cbook._setattr_cm(self, drawon=False))
            for slider in self._sliders:
                stack.enter_context(cbook._setattr_cm(slider, drawon=False))
            # Reset the slider to the initial position.
            for slider in self._sliders:
                slider.reset()
        # Draw the canvas.
        if self.drawon:
            event.canvas.draw()
            self.targetfig.canvas.draw()
