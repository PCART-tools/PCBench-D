    def _setitem_frame(self, key, value):
        # support boolean setting with DataFrame input, e.g.
        # df[df > df2] = 0
        if key.values.dtype != np.bool_:
            raise TypeError('Must pass DataFrame with boolean values only')

        if self._is_mixed_type:
            if not self._is_numeric_mixed_type:
                raise TypeError(
                    'Cannot do boolean setting on mixed-type frame')

        self.where(-key, value, inplace=True)
