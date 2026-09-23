    def draw_artist(self, a):
        """
        Efficiently redraw a single artist.
        """
        a.draw(self.figure.canvas.get_renderer())
