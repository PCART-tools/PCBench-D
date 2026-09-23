    def _process_args(self, *args, **kwargs):
        """
        Process args and kwargs.
        """
        if isinstance(args[0], QuadContourSet):
            if self.levels is None:
                self.levels = args[0].levels
            self.zmin = args[0].zmin
            self.zmax = args[0].zmax
            self._corner_mask = args[0]._corner_mask
            if self._corner_mask == 'legacy':
                contour_generator = args[0].Cntr
            else:
                contour_generator = args[0]._contour_generator
            self._mins = args[0]._mins
            self._maxs = args[0]._maxs
        else:
            self._corner_mask = kwargs.pop('corner_mask', None)
            if self._corner_mask is None:
                self._corner_mask = mpl.rcParams['contour.corner_mask']

            x, y, z = self._contour_args(args, kwargs)

            _mask = ma.getmask(z)
            if _mask is ma.nomask or not _mask.any():
                _mask = None

            if self._corner_mask == 'legacy':
                cbook.warn_deprecated('1.5',
                                      name="corner_mask='legacy'",
                                      alternative='corner_mask=False or True')
                contour_generator = _cntr.Cntr(x, y, z.filled(), _mask)
            else:
                contour_generator = _contour.QuadContourGenerator(
                    x, y, z.filled(), _mask, self._corner_mask, self.nchunk)

            t = self.get_transform()

            # if the transform is not trans data, and some part of it
            # contains transData, transform the xs and ys to data coordinates
            if (t != self.ax.transData and
                    any(t.contains_branch_seperately(self.ax.transData))):
                trans_to_data = t - self.ax.transData
                pts = (np.vstack([x.flat, y.flat]).T)
                transformed_pts = trans_to_data.transform(pts)
                x = transformed_pts[..., 0]
                y = transformed_pts[..., 1]

            self._mins = [ma.min(x), ma.min(y)]
            self._maxs = [ma.max(x), ma.max(y)]

        if self._corner_mask == 'legacy':
            self.Cntr = contour_generator
        else:
            self._contour_generator = contour_generator

        return kwargs
