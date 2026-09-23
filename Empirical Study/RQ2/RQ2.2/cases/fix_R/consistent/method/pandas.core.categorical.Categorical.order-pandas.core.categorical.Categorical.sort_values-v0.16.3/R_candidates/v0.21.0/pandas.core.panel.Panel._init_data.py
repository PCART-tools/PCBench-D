    def _init_data(self, data, copy, dtype, **kwargs):
        """
        Generate ND initialization; axes are passed
        as required objects to __init__
        """
        if data is None:
            data = {}
        if dtype is not None:
            dtype = self._validate_dtype(dtype)

        passed_axes = [kwargs.pop(a, None) for a in self._AXIS_ORDERS]

        if kwargs:
            raise TypeError('_init_data() got an unexpected keyword '
                            'argument "{0}"'.format(list(kwargs.keys())[0]))

        axes = None
        if isinstance(data, BlockManager):
            if _any_not_none(*passed_axes):
                axes = [x if x is not None else y
                        for x, y in zip(passed_axes, data.axes)]
            mgr = data
        elif isinstance(data, dict):
            mgr = self._init_dict(data, passed_axes, dtype=dtype)
            copy = False
            dtype = None
        elif isinstance(data, (np.ndarray, list)):
            mgr = self._init_matrix(data, passed_axes, dtype=dtype, copy=copy)
            copy = False
            dtype = None
        elif is_scalar(data) and _all_not_none(*passed_axes):
            values = cast_scalar_to_array([len(x) for x in passed_axes],
                                          data, dtype=dtype)
            mgr = self._init_matrix(values, passed_axes, dtype=values.dtype,
                                    copy=False)
            copy = False
        else:  # pragma: no cover
            raise ValueError('Panel constructor not properly called!')

        NDFrame.__init__(self, mgr, axes=axes, copy=copy, dtype=dtype)
