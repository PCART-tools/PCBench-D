    def interpolate(self, method='pad', axis=0, index=None, values=None,
                    inplace=False, limit=None, limit_direction='forward',
                    fill_value=None, coerce=False, downcast=None, mgr=None,
                    **kwargs):
        def check_int_bool(self, inplace):
            # Only FloatBlocks will contain NaNs.
            # timedelta subclasses IntBlock
            if (self.is_bool or self.is_integer) and not self.is_timedelta:
                if inplace:
                    return self
                else:
                    return self.copy()

        # a fill na type method
        try:
            m = missing.clean_fill_method(method)
        except:
            m = None

        if m is not None:
            r = check_int_bool(self, inplace)
            if r is not None:
                return r
            return self._interpolate_with_fill(method=m, axis=axis,
                                               inplace=inplace, limit=limit,
                                               fill_value=fill_value,
                                               coerce=coerce,
                                               downcast=downcast, mgr=mgr)
        # try an interp method
        try:
            m = missing.clean_interp_method(method, **kwargs)
        except:
            m = None

        if m is not None:
            r = check_int_bool(self, inplace)
            if r is not None:
                return r
            return self._interpolate(method=m, index=index, values=values,
                                     axis=axis, limit=limit,
                                     limit_direction=limit_direction,
                                     fill_value=fill_value, inplace=inplace,
                                     downcast=downcast, mgr=mgr, **kwargs)

        raise ValueError("invalid method '{0}' to interpolate.".format(method))
