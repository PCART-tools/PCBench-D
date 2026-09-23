    def reshape(self, new_shape, *args, **kwargs):
        """
        DEPRECATED: calling this method will raise an error in a
        future release.

        An ndarray-compatible method that returns `self` because
        `Categorical` instances cannot actually be reshaped.

        Parameters
        ----------
        new_shape : int or tuple of ints
            A 1-D array of integers that correspond to the new
            shape of the `Categorical`. For more information on
            the parameter, please refer to `np.reshape`.
        """
        warn("reshape is deprecated and will raise "
             "in a subsequent release", FutureWarning, stacklevel=2)

        nv.validate_reshape(args, kwargs)

        # while the 'new_shape' parameter has no effect,
        # we should still enforce valid shape parameters
        np.reshape(self.codes, new_shape)

        return self
