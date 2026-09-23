    def release_zoom(self, event):
        super().release_zoom(event)
        if hasattr(self, "lastrect"):
            self.canvas._tkcanvas.delete(self.lastrect)
            del self.lastrect
