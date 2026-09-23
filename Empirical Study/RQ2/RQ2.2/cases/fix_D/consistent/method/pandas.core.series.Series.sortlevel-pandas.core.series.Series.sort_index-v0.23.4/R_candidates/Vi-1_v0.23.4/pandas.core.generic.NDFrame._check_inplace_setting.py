    def _check_inplace_setting(self, value):
        """ check whether we allow in-place setting with this type of value """

        if self._is_mixed_type:
            if not self._is_numeric_mixed_type:

                # allow an actual np.nan thru
                try:
                    if np.isnan(value):
                        return True
                except Exception:
                    pass

                raise TypeError('Cannot do inplace boolean setting on '
                                'mixed-types with a non np.nan value')

        return True
