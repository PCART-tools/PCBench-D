    def iset(
        self, loc: int | slice | np.ndarray, value: ArrayLike, inplace: bool = False
    ) -> None:
        """
        Set new column(s).

        This changes the ArrayManager in-place, but replaces (an) existing
        column(s), not changing column values in-place).

        Parameters
        ----------
        loc : integer, slice or boolean mask
            Positional location (already bounds checked)
        value : np.ndarray or ExtensionArray
        inplace : bool, default False
            Whether overwrite existing array as opposed to replacing it.
        """
        # single column -> single integer index
        if lib.is_integer(loc):
            # TODO can we avoid needing to unpack this here? That means converting
            # DataFrame into 1D array when loc is an integer
            if isinstance(value, np.ndarray) and value.ndim == 2:
                assert value.shape[1] == 1
                value = value[:, 0]

            # TODO we receive a datetime/timedelta64 ndarray from DataFrame._iset_item
            # but we should avoid that and pass directly the proper array
            value = maybe_coerce_values(value)

            assert isinstance(value, (np.ndarray, ExtensionArray))
            assert value.ndim == 1
            assert len(value) == len(self._axes[0])
            self.arrays[loc] = value
            return

        # multiple columns -> convert slice or array to integer indices
        elif isinstance(loc, slice):
            indices = range(
                loc.start if loc.start is not None else 0,
                loc.stop if loc.stop is not None else self.shape_proper[1],
                loc.step if loc.step is not None else 1,
            )
        else:
            assert isinstance(loc, np.ndarray)
            assert loc.dtype == "bool"
            # error: Incompatible types in assignment (expression has type "ndarray",
            # variable has type "range")
            indices = np.nonzero(loc)[0]  # type: ignore[assignment]

        assert value.ndim == 2
        assert value.shape[0] == len(self._axes[0])

        for value_idx, mgr_idx in enumerate(indices):
            # error: No overload variant of "__getitem__" of "ExtensionArray" matches
            # argument type "Tuple[slice, int]"
            value_arr = value[:, value_idx]  # type: ignore[call-overload]
            self.arrays[mgr_idx] = value_arr
        return
