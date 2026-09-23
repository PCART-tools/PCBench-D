    def update_background(self, event):
        """Force an update of the background."""
        # If you add a call to `ignore` here, you'll want to check edge case:
        # `release` can call a draw event even when `ignore` is True.
        if not self.useblit:
            return
        # Make sure that widget artists don't get accidentally included in the
        # background, by re-rendering the background if needed (and then
        # re-re-rendering the canvas with the visible widget artists).
        # We need to remove all artists which will be drawn when updating
        # the selector: if we have animated artists in the figure, it is safer
        # to redrawn by default, in case they have updated by the callback
        # zorder needs to be respected when redrawing
        artists = sorted(self.artists + self._get_animated_artists(),
                         key=lambda a: a.get_zorder())
        needs_redraw = any(artist.get_visible() for artist in artists)
        with ExitStack() as stack:
            if needs_redraw:
                for artist in artists:
                    stack.enter_context(artist._cm_set(visible=False))
                self.canvas.draw()
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        if needs_redraw:
            for artist in artists:
                self.ax.draw_artist(artist)
