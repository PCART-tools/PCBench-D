    def update(self):
        """Draw using blit() or draw_idle(), depending on ``self.useblit``."""
        if (not self.ax.get_visible() or
                self.ax.get_figure(root=True)._get_renderer() is None):
            return
        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            else:
                self.update_background(None)
            # We need to draw all artists, which are not included in the
            # background, therefore we also draw self._get_animated_artists()
            # and we make sure that we respect z_order
            artists = sorted(self.artists + self._get_animated_artists(),
                             key=lambda a: a.get_zorder())
            for artist in artists:
                self.ax.draw_artist(artist)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()
