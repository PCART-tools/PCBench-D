    def set_annotation_clip(self, b):
        """
        Set the clipping behavior.

        Parameters
        ----------
        b : bool or None

            - *False*: The annotation will always be drawn regardless of its
              position.
            - *True*: The annotation will only be drawn if ``self.xy`` is
              inside the axes.
            - *None*: The annotation will only be drawn if ``self.xy`` is
              inside the axes and  ``self.xycoords == "data"``.
        """
        self._annotation_clip = b
        self.stale = True
