    @Appender(_shared_docs['transpose'] % _shared_doc_kwargs)
    def transpose(self, *args, **kwargs):

        # construct the args
        axes, kwargs = self._construct_axes_from_arguments(
            args, kwargs, require_all=True)
        axes_names = tuple([self._get_axis_name(axes[a])
                            for a in self._AXIS_ORDERS])
        axes_numbers = tuple([self._get_axis_number(axes[a])
                             for a in self._AXIS_ORDERS])

        # we must have unique axes
        if len(axes) != len(set(axes)):
            raise ValueError('Must specify %s unique axes' % self._AXIS_LEN)

        new_axes = self._construct_axes_dict_from(
            self, [self._get_axis(x) for x in axes_names])
        new_values = self.values.transpose(axes_numbers)
        if kwargs.pop('copy', None) or (len(args) and args[-1]):
            new_values = new_values.copy()

        if kwargs:
            raise TypeError('transpose() got an unexpected keyword '
                    'argument "{0}"'.format(list(kwargs.keys())[0]))

        return self._constructor(new_values, **new_axes).__finalize__(self)
