    def release(self, event):
        if hasattr(self, "lastrect"):
            self.canvas._tkcanvas.delete(self.lastrect)
            del self.lastrect
