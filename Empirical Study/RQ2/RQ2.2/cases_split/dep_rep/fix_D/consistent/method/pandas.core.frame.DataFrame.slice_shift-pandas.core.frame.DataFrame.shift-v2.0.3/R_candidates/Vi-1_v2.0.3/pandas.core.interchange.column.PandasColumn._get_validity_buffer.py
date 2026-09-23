    def _get_validity_buffer(self) -> tuple[PandasBuffer, Any]:
        """
        Return the buffer containing the mask values indicating missing data and
        the buffer's associated dtype.
        Raises NoBufferPresent if null representation is not a bit or byte mask.
        """
        null, invalid = self.describe_null

        if self.dtype[0] == DtypeKind.STRING:
            # For now, use byte array as the mask.
            # TODO: maybe store as bit array to save space?..
            buf = self._col.to_numpy()

            # Determine the encoding for valid values
            valid = invalid == 0
            invalid = not valid

            mask = np.zeros(shape=(len(buf),), dtype=np.bool_)
            for i, obj in enumerate(buf):
                mask[i] = valid if isinstance(obj, str) else invalid

            # Convert the mask array to a Pandas "buffer" using
            # a NumPy array as the backing store
            buffer = PandasBuffer(mask)

            # Define the dtype of the returned buffer
            dtype = (DtypeKind.BOOL, 8, ArrowCTypes.BOOL, Endianness.NATIVE)

            return buffer, dtype

        try:
            msg = f"{_NO_VALIDITY_BUFFER[null]} so does not have a separate mask"
        except KeyError:
            # TODO: implement for other bit/byte masks?
            raise NotImplementedError("See self.describe_null")

        raise NoBufferPresent(msg)
