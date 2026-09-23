    def _combine_series(self, other, func, fill_value=None, axis=None,
                        level=None, try_cast=True):
        if axis is not None:
            axis = self._get_axis_name(axis)
            if axis == 'index':
                return self._combine_match_index(other, func, level=level,
                                                 fill_value=fill_value,
                                                 try_cast=try_cast)
            else:
                return self._combine_match_columns(other, func, level=level,
                                                   fill_value=fill_value,
                                                   try_cast=try_cast)
        return self._combine_series_infer(other, func, level=level,
                                          fill_value=fill_value,
                                          try_cast=try_cast)
