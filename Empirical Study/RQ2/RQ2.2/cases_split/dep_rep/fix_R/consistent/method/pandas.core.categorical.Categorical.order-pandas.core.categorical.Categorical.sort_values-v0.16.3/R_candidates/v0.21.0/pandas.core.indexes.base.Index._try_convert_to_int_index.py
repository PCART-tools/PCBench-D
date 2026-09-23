    @classmethod
    def _try_convert_to_int_index(cls, data, copy, name):
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
        try:
            res = data.astype('i8', copy=False)
            if (res == data).all():
                return Int64Index(res, copy=copy, name=name)
        except (OverflowError, TypeError, ValueError):
            pass

        # Conversion to int64 failed (possibly due to
        # overflow), so let's try now with uint64.
        try:
            res = data.astype('u8', copy=False)
            if (res == data).all():
                return UInt64Index(res, copy=copy, name=name)
        except (OverflowError, TypeError, ValueError):
            pass

        raise ValueError
