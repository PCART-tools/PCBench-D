    def _set_via_chunk_iteration(
        self, indices: npt.NDArray[np.intp], value: npt.NDArray[Any]
    ) -> pa.ChunkedArray:
        """
        Loop through the array chunks and set the new values while
        leaving the chunking layout unchanged.

        Parameters
        ----------
        indices : npt.NDArray[np.intp]
            Position indices for the underlying ChunkedArray.

        value : ExtensionDtype.type, Sequence[ExtensionDtype.type], or object
            value or values to be set of ``key``.

        Notes
        -----
        Assumes that indices is sorted. Caller is responsible for sorting.
        """
        new_data = []
        stop = 0
        for chunk in self._data.iterchunks():
            start, stop = stop, stop + len(chunk)
            if len(indices) == 0 or stop <= indices[0]:
                new_data.append(chunk)
            else:
                n = int(np.searchsorted(indices, stop, side="left"))
                c_ind = indices[:n] - start
                indices = indices[n:]
                n = len(c_ind)
                c_value, value = value[:n], value[n:]
                new_data.append(self._replace_with_indices(chunk, c_ind, c_value))
        return pa.chunked_array(new_data)
