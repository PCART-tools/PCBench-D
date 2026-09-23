    def remove_rubberband(self):
        if self.canvas._rubberband_rect:
            self.canvas._tkcanvas.delete(self.canvas._rubberband_rect)
            self.canvas._rubberband_rect = None
