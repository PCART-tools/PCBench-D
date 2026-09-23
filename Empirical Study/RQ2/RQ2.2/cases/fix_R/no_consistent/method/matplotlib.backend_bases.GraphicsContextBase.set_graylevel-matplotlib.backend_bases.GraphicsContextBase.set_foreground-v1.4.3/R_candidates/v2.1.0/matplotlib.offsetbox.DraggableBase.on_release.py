    def on_release(self, event):
        if self.got_artist:
            self.finalize_offset()
            self.got_artist = False
            self.canvas.mpl_disconnect(self._c1)

            if self._use_blit:
                self.ref_artist.set_animated(False)
