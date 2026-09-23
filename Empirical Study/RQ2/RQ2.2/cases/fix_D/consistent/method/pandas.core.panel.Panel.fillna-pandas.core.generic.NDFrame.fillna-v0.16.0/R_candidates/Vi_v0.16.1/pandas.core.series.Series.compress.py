    def compress(self, condition, axis=0, out=None, **kwargs):
        """
        Return selected slices of an array along given axis as a Series

        See also
        --------
        numpy.ndarray.compress
        """
        return self[condition]
