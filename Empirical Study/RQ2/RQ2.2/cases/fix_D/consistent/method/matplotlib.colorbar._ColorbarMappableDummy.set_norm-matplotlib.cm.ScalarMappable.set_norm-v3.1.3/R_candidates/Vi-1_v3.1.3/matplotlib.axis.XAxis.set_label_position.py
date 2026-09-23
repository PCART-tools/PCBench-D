    def set_label_position(self, position):
        """
        Set the label position (top or bottom)

        Parameters
        ----------
        position : {'top', 'bottom'}
        """
        if position == 'top':
            self.label.set_verticalalignment('baseline')
        elif position == 'bottom':
            self.label.set_verticalalignment('top')
        else:
            raise ValueError("Position accepts only 'top' or 'bottom'")
        self.label_position = position
        self.stale = True
