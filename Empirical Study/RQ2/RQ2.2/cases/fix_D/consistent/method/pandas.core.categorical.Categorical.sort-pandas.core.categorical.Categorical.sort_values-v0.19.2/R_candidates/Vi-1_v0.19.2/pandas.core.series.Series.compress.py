    def compress(self, condition, *args, **kwargs):
        """
        Return selected slices of an array along given axis as a Series

        See also
        --------
        numpy.ndarray.compress
        """
        nv.validate_compress(args, kwargs)
        return self[condition]
