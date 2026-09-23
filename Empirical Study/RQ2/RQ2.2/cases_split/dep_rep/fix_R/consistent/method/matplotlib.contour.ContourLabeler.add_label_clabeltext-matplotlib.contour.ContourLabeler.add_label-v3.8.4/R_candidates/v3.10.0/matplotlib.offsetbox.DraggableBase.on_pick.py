    def on_pick(self, evt):
        if self._check_still_parented():
            if evt.artist == self.ref_artist:
                self.mouse_x = evt.mouseevent.x
                self.mouse_y = evt.mouseevent.y
                self.save_offset()
                self.got_artist = True
            if self.got_artist and self._use_blit:
                self.ref_artist.set_animated(True)
                self.canvas.draw()
                fig = self.ref_artist.get_figure(root=False)
                self.background = self.canvas.copy_from_bbox(fig.bbox)
                self.ref_artist.draw(fig._get_renderer())
                self.canvas.blit()
