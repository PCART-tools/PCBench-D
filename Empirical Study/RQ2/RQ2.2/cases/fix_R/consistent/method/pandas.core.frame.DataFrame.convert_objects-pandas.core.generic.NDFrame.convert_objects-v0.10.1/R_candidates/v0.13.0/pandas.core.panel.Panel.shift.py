    def shift(self, lags, freq=None, axis='major'):
        """
        Shift major or minor axis by specified number of leads/lags. Drops
        periods right now compared with DataFrame.shift

        Parameters
        ----------
        lags : int
        axis : {'major', 'minor'}

        Returns
        -------
        shifted : Panel
        """
        values = self.values
        items = self.items
        major_axis = self.major_axis
        minor_axis = self.minor_axis

        if freq:
            return self.tshift(lags, freq, axis=axis)

        if lags > 0:
            vslicer = slice(None, -lags)
            islicer = slice(lags, None)
        elif lags == 0:
            vslicer = islicer = slice(None)
        else:
            vslicer = slice(-lags, None)
            islicer = slice(None, lags)

        axis = self._get_axis_name(axis)
        if axis == 'major_axis':
            values = values[:, vslicer, :]
            major_axis = major_axis[islicer]
        elif axis == 'minor_axis':
            values = values[:, :, vslicer]
            minor_axis = minor_axis[islicer]
        else:
            raise ValueError('Invalid axis')

        return self._constructor(values, items=items, major_axis=major_axis,
                                 minor_axis=minor_axis)
