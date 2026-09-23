    def draw_artist(self, a):
        """
        Efficiently redraw a single artist.
        """
        a.draw(self.get_figure(root=True).canvas.get_renderer())
