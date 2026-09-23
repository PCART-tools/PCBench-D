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
        if self.codes is None:
            xys = self.vertices
        elif len(np.intersect1d(self.codes, [Path.CURVE3, Path.CURVE4])) == 0:
            # Optimization for the straight line case.
            # Instead of iterating through each curve, consider
            # each line segment's end-points
            # (recall that STOP and CLOSEPOLY vertices are ignored)
            xys = self.vertices[np.isin(self.codes,
                                        [Path.MOVETO, Path.LINETO])]
        else:
            xys = []
            for curve, code in self.iter_bezier(**kwargs):
                # places where the derivative is zero can be extrema
                _, dzeros = curve.axis_aligned_extrema()
                # as can the ends of the curve
                xys.append(curve([0, *dzeros, 1]))
            xys = np.concatenate(xys)
        if len(xys):
            return Bbox([xys.min(axis=0), xys.max(axis=0)])
        else:
            return Bbox.null()
