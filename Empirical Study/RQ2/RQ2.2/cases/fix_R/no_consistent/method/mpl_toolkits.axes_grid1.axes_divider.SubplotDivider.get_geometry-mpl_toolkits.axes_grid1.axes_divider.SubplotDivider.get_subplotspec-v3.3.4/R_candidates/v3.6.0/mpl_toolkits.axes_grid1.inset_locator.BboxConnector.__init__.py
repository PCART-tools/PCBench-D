    @_docstring.dedent_interpd
    def __init__(self, bbox1, bbox2, loc1, loc2=None, **kwargs):
        """
        Connect two bboxes with a straight line.

        Parameters
        ----------
        bbox1, bbox2 : `matplotlib.transforms.Bbox`
            Bounding boxes to connect.

        loc1, loc2 : {1, 2, 3, 4}
            Corner of *bbox1* and *bbox2* to draw the line. Valid values are::

                'upper right'  : 1,
                'upper left'   : 2,
                'lower left'   : 3,
                'lower right'  : 4

            *loc2* is optional and defaults to *loc1*.

        **kwargs
            Patch properties for the line drawn. Valid arguments include:

            %(Patch:kwdoc)s
        """
        if "transform" in kwargs:
            raise ValueError("transform should not be set")

        kwargs["transform"] = IdentityTransform()
        if 'fill' in kwargs:
            super().__init__(**kwargs)
        else:
            fill = bool({'fc', 'facecolor', 'color'}.intersection(kwargs))
            super().__init__(fill=fill, **kwargs)
        self.bbox1 = bbox1
        self.bbox2 = bbox2
        self.loc1 = loc1
        self.loc2 = loc2
