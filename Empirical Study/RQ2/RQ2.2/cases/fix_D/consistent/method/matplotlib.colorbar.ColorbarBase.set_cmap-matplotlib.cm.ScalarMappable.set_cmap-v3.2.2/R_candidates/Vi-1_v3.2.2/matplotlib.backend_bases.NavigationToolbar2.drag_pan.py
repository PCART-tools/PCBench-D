    def drag_pan(self, event):
        """Callback for dragging in pan/zoom mode."""
        for a, ind in self._xypress:
            #safer to use the recorded button at the press than current button:
            #multiple button can get pressed during motion...
            a.drag_pan(self._button_pressed, event.key, event.x, event.y)
        self.canvas.draw_idle()
