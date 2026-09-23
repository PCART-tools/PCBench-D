    def on_motion_blit(self, evt):
        if self._check_still_parented() and self.got_artist:
            dx = evt.x - self.mouse_x
            dy = evt.y - self.mouse_y
            self.update_offset(dx, dy)
            self.canvas.restore_region(self.background)
            self.ref_artist.draw(self.ref_artist.figure._cachedRenderer)
            self.canvas.blit()
