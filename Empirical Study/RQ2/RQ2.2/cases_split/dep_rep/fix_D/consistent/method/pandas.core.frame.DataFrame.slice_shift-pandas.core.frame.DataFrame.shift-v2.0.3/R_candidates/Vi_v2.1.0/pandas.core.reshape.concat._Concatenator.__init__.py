    def __init__(
        self,
        objs: Iterable[Series | DataFrame] | Mapping[HashableT, Series | DataFrame],
        axis: Axis = 0,
        join: str = "outer",
        keys=None,
        levels=None,
        names: list[HashableT] | None = None,
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

        if not is_bool(sort):
            raise ValueError(
                f"The 'sort' keyword only accepts boolean values; {sort} was passed."
            )
        # Incompatible types in assignment (expression has type "Union[bool, bool_]",
        # variable has type "bool")
        self.sort = sort  # type: ignore[assignment]

        self.ignore_index = ignore_index
        self.verify_integrity = verify_integrity
        self.copy = copy

        objs, keys = self._clean_keys_and_objs(objs, keys)

        # figure out what our result ndim is going to be
        ndims = self._get_ndims(objs)
        sample, objs = self._get_sample_object(objs, ndims, keys, names, levels)

        # Standardize axis parameter to int
        if sample.ndim == 1:
            from pandas import DataFrame

            axis = DataFrame._get_axis_number(axis)
            self._is_frame = False
            self._is_series = True
        else:
            axis = sample._get_axis_number(axis)
            self._is_frame = True
            self._is_series = False

            # Need to flip BlockManager axis in the DataFrame special case
            axis = sample._get_block_manager_axis(axis)

        # if we have mixed ndims, then convert to highest ndim
        # creating column numbers as needed
        if len(ndims) > 1:
            objs, sample = self._sanitize_mixed_ndim(objs, sample, ignore_index, axis)

        self.objs = objs

        # note: this is the BlockManager axis (since DataFrame is transposed)
        self.bm_axis = axis
        self.axis = 1 - self.bm_axis if self._is_frame else 0
        self.keys = keys
        self.names = names or getattr(keys, "names", None)
        self.levels = levels
