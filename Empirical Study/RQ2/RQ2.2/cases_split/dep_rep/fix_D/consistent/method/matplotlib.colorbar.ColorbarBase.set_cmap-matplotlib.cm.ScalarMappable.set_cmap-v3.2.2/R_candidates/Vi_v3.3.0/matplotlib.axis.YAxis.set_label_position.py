    def set_label_position(self, position):
        """
        Set the label position (left or right)

        Parameters
        ----------
        position : {'left', 'right'}
        """
        self.label.set_rotation_mode('anchor')
        self.label.set_horizontalalignment('center')
        self.label.set_verticalalignment(cbook._check_getitem({
            'left': 'bottom', 'right': 'top',
        }, position=position))
        self.label_position = position
        self.stale = True
