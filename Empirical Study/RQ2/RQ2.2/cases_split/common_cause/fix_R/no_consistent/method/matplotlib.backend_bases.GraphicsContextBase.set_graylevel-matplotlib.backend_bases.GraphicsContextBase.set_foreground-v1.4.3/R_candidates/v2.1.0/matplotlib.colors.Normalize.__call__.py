    def __call__(self, value, clip=None):
        """
        Normalize *value* data in the ``[vmin, vmax]`` interval into
        the ``[0.0, 1.0]`` interval and return it.  *clip* defaults
        to *self.clip* (which defaults to *False*).  If not already
        initialized, *vmin* and *vmax* are initialized using
        *autoscale_None(value)*.
        """
        if clip is None:
            clip = self.clip

        result, is_scalar = self.process_value(value)

        self.autoscale_None(result)
        # Convert at least to float, without losing precision.
        (vmin,), _ = self.process_value(self.vmin)
        (vmax,), _ = self.process_value(self.vmax)
        if vmin == vmax:
            result.fill(0)   # Or should it be all masked?  Or 0.5?
        elif vmin > vmax:
            raise ValueError("minvalue must be less than or equal to maxvalue")
        else:
            if clip:
                mask = np.ma.getmask(result)
                result = np.ma.array(np.clip(result.filled(vmax), vmin, vmax),
                                     mask=mask)
            # ma division is very slow; we can take a shortcut
            resdat = result.data
            resdat -= vmin
            resdat /= (vmax - vmin)
            result = np.ma.array(resdat, mask=result.mask, copy=False)
        # Agg cannot handle float128.  We actually only need 32-bit of
        # precision, but on Windows, `np.dtype(np.longdouble) == np.float64`,
        # so casting to float32 would lose precision on float64s as well.
        if result.dtype == np.longdouble:
            result = result.astype(np.float64)
        if is_scalar:
            result = result[0]
        return result
