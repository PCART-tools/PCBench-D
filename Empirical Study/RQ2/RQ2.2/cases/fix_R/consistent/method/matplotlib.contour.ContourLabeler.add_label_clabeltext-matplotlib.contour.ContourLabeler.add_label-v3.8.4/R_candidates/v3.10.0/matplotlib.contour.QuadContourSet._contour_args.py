    def _contour_args(self, args, kwargs):
        if self.filled:
            fn = 'contourf'
        else:
            fn = 'contour'
        nargs = len(args)

        if 0 < nargs <= 2:
            z, *args = args
            z = ma.asarray(z)
            x, y = self._initialize_x_y(z)
        elif 2 < nargs <= 4:
            x, y, z_orig, *args = args
            x, y, z = self._check_xyz(x, y, z_orig, kwargs)

        else:
            raise _api.nargs_error(fn, takes="from 1 to 4", given=nargs)
        z = ma.masked_invalid(z, copy=False)
        self.zmax = z.max().astype(float)
        self.zmin = z.min().astype(float)
        if self.logscale and self.zmin <= 0:
            z = ma.masked_where(z <= 0, z)
            _api.warn_external('Log scale: values of z <= 0 have been masked')
            self.zmin = z.min().astype(float)
        self._process_contour_level_args(args, z.dtype)
        return (x, y, z)
