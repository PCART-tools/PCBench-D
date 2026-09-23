    def update_from(self, other):
        # docstring inherited.
        super().update_from(other)
        # For some properties we don't need or don't want to go through the
        # getters/setters, so we just copy them directly.
        self._edgecolor = other._edgecolor
        self._facecolor = other._facecolor
        self._original_edgecolor = other._original_edgecolor
        self._original_facecolor = other._original_facecolor
        self._fill = other._fill
        self._hatch = other._hatch
        self._hatch_color = other._hatch_color
        self._unscaled_dash_pattern = other._unscaled_dash_pattern
        self.set_linewidth(other._linewidth)  # also sets scaled dashes
        self.set_transform(other.get_data_transform())
        # If the transform of other needs further initialization, then it will
        # be the case for this artist too.
        self._transformSet = other.is_transform_set()
