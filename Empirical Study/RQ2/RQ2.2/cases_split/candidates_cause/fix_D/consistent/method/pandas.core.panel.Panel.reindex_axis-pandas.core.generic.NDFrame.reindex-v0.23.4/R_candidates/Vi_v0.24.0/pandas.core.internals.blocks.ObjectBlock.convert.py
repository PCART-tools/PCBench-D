    def convert(self, *args, **kwargs):
        """ attempt to coerce any object types to better types return a copy of
        the block (if copy = True) by definition we ARE an ObjectBlock!!!!!

        can return multiple blocks!
        """

        if args:
            raise NotImplementedError
        by_item = kwargs.get('by_item', True)

        new_inputs = ['coerce', 'datetime', 'numeric', 'timedelta']
        new_style = False
        for kw in new_inputs:
            new_style |= kw in kwargs

        if new_style:
            fn = soft_convert_objects
            fn_inputs = new_inputs
        else:
            fn = maybe_convert_objects
            fn_inputs = ['convert_dates', 'convert_numeric',
                         'convert_timedeltas']
        fn_inputs += ['copy']

        fn_kwargs = {key: kwargs[key] for key in fn_inputs if key in kwargs}

        # operate column-by-column
        def f(m, v, i):
            shape = v.shape
            values = fn(v.ravel(), **fn_kwargs)
            try:
                values = values.reshape(shape)
                values = _block_shape(values, ndim=self.ndim)
            except (AttributeError, NotImplementedError):
                pass

            return values

        if by_item and not self._is_single_block:
            blocks = self.split_and_operate(None, f, False)
        else:
            values = f(None, self.values.ravel(), None)
            blocks = [make_block(values, ndim=self.ndim,
                                 placement=self.mgr_locs)]

        return blocks
