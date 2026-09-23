    def convert(
        self,
        copy: bool = True,
        datetime: bool = True,
        numeric: bool = True,
        timedelta: bool = True,
        coerce: bool = False,
    ):
        """ attempt to coerce any object types to better types return a copy of
        the block (if copy = True) by definition we ARE an ObjectBlock!!!!!

        can return multiple blocks!
        """

        # operate column-by-column
        def f(mask, val, idx):
            shape = val.shape
            values = soft_convert_objects(
                val.ravel(),
                datetime=datetime,
                numeric=numeric,
                timedelta=timedelta,
                coerce=coerce,
                copy=copy,
            )
            if isinstance(values, np.ndarray):
                # TODO: allow EA once reshape is supported
                values = values.reshape(shape)

            values = _block_shape(values, ndim=self.ndim)
            return values

        if self.ndim == 2:
            blocks = self.split_and_operate(None, f, False)
        else:
            values = f(None, self.values.ravel(), None)
            blocks = [make_block(values, ndim=self.ndim, placement=self.mgr_locs)]

        return blocks
