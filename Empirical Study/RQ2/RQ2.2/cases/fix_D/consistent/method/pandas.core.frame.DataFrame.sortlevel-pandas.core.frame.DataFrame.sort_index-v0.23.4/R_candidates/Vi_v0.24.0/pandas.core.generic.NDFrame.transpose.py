    def transpose(self, *args, **kwargs):
        """
        Permute the dimensions of the %(klass)s

        Parameters
        ----------
        args : %(args_transpose)s
        copy : boolean, default False
            Make a copy of the underlying data. Mixed-dtype data will
            always result in a copy

        Returns
        -------
        y : same as input

        Examples
        --------
        >>> p.transpose(2, 0, 1)
        >>> p.transpose(2, 0, 1, copy=True)
        """

        # construct the args
        axes, kwargs = self._construct_axes_from_arguments(args, kwargs,
                                                           require_all=True)
        axes_names = tuple(self._get_axis_name(axes[a])
                           for a in self._AXIS_ORDERS)
        axes_numbers = tuple(self._get_axis_number(axes[a])
                             for a in self._AXIS_ORDERS)

        # we must have unique axes
        if len(axes) != len(set(axes)):
            raise ValueError('Must specify %s unique axes' % self._AXIS_LEN)

        new_axes = self._construct_axes_dict_from(self, [self._get_axis(x)
                                                         for x in axes_names])
        new_values = self.values.transpose(axes_numbers)
        if kwargs.pop('copy', None) or (len(args) and args[-1]):
            new_values = new_values.copy()

        nv.validate_transpose_for_generic(self, kwargs)
        return self._constructor(new_values, **new_axes).__finalize__(self)
