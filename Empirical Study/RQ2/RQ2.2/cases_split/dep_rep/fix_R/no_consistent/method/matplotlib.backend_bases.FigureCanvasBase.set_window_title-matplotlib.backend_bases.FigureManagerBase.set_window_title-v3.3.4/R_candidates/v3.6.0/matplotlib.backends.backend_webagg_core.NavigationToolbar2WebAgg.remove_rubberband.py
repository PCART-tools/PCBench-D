    def remove_rubberband(self):
        self.canvas.send_event("rubberband", x0=-1, y0=-1, x1=-1, y1=-1)
