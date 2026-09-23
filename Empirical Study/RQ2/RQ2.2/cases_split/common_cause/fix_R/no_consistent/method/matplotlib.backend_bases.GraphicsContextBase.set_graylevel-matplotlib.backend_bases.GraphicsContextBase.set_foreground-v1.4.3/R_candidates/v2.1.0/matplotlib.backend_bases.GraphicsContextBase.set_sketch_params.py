    def set_sketch_params(self, scale=None, length=None, randomness=None):
        """
        Sets the sketch parameters.

        Parameters
        ----------

        scale : float, optional
            The amplitude of the wiggle perpendicular to the source
            line, in pixels.  If scale is `None`, or not provided, no
            sketch filter will be provided.

        length : float, optional
             The length of the wiggle along the line, in pixels
             (default 128)

        randomness : float, optional
            The scale factor by which the length is shrunken or
            expanded (default 16)
        """
        self._sketch = (
            None if scale is None
            else (scale, length or 128., randomness or 16.))
