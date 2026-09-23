    @doc(ExtensionArray.factorize)
    def factorize(
        self,
        na_sentinel: int | lib.NoDefault = lib.no_default,
        use_na_sentinel: bool | lib.NoDefault = lib.no_default,
    ) -> tuple[np.ndarray, ExtensionArray]:
        resolved_na_sentinel = algos.resolve_na_sentinel(na_sentinel, use_na_sentinel)
        arr = self._data
        mask = self._mask

        # Pass non-None na_sentinel; recode and add NA to uniques if necessary below
        na_sentinel_arg = -1 if resolved_na_sentinel is None else resolved_na_sentinel
        codes, uniques = factorize_array(arr, na_sentinel=na_sentinel_arg, mask=mask)

        # check that factorize_array correctly preserves dtype.
        assert uniques.dtype == self.dtype.numpy_dtype, (uniques.dtype, self.dtype)

        has_na = mask.any()
        if resolved_na_sentinel is not None or not has_na:
            size = len(uniques)
        else:
            # Make room for an NA value
            size = len(uniques) + 1
        uniques_mask = np.zeros(size, dtype=bool)
        if resolved_na_sentinel is None and has_na:
            na_index = mask.argmax()
            # Insert na with the proper code
            if na_index == 0:
                na_code = np.intp(0)
            else:
                # mypy error: Slice index must be an integer or None
                # https://github.com/python/mypy/issues/2410
                na_code = codes[:na_index].argmax() + 1  # type: ignore[misc]
            codes[codes >= na_code] += 1
            codes[codes == -1] = na_code
            # dummy value for uniques; not used since uniques_mask will be True
            uniques = np.insert(uniques, na_code, 0)
            uniques_mask[na_code] = True
        uniques_ea = type(self)(uniques, uniques_mask)

        return codes, uniques_ea
