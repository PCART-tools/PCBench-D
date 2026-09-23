    def convert(self, *args, **kwargs):
        """ attempt to coerce any object types to better types return a copy of
        the block (if copy = True) by definition we ARE an ObjectBlock!!!!!

        can return multiple blocks!
        """

        if args:
            raise NotImplementedError
        by_item = True if 'by_item' not in kwargs else kwargs['by_item']

        new_inputs = ['coerce', 'datetime', 'numeric', 'timedelta']
        new_style = False
        for kw in new_inputs:
            new_style |= kw in kwargs

        if new_style:
            fn = _soft_convert_objects
            fn_inputs = new_inputs
        else:
            fn = _possibly_convert_objects
            fn_inputs = ['convert_dates', 'convert_numeric',
                         'convert_timedeltas']
        fn_inputs += ['copy']

        fn_kwargs = {}
        for key in fn_inputs:
            if key in kwargs:
                fn_kwargs[key] = kwargs[key]

        # attempt to create new type blocks
        blocks = []
        if by_item and not self._is_single_block:

            for i, rl in enumerate(self.mgr_locs):
                values = self.iget(i)

                shape = values.shape
                values = fn(values.ravel(), **fn_kwargs)
                try:
                    values = values.reshape(shape)
                    values = _block_shape(values, ndim=self.ndim)
                except (AttributeError, NotImplementedError):
                    pass
                newb = make_block(values, ndim=self.ndim, placement=[rl])
                blocks.append(newb)

        else:
            values = fn(
                self.values.ravel(), **fn_kwargs).reshape(self.values.shape)
            blocks.append(make_block(values, ndim=self.ndim,
                                     placement=self.mgr_locs))

        return blocks
