    def downcast(self, dtypes=None, mgr=None):
        """ try to downcast each item to the dict of dtypes if present """

        # turn it off completely
        if dtypes is False:
            return self

        values = self.values

        # single block handling
        if self._is_single_block:

            # try to cast all non-floats here
            if dtypes is None:
                dtypes = 'infer'

            nv = maybe_downcast_to_dtype(values, dtypes)
            return self.make_block(nv)

        # ndim > 1
        if dtypes is None:
            return self

        if not (dtypes == 'infer' or isinstance(dtypes, dict)):
            raise ValueError("downcast must have a dictionary or 'infer' as "
                             "its argument")

        # operate column-by-column
        # this is expensive as it splits the blocks items-by-item
        def f(m, v, i):

            if dtypes == 'infer':
                dtype = 'infer'
            else:
                raise AssertionError("dtypes as dict is not supported yet")

            if dtype is not None:
                v = maybe_downcast_to_dtype(v, dtype)
            return v

        return self.split_and_operate(None, f, False)
