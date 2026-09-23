    def set_alpha(self, alpha):
        # docstring inherited
        super().set_alpha(alpha)
        self._update_dict['array'] = True
        self._set_facecolor(self._original_facecolor)
        self._set_edgecolor(self._original_edgecolor)
