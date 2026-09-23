    def __init__(self, objs, axis=0, join='outer', join_axes=None,
                 keys=None, levels=None, names=None,
                 ignore_index=False, verify_integrity=False, copy=True):
        if isinstance(objs, (NDFrame, compat.string_types)):
            raise TypeError('first argument must be an iterable of pandas '
                            'objects, you passed an object of type '
                            '"{0}"'.format(type(objs).__name__))

        if join == 'outer':
            self.intersect = False
        elif join == 'inner':
            self.intersect = True
        else:  # pragma: no cover
            raise ValueError('Only can inner (intersect) or outer (union) '
                             'join the other axis')

        if isinstance(objs, dict):
            if keys is None:
                keys = sorted(objs)
            objs = [objs[k] for k in keys]
        else:
            objs = list(objs)

        if len(objs) == 0:
            raise ValueError('No objects to concatenate')

        if keys is None:
            objs = [obj for obj in objs if obj is not None]
        else:
            # #1649
            clean_keys = []
            clean_objs = []
            for k, v in zip(keys, objs):
                if v is None:
                    continue
                clean_keys.append(k)
                clean_objs.append(v)
            objs = clean_objs
            name = getattr(keys, 'name', None)
            keys = Index(clean_keys, name=name)

        if len(objs) == 0:
            raise ValueError('All objects passed were None')

        # consolidate data & figure out what our result ndim is going to be
        ndims = set()
        for obj in objs:
            if not isinstance(obj, NDFrame):
                raise TypeError("cannot concatenate a non-NDFrame object")

            # consolidate
            obj._consolidate(inplace=True)
            ndims.add(obj.ndim)

        # get the sample
        # want the higest ndim that we have, and must be non-empty
        # unless all objs are empty
        sample = None
        if len(ndims) > 1:
            max_ndim = max(ndims)
            for obj in objs:
                if obj.ndim == max_ndim and np.sum(obj.shape):
                    sample = obj
                    break

        else:
            # filter out the empties if we have not multi-index possibilities
            # note to keep empty Series as it affect to result columns / name
            non_empties = [obj for obj in objs
                           if sum(obj.shape) > 0 or isinstance(obj, Series)]

            if (len(non_empties) and (keys is None and names is None and
                                      levels is None and
                                      join_axes is None and
                                      not self.intersect)):
                objs = non_empties
                sample = objs[0]

        if sample is None:
            sample = objs[0]
        self.objs = objs

        # Standardize axis parameter to int
        if isinstance(sample, Series):
            axis = DataFrame()._get_axis_number(axis)
        else:
            axis = sample._get_axis_number(axis)

        # Need to flip BlockManager axis in the DataFrame special case
        self._is_frame = isinstance(sample, DataFrame)
        if self._is_frame:
            axis = 1 if axis == 0 else 0

        self._is_series = isinstance(sample, Series)
        if not 0 <= axis <= sample.ndim:
            raise AssertionError("axis must be between 0 and {0}, "
                                 "input was {1}".format(sample.ndim, axis))

        # if we have mixed ndims, then convert to highest ndim
        # creating column numbers as needed
        if len(ndims) > 1:
            current_column = 0
            max_ndim = sample.ndim
            self.objs, objs = [], self.objs
            for obj in objs:

                ndim = obj.ndim
                if ndim == max_ndim:
                    pass

                elif ndim != max_ndim - 1:
                    raise ValueError("cannot concatenate unaligned mixed "
                                     "dimensional NDFrame objects")

                else:
                    name = getattr(obj, 'name', None)
                    if ignore_index or name is None:
                        name = current_column
                        current_column += 1

                    # doing a row-wise concatenation so need everything
                    # to line up
                    if self._is_frame and axis == 1:
                        name = 0
                    obj = sample._constructor({name: obj})

                self.objs.append(obj)

        # note: this is the BlockManager axis (since DataFrame is transposed)
        self.axis = axis
        self.join_axes = join_axes
        self.keys = keys
        self.names = names or getattr(keys, 'names', None)
        self.levels = levels

        self.ignore_index = ignore_index
        self.verify_integrity = verify_integrity
        self.copy = copy

        self.new_axes = self._get_new_axes()
