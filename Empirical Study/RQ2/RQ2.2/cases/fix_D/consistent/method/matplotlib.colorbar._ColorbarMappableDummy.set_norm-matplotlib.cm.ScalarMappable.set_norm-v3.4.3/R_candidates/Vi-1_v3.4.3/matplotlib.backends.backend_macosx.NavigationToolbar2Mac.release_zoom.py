    def release_zoom(self, event):
        super().release_zoom(event)
        self.canvas.remove_rubberband()
