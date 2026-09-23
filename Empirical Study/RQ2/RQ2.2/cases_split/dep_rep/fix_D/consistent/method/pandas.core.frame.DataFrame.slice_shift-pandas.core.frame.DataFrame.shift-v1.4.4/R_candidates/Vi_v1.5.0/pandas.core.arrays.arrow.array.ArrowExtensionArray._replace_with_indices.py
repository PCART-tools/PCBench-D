    @classmethod
    def _replace_with_indices(
        cls,
        chunk: pa.Array,
        indices: npt.NDArray[np.intp],
        value: npt.NDArray[Any],
    ) -> pa.Array:
        """
        Replace items selected with a set of positional indices.

        Analogous to pyarrow.compute.replace_with_mask, except that replacement
        positions are identified via indices rather than a mask.

        Parameters
        ----------
        chunk : pa.Array
        indices : npt.NDArray[np.intp]
        value : npt.NDArray[Any]
            Replacement value(s).

        Returns
        -------
        pa.Array
        """
        n = len(indices)

        if n == 0:
            return chunk

        start, stop = indices[[0, -1]]

        if (stop - start) == (n - 1):
            # fast path for a contiguous set of indices
            arrays = [
                chunk[:start],
                pa.array(value, type=chunk.type, from_pandas=True),
                chunk[stop + 1 :],
            ]
            arrays = [arr for arr in arrays if len(arr)]
            if len(arrays) == 1:
                return arrays[0]
            return pa.concat_arrays(arrays)

        mask = np.zeros(len(chunk), dtype=np.bool_)
        mask[indices] = True

        if pa_version_under5p0:
            arr = chunk.to_numpy(zero_copy_only=False)
            arr[mask] = value
            return pa.array(arr, type=chunk.type)

        if isna(value).all():
            return pc.if_else(mask, None, chunk)

        return pc.replace_with_mask(chunk, mask, value)
