    def __init__(
        self,
        objs: Iterable[NDFrame] | Mapping[HashableT, NDFrame],
        axis: Axis = 0,
        join: str = "outer",
        keys=None,
        levels=None,
        names=None,
        ignore_index: bool = False,
        verify_integrity: bool = False,
        copy: bool = True,
        sort: bool = False,
    ) -> None:
        if isinstance(objs, (ABCSeries, ABCDataFrame, str)):
            raise TypeError(
                "first argument must be an iterable of pandas "
                f'objects, you passed an object of type "{type(objs).__name__}"'
            )

        if join == "outer":
            self.intersect = False
        elif join == "inner":
            self.intersect = True
        else:  # pragma: no cover
            raise ValueError(
                "Only can inner (intersect) or outer (union) join the other axis"
            )

        if isinstance(objs, abc.Mapping):
            if keys is None:
                keys = list(objs.keys())
            objs = [objs[k] for k in keys]
        else:
            objs = list(objs)

        if len(objs) == 0:
            raise ValueError("No objects to concatenate")

        if keys is None:
            objs = list(com.not_none(*objs))
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

            if isinstance(keys, MultiIndex):
                # TODO: retain levels?
                keys = type(keys).from_tuples(clean_keys, names=keys.names)
            else:
                name = getattr(keys, "name", None)
                keys = Index(clean_keys, name=name, dtype=getattr(keys, "dtype", None))

        if len(objs) == 0:
            raise ValueError("All objects passed were None")

        # figure out what our result ndim is going to be
        ndims = set()
        for obj in objs:
            if not isinstance(obj, (ABCSeries, ABCDataFrame)):
                msg = (
                    f"cannot concatenate object of type '{type(obj)}'; "
                    "only Series and DataFrame objs are valid"
                )
                raise TypeError(msg)

            ndims.add(obj.ndim)

        # get the sample
        # want the highest ndim that we have, and must be non-empty
        # unless all objs are empty
        sample: NDFrame | None = None
        if len(ndims) > 1:
            max_ndim = max(ndims)
            for obj in objs:
                if obj.ndim == max_ndim and np.sum(obj.shape):
                    sample = obj
                    break

        else:
            # filter out the empties if we have not multi-index possibilities
            # note to keep empty Series as it affect to result columns / name
            non_empties = [
                obj for obj in objs if sum(obj.shape) > 0 or isinstance(obj, ABCSeries)
            ]

            if len(non_empties) and (
                keys is None and names is None and levels is None and not self.intersect
            ):
                objs = non_empties
                sample = objs[0]

        if sample is None:
            sample = objs[0]
        self.objs = objs

        # Standardize axis parameter to int
        if isinstance(sample, ABCSeries):
            from pandas import DataFrame

            axis = DataFrame._get_axis_number(axis)
        else:
            axis = sample._get_axis_number(axis)

        # Need to flip BlockManager axis in the DataFrame special case
        self._is_frame = isinstance(sample, ABCDataFrame)
        if self._is_frame:
            axis = sample._get_block_manager_axis(axis)

        self._is_series = isinstance(sample, ABCSeries)
        if not 0 <= axis <= sample.ndim:
            raise AssertionError(
                f"axis must be between 0 and {sample.ndim}, input was {axis}"
            )

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
                    raise ValueError(
                        "cannot concatenate unaligned mixed "
                        "dimensional NDFrame objects"
                    )

                else:
                    name = getattr(obj, "name", None)
                    if ignore_index or name is None:
                        name = current_column
                        current_column += 1

                    # doing a row-wise concatenation so need everything
                    # to line up
                    if self._is_frame and axis == 1:
                        name = 0
                    # mypy needs to know sample is not an NDFrame
                    sample = cast("DataFrame | Series", sample)
                    obj = sample._constructor({name: obj}, copy=False)

                self.objs.append(obj)

        # note: this is the BlockManager axis (since DataFrame is transposed)
        self.bm_axis = axis
        self.axis = 1 - self.bm_axis if self._is_frame else 0
        self.keys = keys
        self.names = names or getattr(keys, "names", None)
        self.levels = levels

        if not is_bool(sort):
            raise ValueError(
                f"The 'sort' keyword only accepts boolean values; {sort} was passed."
            )
        self.sort = sort

        self.ignore_index = ignore_index
        self.verify_integrity = verify_integrity
        self.copy = copy

        self.new_axes = self._get_new_axes()
