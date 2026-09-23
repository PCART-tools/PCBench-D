    def get_children(self):
        # docstring inherited.
        return [
            *self._children,
            *self.spines.values(),
            *self._axis_map.values(),
            self.title, self._left_title, self._right_title,
            *self.child_axes,
            *([self.legend_] if self.legend_ is not None else []),
            self.patch,
        ]
