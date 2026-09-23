    def _get_offsets_buffer(self) -> tuple[PandasBuffer, Any]:
        """
        Return the buffer containing the offset values for variable-size binary
        data (e.g., variable-length strings) and the buffer's associated dtype.
        Raises NoBufferPresent if the data buffer does not have an associated
        offsets buffer.
        """
        if self.dtype[0] == DtypeKind.STRING:
            # For each string, we need to manually determine the next offset
            values = self._col.to_numpy()
            ptr = 0
            offsets = np.zeros(shape=(len(values) + 1,), dtype=np.int64)
            for i, v in enumerate(values):
                # For missing values (in this case, `np.nan` values)
                # we don't increment the pointer
                if isinstance(v, str):
                    b = v.encode(encoding="utf-8")
                    ptr += len(b)

                offsets[i + 1] = ptr

            # Convert the offsets to a Pandas "buffer" using
            # the NumPy array as the backing store
            buffer = PandasBuffer(offsets)

            # Assemble the buffer dtype info
            dtype = (
                DtypeKind.INT,
                64,
                ArrowCTypes.INT64,
                Endianness.NATIVE,
            )  # note: currently only support native endianness
        else:
            raise NoBufferPresent(
                "This column has a fixed-length dtype so "
                "it does not have an offsets buffer"
            )

        return buffer, dtype
