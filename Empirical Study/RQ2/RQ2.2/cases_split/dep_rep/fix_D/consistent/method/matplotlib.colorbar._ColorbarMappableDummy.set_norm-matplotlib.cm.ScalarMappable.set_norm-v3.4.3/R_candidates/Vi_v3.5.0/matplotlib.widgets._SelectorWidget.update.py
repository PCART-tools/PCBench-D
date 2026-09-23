    def update(self):
        """Draw using blit() or draw_idle(), depending on ``self.useblit``."""
        if not self.ax.get_visible() or self.ax.figure._cachedRenderer is None:
            return False
        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            else:
                self.update_background(None)
            for artist in self.artists:
                self.ax.draw_artist(artist)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()
        return False
