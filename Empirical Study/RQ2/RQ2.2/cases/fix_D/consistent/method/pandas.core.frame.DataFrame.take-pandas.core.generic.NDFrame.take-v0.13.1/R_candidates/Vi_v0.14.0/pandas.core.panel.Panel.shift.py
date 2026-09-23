    @deprecate_kwarg(old_arg_name='lags', new_arg_name='periods')
    def shift(self, periods=1, freq=None, axis='major'):
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
        if freq:
            return self.tshift(periods, freq, axis=axis)

        if axis == 'items':
            raise ValueError('Invalid axis')

        return super(Panel, self).slice_shift(periods, axis=axis)
