    def _init_data(self, data, copy, dtype, **kwargs):
        """
        Generate ND initialization; axes are passed
        as required objects to __init__
        """
        if data is None:
            data = {}
        if dtype is not None:
            dtype = self._validate_dtype(dtype)

        passed_axes = [kwargs.get(a) for a in self._AXIS_ORDERS]
        axes = None
        if isinstance(data, BlockManager):
            if any(x is not None for x in passed_axes):
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
        else:  # pragma: no cover
            raise PandasError('Panel constructor not properly called!')

        NDFrame.__init__(self, mgr, axes=axes, copy=copy, dtype=dtype)
