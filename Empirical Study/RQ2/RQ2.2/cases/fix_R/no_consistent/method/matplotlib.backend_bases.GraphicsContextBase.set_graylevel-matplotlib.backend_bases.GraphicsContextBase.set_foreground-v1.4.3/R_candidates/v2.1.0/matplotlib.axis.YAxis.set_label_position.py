    def set_label_position(self, position):
        """
        Set the label position (left or right)

        ACCEPTS: [ 'left' | 'right' ]
        """
        self.label.set_rotation_mode('anchor')
        self.label.set_horizontalalignment('center')
        if position == 'left':
            self.label.set_verticalalignment('bottom')
        elif position == 'right':
            self.label.set_verticalalignment('top')
        else:
            msg = "Position accepts only [ 'left' | 'right' ]"
            raise ValueError(msg)
        self.label_position = position
        self.stale = True
