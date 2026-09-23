    def get_results(self, box, used_characters):
        _mathtext.ship(0, 0, box)
        return self._PSResult(self.width,
                              self.height + self.depth,
                              self.depth,
                              self.pswriter,
                              used_characters)
