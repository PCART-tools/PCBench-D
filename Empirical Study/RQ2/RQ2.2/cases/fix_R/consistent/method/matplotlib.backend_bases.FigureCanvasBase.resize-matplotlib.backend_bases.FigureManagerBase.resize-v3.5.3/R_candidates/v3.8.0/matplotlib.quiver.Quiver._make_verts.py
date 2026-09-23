    def _make_verts(self, U, V, angles):
        uv = (U + V * 1j)
        str_angles = angles if isinstance(angles, str) else ''
        if str_angles == 'xy' and self.scale_units == 'xy':
            # Here eps is 1 so that if we get U, V by diffing
            # the X, Y arrays, the vectors will connect the
            # points, regardless of the axis scaling (including log).
            angles, lengths = self._angles_lengths(U, V, eps=1)
        elif str_angles == 'xy' or self.scale_units == 'xy':
            # Calculate eps based on the extents of the plot
            # so that we don't end up with roundoff error from
            # adding a small number to a large.
            eps = np.abs(self.axes.dataLim.extents).max() * 0.001
            angles, lengths = self._angles_lengths(U, V, eps=eps)
        if str_angles and self.scale_units == 'xy':
            a = lengths
        else:
            a = np.abs(uv)
        if self.scale is None:
            sn = max(10, math.sqrt(self.N))
            if self.Umask is not ma.nomask:
                amean = a[~self.Umask].mean()
            else:
                amean = a.mean()
            # crude auto-scaling
            # scale is typical arrow length as a multiple of the arrow width
            scale = 1.8 * amean * sn / self.span
        if self.scale_units is None:
            if self.scale is None:
                self.scale = scale
            widthu_per_lenu = 1.0
        else:
            if self.scale_units == 'xy':
                dx = 1
            else:
                dx = self._dots_per_unit(self.scale_units)
            widthu_per_lenu = dx / self._trans_scale
            if self.scale is None:
                self.scale = scale * widthu_per_lenu
        length = a * (widthu_per_lenu / (self.scale * self.width))
        X, Y = self._h_arrows(length)
        if str_angles == 'xy':
            theta = angles
        elif str_angles == 'uv':
            theta = np.angle(uv)
        else:
            theta = ma.masked_invalid(np.deg2rad(angles)).filled(0)
        theta = theta.reshape((-1, 1))  # for broadcasting
        xy = (X + Y * 1j) * np.exp(1j * theta) * self.width
        XY = np.stack((xy.real, xy.imag), axis=2)
        if self.Umask is not ma.nomask:
            XY = ma.array(XY)
            XY[self.Umask] = ma.masked
            # This might be handled more efficiently with nans, given
            # that nans will end up in the paths anyway.

        return XY
