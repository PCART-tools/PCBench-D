    def set_offset_position(self, position):
        """
        Parameters
        ----------
        position : {'left', 'right'}
        """
        x, y = self.offsetText.get_position()
        if position == 'left':
            x = 0
        elif position == 'right':
            x = 1
        else:
            raise ValueError("Position accepts only [ 'left' | 'right' ]")

        self.offsetText.set_ha(position)
        self.offsetText.set_position((x, y))
        self.stale = True
