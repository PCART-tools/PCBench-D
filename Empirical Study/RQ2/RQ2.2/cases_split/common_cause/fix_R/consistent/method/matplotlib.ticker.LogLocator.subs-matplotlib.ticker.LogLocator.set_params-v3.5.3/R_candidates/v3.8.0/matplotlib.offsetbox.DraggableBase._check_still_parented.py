    def _check_still_parented(self):
        if self.ref_artist.figure is None:
            self.disconnect()
            return False
        else:
            return True
