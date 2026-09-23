    def set_offset_position(self, position):
        """
        Parameters
        ----------
        position : {'left', 'right'}
        """
        x, y = self.offsetText.get_position()
        x = _api.check_getitem({'left': 0, 'right': 1}, position=position)

        self.offsetText.set_ha(position)
        self.offsetText.set_position((x, y))
        self.stale = True
