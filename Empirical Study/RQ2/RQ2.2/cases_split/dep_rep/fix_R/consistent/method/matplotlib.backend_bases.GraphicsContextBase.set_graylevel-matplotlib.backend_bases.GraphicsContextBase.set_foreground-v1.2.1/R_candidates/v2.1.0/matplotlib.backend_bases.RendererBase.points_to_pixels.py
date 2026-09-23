    def points_to_pixels(self, points):
        """
        Convert points to display units

        You need to override this function (unless your backend
        doesn't have a dpi, e.g., postscript or svg).  Some imaging
        systems assume some value for pixels per inch::

            points to pixels = points * pixels_per_inch/72.0 * dpi/72.0

        Parameters
        ----------
        points : scalar or array_like
            a float or a numpy array of float

        Returns
        -------
        Points converted to pixels
        """
        return points
