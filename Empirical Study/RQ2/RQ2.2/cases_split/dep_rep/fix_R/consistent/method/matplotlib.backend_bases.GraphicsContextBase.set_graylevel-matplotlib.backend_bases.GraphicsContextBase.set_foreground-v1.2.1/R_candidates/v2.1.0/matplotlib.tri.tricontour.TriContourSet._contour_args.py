    def _contour_args(self, args, kwargs):
        if self.filled:
            fn = 'contourf'
        else:
            fn = 'contour'
        tri, args, kwargs = Triangulation.get_from_args_and_kwargs(*args,
                                                                   **kwargs)
        z = np.asarray(args[0])
        if z.shape != tri.x.shape:
            raise ValueError('z array must have same length as triangulation x'
                             ' and y arrays')
        self.zmax = z.max()
        self.zmin = z.min()
        if self.logscale and self.zmin <= 0:
            raise ValueError('Cannot %s log of negative values.' % fn)
        self._contour_level_args(z, args[1:])
        return (tri, z)
