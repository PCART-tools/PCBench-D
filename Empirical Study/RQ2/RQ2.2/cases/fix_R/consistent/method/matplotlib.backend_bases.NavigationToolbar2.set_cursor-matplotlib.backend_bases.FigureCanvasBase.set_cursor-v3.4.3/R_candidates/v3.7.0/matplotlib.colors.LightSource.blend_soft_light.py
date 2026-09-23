    def blend_soft_light(self, rgb, intensity):
        """
        Combine an RGB image with an intensity map using "soft light" blending,
        using the "pegtop" formula.

        Parameters
        ----------
        rgb : `~numpy.ndarray`
            An MxNx3 RGB array of floats ranging from 0 to 1 (color image).
        intensity : `~numpy.ndarray`
            An MxNx1 array of floats ranging from 0 to 1 (grayscale image).

        Returns
        -------
        `~numpy.ndarray`
            An MxNx3 RGB array representing the combined images.
        """
        return 2 * intensity * rgb + (1 - 2 * intensity) * rgb**2
