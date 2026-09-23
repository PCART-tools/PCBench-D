    def transform_point(self, point):
        """
        A convenience function that returns the transformed copy of a
        single point.

        The point is given as a sequence of length :attr:`input_dims`.
        The transformed point is returned as a sequence of length
        :attr:`output_dims`.
        """
        if len(point) != self.input_dims:
            raise ValueError("The length of 'point' must be 'self.input_dims'")
        return self.transform(np.asarray([point]))[0]
