    def set_label_position(self, position):
        """
        Set the label position (top or bottom)

        Parameters
        ----------
        position : {'top', 'bottom'}
        """
        self.label.set_verticalalignment(_api.check_getitem({
            'top': 'baseline', 'bottom': 'top',
        }, position=position))
        self.label_position = position
        self.stale = True
