    def fast_xs(self, loc: int) -> SingleBlockManager:
        """
        Return the array corresponding to `frame.iloc[loc]`.

        Parameters
        ----------
        loc : int

        Returns
        -------
        np.ndarray or ExtensionArray
        """
        if len(self.blocks) == 1:
            result = self.blocks[0].iget((slice(None), loc))
            block = new_block(result, placement=slice(0, len(result)), ndim=1)
            # in the case of a single block, the new block is a view
            ref = weakref.ref(self.blocks[0])
            return SingleBlockManager(block, self.axes[0], [ref])

        dtype = interleaved_dtype([blk.dtype for blk in self.blocks])

        n = len(self)

        # GH#46406
        immutable_ea = isinstance(dtype, SparseDtype)

        if isinstance(dtype, ExtensionDtype) and not immutable_ea:
            cls = dtype.construct_array_type()
            result = cls._empty((n,), dtype=dtype)
        else:
            # error: Argument "dtype" to "empty" has incompatible type
            # "Union[Type[object], dtype[Any], ExtensionDtype, None]"; expected
            # "None"
            result = np.empty(
                n, dtype=object if immutable_ea else dtype  # type: ignore[arg-type]
            )
            result = ensure_wrapped_if_datetimelike(result)

        for blk in self.blocks:
            # Such assignment may incorrectly coerce NaT to None
            # result[blk.mgr_locs] = blk._slice((slice(None), loc))
            for i, rl in enumerate(blk.mgr_locs):
                result[rl] = blk.iget((i, loc))

        if immutable_ea:
            dtype = cast(ExtensionDtype, dtype)
            result = dtype.construct_array_type()._from_sequence(result, dtype=dtype)

        block = new_block(result, placement=slice(0, len(result)), ndim=1)
        return SingleBlockManager(block, self.axes[0])
