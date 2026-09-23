    def item(self):
        """
        Return the first element of the underlying data as a python scalar.

        Returns
        -------
        scalar
            The first element of %(klass)s.

        Raises
        ------
        ValueError
            If the data is not length-1.
        """
        if not (
            is_extension_array_dtype(self.dtype) or needs_i8_conversion(self.dtype)
        ):
            # numpy returns ints instead of datetime64/timedelta64 objects,
            #  which we need to wrap in Timestamp/Timedelta/Period regardless.
            return self.values.item()

        if len(self) == 1:
            return next(iter(self))
        else:
            raise ValueError("can only convert an array of size 1 to a Python scalar")
