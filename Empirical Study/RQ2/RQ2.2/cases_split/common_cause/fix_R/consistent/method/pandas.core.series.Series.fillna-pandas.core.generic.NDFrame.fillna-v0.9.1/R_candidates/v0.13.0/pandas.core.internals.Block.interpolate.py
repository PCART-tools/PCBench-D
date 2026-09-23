    def interpolate(self, method='pad', axis=0, index=None,
                    values=None, inplace=False, limit=None,
                    fill_value=None, coerce=False, downcast=None, **kwargs):

        # a fill na type method
        try:
            m = com._clean_fill_method(method)
        except:
            m = None

        if m is not None:
            return self._interpolate_with_fill(method=m,
                                               axis=axis,
                                               inplace=inplace,
                                               limit=limit,
                                               fill_value=fill_value,
                                               coerce=coerce,
                                               downcast=downcast)
        # try an interp method
        try:
            m = com._clean_interp_method(method, **kwargs)
        except:
            m = None

        if m is not None:
            return self._interpolate(method=m,
                                     index=index,
                                     values=values,
                                     axis=axis,
                                     limit=limit,
                                     fill_value=fill_value,
                                     inplace=inplace,
                                     downcast=downcast,
                                     **kwargs)

        raise ValueError("invalid method '{0}' to interpolate.".format(method))
