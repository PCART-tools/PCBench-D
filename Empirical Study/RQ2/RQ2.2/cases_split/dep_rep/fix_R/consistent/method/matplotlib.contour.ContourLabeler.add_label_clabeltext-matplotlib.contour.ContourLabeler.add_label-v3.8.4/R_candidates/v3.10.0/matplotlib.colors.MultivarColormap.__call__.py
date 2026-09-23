    def __call__(self, X, alpha=None, bytes=False, clip=True):
        r"""
        Parameters
        ----------
        X : tuple (X0, X1, ...) of length equal to the number of colormaps
            X0, X1 ...:
            float or int, `~numpy.ndarray` or scalar
            The data value(s) to convert to RGBA.
            For floats, *Xi...* should be in the interval ``[0.0, 1.0]`` to
            return the RGBA values ``X*100`` percent along the Colormap line.
            For integers, *Xi...*  should be in the interval ``[0, self[i].N)`` to
            return RGBA values *indexed* from colormap [i] with index ``Xi``, where
            self[i] is colormap i.
        alpha : float or array-like or None
            Alpha must be a scalar between 0 and 1, a sequence of such
            floats with shape matching *Xi*, or None.
        bytes : bool, default: False
            If False (default), the returned RGBA values will be floats in the
            interval ``[0, 1]`` otherwise they will be `numpy.uint8`\s in the
            interval ``[0, 255]``.
        clip : bool, default: True
            If True, clip output to 0 to 1

        Returns
        -------
        Tuple of RGBA values if X[0] is scalar, otherwise an array of
        RGBA values with a shape of ``X.shape + (4, )``.
        """

        if len(X) != len(self):
            raise ValueError(
                f'For the selected colormap the data must have a first dimension '
                f'{len(self)}, not {len(X)}')
        rgba, mask_bad = self[0]._get_rgba_and_mask(X[0], bytes=False)
        for c, xx in zip(self[1:], X[1:]):
            sub_rgba, sub_mask_bad = c._get_rgba_and_mask(xx, bytes=False)
            rgba[..., :3] += sub_rgba[..., :3]  # add colors
            rgba[..., 3] *= sub_rgba[..., 3]  # multiply alpha
            mask_bad |= sub_mask_bad

        if self.combination_mode == 'sRGB_sub':
            rgba[..., :3] -= len(self) - 1

        rgba[mask_bad] = self.get_bad()

        if clip:
            rgba = np.clip(rgba, 0, 1)

        if alpha is not None:
            if clip:
                alpha = np.clip(alpha, 0, 1)
            if np.shape(alpha) not in [(), np.shape(X[0])]:
                raise ValueError(
                    f"alpha is array-like but its shape {np.shape(alpha)} does "
                    f"not match that of X[0] {np.shape(X[0])}")
            rgba[..., -1] *= alpha

        if bytes:
            if not clip:
                raise ValueError(
                    "clip cannot be false while bytes is true"
                    " as uint8 does not support values below 0"
                    " or above 255.")
            rgba = (rgba * 255).astype('uint8')

        if not np.iterable(X[0]):
            rgba = tuple(rgba)

        return rgba
