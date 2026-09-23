    def update(self):
        """draw using newfangled blit or oldfangled draw depending on
        useblit

        """
        if not self.ax.get_visible():
            return False

        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            for artist in self.artists:
                self.ax.draw_artist(artist)

            self.canvas.blit(self.ax.bbox)

        else:
            self.canvas.draw_idle()
        return False
