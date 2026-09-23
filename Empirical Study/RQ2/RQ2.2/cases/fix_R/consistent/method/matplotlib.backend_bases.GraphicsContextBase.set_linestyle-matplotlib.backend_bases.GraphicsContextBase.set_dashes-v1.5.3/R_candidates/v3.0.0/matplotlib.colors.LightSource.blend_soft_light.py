    def blend_soft_light(self, rgb, intensity):
        """
        Combines an rgb image with an intensity map using "soft light"
        blending.  Uses the "pegtop" formula.

        Parameters
        ----------
        rgb : ndarray
            An MxNx3 RGB array of floats ranging from 0 to 1 (color image).
        intensity : ndarray
            An MxNx1 array of floats ranging from 0 to 1 (grayscale image).

        Returns
        -------
        rgb : ndarray
            An MxNx3 RGB array representing the combined images.
        """
        return 2 * intensity * rgb + (1 - 2 * intensity) * rgb**2
