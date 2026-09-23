    def get_extents(self, transform=None, **kwargs):
        """
        Get Bbox of the path.

        Parameters
        ----------
        transform : matplotlib.transforms.Transform, optional
            Transform to apply to path before computing extents, if any.
        **kwargs
            Forwarded to `.iter_bezier`.

        Returns
        -------
        matplotlib.transforms.Bbox
            The extents of the path Bbox([[xmin, ymin], [xmax, ymax]])
        """
        from .transforms import Bbox
        if transform is not None:
            self = transform.transform_path(self)
        bbox = Bbox.null()
        for curve, code in self.iter_bezier(**kwargs):
            # places where the derivative is zero can be extrema
            _, dzeros = curve.axis_aligned_extrema()
            # as can the ends of the curve
            bbox.update_from_data_xy(curve([0, *dzeros, 1]), ignore=False)
        return bbox
