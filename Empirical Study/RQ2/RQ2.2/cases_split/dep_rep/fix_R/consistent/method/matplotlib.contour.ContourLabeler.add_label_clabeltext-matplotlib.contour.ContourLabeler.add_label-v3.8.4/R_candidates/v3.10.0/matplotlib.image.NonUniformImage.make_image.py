    def make_image(self, renderer, magnification=1.0, unsampled=False):
        # docstring inherited
        if self._A is None:
            raise RuntimeError('You must first set the image array')
        if unsampled:
            raise ValueError('unsampled not supported on NonUniformImage')
        A = self._A
        if A.ndim == 2:
            if A.dtype != np.uint8:
                A = self.to_rgba(A, bytes=True)
            else:
                A = np.repeat(A[:, :, np.newaxis], 4, 2)
                A[:, :, 3] = 255
        else:
            if A.dtype != np.uint8:
                A = (255*A).astype(np.uint8)
            if A.shape[2] == 3:
                B = np.zeros(tuple([*A.shape[0:2], 4]), np.uint8)
                B[:, :, 0:3] = A
                B[:, :, 3] = 255
                A = B
        l, b, r, t = self.axes.bbox.extents
        width = int(((round(r) + 0.5) - (round(l) - 0.5)) * magnification)
        height = int(((round(t) + 0.5) - (round(b) - 0.5)) * magnification)

        invertedTransform = self.axes.transData.inverted()
        x_pix = invertedTransform.transform(
            [(x, b) for x in np.linspace(l, r, width)])[:, 0]
        y_pix = invertedTransform.transform(
            [(l, y) for y in np.linspace(b, t, height)])[:, 1]

        if self._interpolation == "nearest":
            x_mid = (self._Ax[:-1] + self._Ax[1:]) / 2
            y_mid = (self._Ay[:-1] + self._Ay[1:]) / 2
            x_int = x_mid.searchsorted(x_pix)
            y_int = y_mid.searchsorted(y_pix)
            # The following is equal to `A[y_int[:, None], x_int[None, :]]`,
            # but many times faster.  Both casting to uint32 (to have an
            # effectively 1D array) and manual index flattening matter.
            im = (
                np.ascontiguousarray(A).view(np.uint32).ravel()[
                    np.add.outer(y_int * A.shape[1], x_int)]
                .view(np.uint8).reshape((height, width, 4)))
        else:  # self._interpolation == "bilinear"
            # Use np.interp to compute x_int/x_float has similar speed.
            x_int = np.clip(
                self._Ax.searchsorted(x_pix) - 1, 0, len(self._Ax) - 2)
            y_int = np.clip(
                self._Ay.searchsorted(y_pix) - 1, 0, len(self._Ay) - 2)
            idx_int = np.add.outer(y_int * A.shape[1], x_int)
            x_frac = np.clip(
                np.divide(x_pix - self._Ax[x_int], np.diff(self._Ax)[x_int],
                          dtype=np.float32),  # Downcasting helps with speed.
                0, 1)
            y_frac = np.clip(
                np.divide(y_pix - self._Ay[y_int], np.diff(self._Ay)[y_int],
                          dtype=np.float32),
                0, 1)
            f00 = np.outer(1 - y_frac, 1 - x_frac)
            f10 = np.outer(y_frac, 1 - x_frac)
            f01 = np.outer(1 - y_frac, x_frac)
            f11 = np.outer(y_frac, x_frac)
            im = np.empty((height, width, 4), np.uint8)
            for chan in range(4):
                ac = A[:, :, chan].reshape(-1)  # reshape(-1) avoids a copy.
                # Shifting the buffer start (`ac[offset:]`) avoids an array
                # addition (`ac[idx_int + offset]`).
                buf = f00 * ac[idx_int]
                buf += f10 * ac[A.shape[1]:][idx_int]
                buf += f01 * ac[1:][idx_int]
                buf += f11 * ac[A.shape[1] + 1:][idx_int]
                im[:, :, chan] = buf  # Implicitly casts to uint8.
        return im, l, b, IdentityTransform()
