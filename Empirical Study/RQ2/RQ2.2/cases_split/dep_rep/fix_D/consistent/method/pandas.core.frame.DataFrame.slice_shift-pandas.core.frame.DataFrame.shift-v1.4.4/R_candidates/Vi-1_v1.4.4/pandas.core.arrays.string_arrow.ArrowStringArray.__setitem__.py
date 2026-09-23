    def __setitem__(self, key: int | slice | np.ndarray, value: Any) -> None:
        """Set one or more values inplace.

        Parameters
        ----------
        key : int, ndarray, or slice
            When called from, e.g. ``Series.__setitem__``, ``key`` will be
            one of

            * scalar int
            * ndarray of integers.
            * boolean ndarray
            * slice object

        value : ExtensionDtype.type, Sequence[ExtensionDtype.type], or object
            value or values to be set of ``key``.

        Returns
        -------
        None
        """
        key = check_array_indexer(self, key)

        if is_integer(key):
            key = cast(int, key)

            if not is_scalar(value):
                raise ValueError("Must pass scalars with scalar indexer")
            elif isna(value):
                value = None
            elif not isinstance(value, str):
                raise ValueError("Scalar must be NA or str")

            # Slice data and insert in-between
            new_data = [
                *self._data[0:key].chunks,
                pa.array([value], type=pa.string()),
                *self._data[(key + 1) :].chunks,
            ]
            self._data = pa.chunked_array(new_data)
        else:
            # Convert to integer indices and iteratively assign.
            # TODO: Make a faster variant of this in Arrow upstream.
            #       This is probably extremely slow.

            # Convert all possible input key types to an array of integers
            if isinstance(key, slice):
                key_array = np.array(range(len(self))[key])
            elif is_bool_dtype(key):
                # TODO(ARROW-9430): Directly support setitem(booleans)
                key_array = np.argwhere(key).flatten()
            else:
                # TODO(ARROW-9431): Directly support setitem(integers)
                key_array = np.asanyarray(key)

            if is_scalar(value):
                value = np.broadcast_to(value, len(key_array))
            else:
                value = np.asarray(value)

            if len(key_array) != len(value):
                raise ValueError("Length of indexer and values mismatch")

            for k, v in zip(key_array, value):
                self[k] = v
