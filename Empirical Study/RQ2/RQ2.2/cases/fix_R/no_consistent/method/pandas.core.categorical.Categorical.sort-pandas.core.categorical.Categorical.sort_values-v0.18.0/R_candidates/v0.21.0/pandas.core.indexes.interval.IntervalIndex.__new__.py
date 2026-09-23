    def __new__(cls, data, closed='right',
                name=None, copy=False, dtype=None,
                fastpath=False, verify_integrity=True):

        if fastpath:
            return cls._simple_new(data.left, data.right, closed, name,
                                   copy=copy, verify_integrity=False)

        if name is None and hasattr(data, 'name'):
            name = data.name

        if isinstance(data, IntervalIndex):
            left = data.left
            right = data.right

        else:

            # don't allow scalars
            if is_scalar(data):
                cls._scalar_data_error(data)

            data = IntervalIndex.from_intervals(data, name=name)
            left, right = data.left, data.right

        return cls._simple_new(left, right, closed, name,
                               copy=copy, verify_integrity=verify_integrity)
