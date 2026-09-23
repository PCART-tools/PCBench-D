    def get_result(self):
        """ compute the results """

        # all empty
        if len(self.columns) == 0 and len(self.index) == 0:
            return self.apply_empty_result()

        # string dispatch
        if isinstance(self.f, compat.string_types):
            # Support for `frame.transform('method')`
            # Some methods (shift, etc.) require the axis argument, others
            # don't, so inspect and insert if nescessary.
            func = getattr(self.obj, self.f)
            sig = compat.signature(func)
            if 'axis' in sig.args:
                self.kwds['axis'] = self.axis
            return func(*self.args, **self.kwds)

        # ufunc
        elif isinstance(self.f, np.ufunc):
            with np.errstate(all='ignore'):
                results = self.f(self.values)
            return self.obj._constructor(data=results, index=self.index,
                                         columns=self.columns, copy=False)

        # broadcasting
        if self.result_type == 'broadcast':
            return self.apply_broadcast()

        # one axis empty
        elif not all(self.obj.shape):
            return self.apply_empty_result()

        # raw
        elif self.raw and not self.obj._is_mixed_type:
            return self.apply_raw()

        return self.apply_standard()
