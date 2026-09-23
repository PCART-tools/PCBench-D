    @staticmethod
    def from_extents(*args):
        """
        Create a new Bbox from *left*, *bottom*, *right* and *top*.

        The *y*-axis increases upwards.
        """
        return Bbox(np.reshape(args, (2, 2)))
