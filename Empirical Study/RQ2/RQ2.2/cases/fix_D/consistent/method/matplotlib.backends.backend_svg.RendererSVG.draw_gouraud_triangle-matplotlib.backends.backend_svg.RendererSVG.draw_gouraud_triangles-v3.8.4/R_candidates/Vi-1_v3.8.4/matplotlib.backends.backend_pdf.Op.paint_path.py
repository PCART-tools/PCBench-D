    @classmethod
    def paint_path(cls, fill, stroke):
        """
        Return the PDF operator to paint a path.

        Parameters
        ----------
        fill : bool
            Fill the path with the fill color.
        stroke : bool
            Stroke the outline of the path with the line color.
        """
        if stroke:
            if fill:
                return cls.fill_stroke
            else:
                return cls.stroke
        else:
            if fill:
                return cls.fill
            else:
                return cls.endpath
