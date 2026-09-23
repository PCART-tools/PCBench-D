    def get_sketch_params(self):
        """
        Return the sketch parameters for the artist.

        Returns
        -------
        sketch_params : tuple or `None`

            A 3-tuple with the following elements:

            * `scale`: The amplitude of the wiggle perpendicular to the
              source line.
            * `length`: The length of the wiggle along the line.
            * `randomness`: The scale factor by which the length is
              shrunken or expanded.

            May return `None` if no sketch parameters were set.
        """
        return self._sketch
