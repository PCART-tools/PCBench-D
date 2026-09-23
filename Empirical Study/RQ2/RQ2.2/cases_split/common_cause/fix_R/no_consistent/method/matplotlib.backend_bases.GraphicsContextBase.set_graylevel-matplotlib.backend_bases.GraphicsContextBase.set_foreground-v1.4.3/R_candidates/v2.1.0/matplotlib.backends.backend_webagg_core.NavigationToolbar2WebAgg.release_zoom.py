    def release_zoom(self, event):
        backend_bases.NavigationToolbar2.release_zoom(self, event)
        self.canvas.send_event(
            "rubberband", x0=-1, y0=-1, x1=-1, y1=-1)
