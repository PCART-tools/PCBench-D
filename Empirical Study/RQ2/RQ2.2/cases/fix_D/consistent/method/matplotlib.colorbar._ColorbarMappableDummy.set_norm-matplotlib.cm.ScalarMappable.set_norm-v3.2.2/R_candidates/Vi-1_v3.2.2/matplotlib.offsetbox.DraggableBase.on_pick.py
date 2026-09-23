    def on_pick(self, evt):
        if self._check_still_parented() and evt.artist == self.ref_artist:

            self.mouse_x = evt.mouseevent.x
            self.mouse_y = evt.mouseevent.y
            self.got_artist = True

            if self._use_blit:
                self.ref_artist.set_animated(True)
                self.canvas.draw()
                self.background = self.canvas.copy_from_bbox(
                                    self.ref_artist.figure.bbox)
                self.ref_artist.draw(self.ref_artist.figure._cachedRenderer)
                self.canvas.blit()
                self._c1 = self.canvas.mpl_connect('motion_notify_event',
                                                   self.on_motion_blit)
            else:
                self._c1 = self.canvas.mpl_connect('motion_notify_event',
                                                   self.on_motion)
            self.save_offset()
