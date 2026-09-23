    def set_offset_position(self, position):
        x, y = self.offsetText.get_position()
        if position == 'left':
            x = 0
        elif position == 'right':
            x = 1
        else:
            msg = "Position accepts only [ 'left' | 'right' ]"
            raise ValueError(msg)

        self.offsetText.set_ha(position)
        self.offsetText.set_position((x, y))
        self.stale = True
