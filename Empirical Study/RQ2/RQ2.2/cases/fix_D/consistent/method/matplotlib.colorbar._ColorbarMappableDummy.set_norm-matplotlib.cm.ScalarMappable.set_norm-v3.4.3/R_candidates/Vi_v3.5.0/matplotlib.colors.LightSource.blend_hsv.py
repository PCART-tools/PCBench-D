    def blend_hsv(self, rgb, intensity, hsv_max_sat=None, hsv_max_val=None,
                  hsv_min_val=None, hsv_min_sat=None):
        """
        Take the input data array, convert to HSV values in the given colormap,
        then adjust those color values to give the impression of a shaded
        relief map with a specified light source.  RGBA values are returned,
        which can then be used to plot the shaded image with imshow.

        The color of the resulting image will be darkened by moving the (s, v)
        values (in hsv colorspace) toward (hsv_min_sat, hsv_min_val) in the
        shaded regions, or lightened by sliding (s, v) toward (hsv_max_sat,
        hsv_max_val) in regions that are illuminated.  The default extremes are
        chose so that completely shaded points are nearly black (s = 1, v = 0)
        and completely illuminated points are nearly white (s = 0, v = 1).

        Parameters
        ----------
        rgb : ndarray
            An MxNx3 RGB array of floats ranging from 0 to 1 (color image).
        intensity : ndarray
            An MxNx1 array of floats ranging from 0 to 1 (grayscale image).
        hsv_max_sat : number, default: 1
            The maximum saturation value that the *intensity* map can shift the
            output image to.
        hsv_min_sat : number, optional
            The minimum saturation value that the *intensity* map can shift the
            output image to. Defaults to 0.
        hsv_max_val : number, optional
            The maximum value ("v" in "hsv") that the *intensity* map can shift
            the output image to. Defaults to 1.
        hsv_min_val : number, optional
            The minimum value ("v" in "hsv") that the *intensity* map can shift
            the output image to. Defaults to 0.

        Returns
        -------
        ndarray
            An MxNx3 RGB array representing the combined images.
        """
        # Backward compatibility...
        if hsv_max_sat is None:
            hsv_max_sat = self.hsv_max_sat
        if hsv_max_val is None:
            hsv_max_val = self.hsv_max_val
        if hsv_min_sat is None:
            hsv_min_sat = self.hsv_min_sat
        if hsv_min_val is None:
            hsv_min_val = self.hsv_min_val

        # Expects a 2D intensity array scaled between -1 to 1...
        intensity = intensity[..., 0]
        intensity = 2 * intensity - 1

        # Convert to rgb, then rgb to hsv
        hsv = rgb_to_hsv(rgb[:, :, 0:3])
        hue, sat, val = np.moveaxis(hsv, -1, 0)

        # Modify hsv values (in place) to simulate illumination.
        # putmask(A, mask, B) <=> A[mask] = B[mask]
        np.putmask(sat, (np.abs(sat) > 1.e-10) & (intensity > 0),
                   (1 - intensity) * sat + intensity * hsv_max_sat)
        np.putmask(sat, (np.abs(sat) > 1.e-10) & (intensity < 0),
                   (1 + intensity) * sat - intensity * hsv_min_sat)
        np.putmask(val, intensity > 0,
                   (1 - intensity) * val + intensity * hsv_max_val)
        np.putmask(val, intensity < 0,
                   (1 + intensity) * val - intensity * hsv_min_val)
        np.clip(hsv[:, :, 1:], 0, 1, out=hsv[:, :, 1:])

        # Convert modified hsv back to rgb.
        return hsv_to_rgb(hsv)
