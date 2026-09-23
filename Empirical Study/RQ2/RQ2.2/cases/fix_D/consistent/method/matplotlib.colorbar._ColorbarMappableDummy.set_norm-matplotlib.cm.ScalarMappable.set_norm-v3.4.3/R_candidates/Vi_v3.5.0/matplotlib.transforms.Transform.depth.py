    @property
    def depth(self):
        """
        Return the number of transforms which have been chained
        together to form this Transform instance.

        .. note::

            For the special case of a Composite transform, the maximum depth
            of the two is returned.

        """
        return 1
