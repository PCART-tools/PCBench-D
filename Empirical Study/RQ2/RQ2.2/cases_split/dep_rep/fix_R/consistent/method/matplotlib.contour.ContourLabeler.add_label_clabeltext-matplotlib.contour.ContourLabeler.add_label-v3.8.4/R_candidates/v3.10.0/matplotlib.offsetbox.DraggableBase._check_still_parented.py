    def _check_still_parented(self):
        if self.ref_artist.get_figure(root=False) is None:
            self.disconnect()
            return False
        else:
            return True
