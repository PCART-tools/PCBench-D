    def draw_artist(self, a):
        """
        Draw `.Artist` *a* only.
        """
        a.draw(self.canvas.get_renderer())
