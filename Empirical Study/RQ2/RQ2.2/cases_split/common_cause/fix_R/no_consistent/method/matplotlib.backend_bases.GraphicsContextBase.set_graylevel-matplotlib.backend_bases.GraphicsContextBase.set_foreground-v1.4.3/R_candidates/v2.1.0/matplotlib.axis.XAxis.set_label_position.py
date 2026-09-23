    def set_label_position(self, position):
        """
        Set the label position (top or bottom)

        ACCEPTS: [ 'top' | 'bottom' ]
        """
        if position == 'top':
            self.label.set_verticalalignment('baseline')
        elif position == 'bottom':
            self.label.set_verticalalignment('top')
        else:
            msg = "Position accepts only [ 'top' | 'bottom' ]"
            raise ValueError(msg)
        self.label_position = position
        self.stale = True
