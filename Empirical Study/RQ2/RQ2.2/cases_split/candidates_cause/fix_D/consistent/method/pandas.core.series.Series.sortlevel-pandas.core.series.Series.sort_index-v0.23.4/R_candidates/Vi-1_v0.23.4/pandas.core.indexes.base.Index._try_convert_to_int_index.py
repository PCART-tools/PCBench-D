    @classmethod
    def _try_convert_to_int_index(cls, data, copy, name, dtype):
        """
        Attempt to convert an array of data into an integer index.

        Parameters
        ----------
        data : The data to convert.
        copy : Whether to copy the data or not.
        name : The name of the index returned.

        Returns
        -------
        int_index : data converted to either an Int64Index or a
                    UInt64Index

        Raises
        ------
        ValueError if the conversion was not successful.
        """

        from .numeric import Int64Index, UInt64Index
        if not is_unsigned_integer_dtype(dtype):
            # skip int64 conversion attempt if uint-like dtype is passed, as
            # this could return Int64Index when UInt64Index is what's desrired
            try:
                res = data.astype('i8', copy=False)
                if (res == data).all():
                    return Int64Index(res, copy=copy, name=name)
            except (OverflowError, TypeError, ValueError):
                pass

        # Conversion to int64 failed (possibly due to overflow) or was skipped,
        # so let's try now with uint64.
        try:
            res = data.astype('u8', copy=False)
            if (res == data).all():
                return UInt64Index(res, copy=copy, name=name)
        except (OverflowError, TypeError, ValueError):
            pass

        raise ValueError
