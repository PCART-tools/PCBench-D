    def get_new_values(self, values, fill_value=None):

        if values.ndim == 1:
            values = values[:, np.newaxis]

        sorted_values = self._make_sorted_values(values)

        # place the values
        length, width = self.full_shape
        stride = values.shape[1]
        result_width = width * stride
        result_shape = (length, result_width)
        mask = self.mask
        mask_all = self.mask_all

        # we can simply reshape if we don't have a mask
        if mask_all and len(values):
            # TODO: Under what circumstances can we rely on sorted_values
            #  matching values?  When that holds, we can slice instead
            #  of take (in particular for EAs)
            new_values = (
                sorted_values.reshape(length, width, stride)
                .swapaxes(1, 2)
                .reshape(result_shape)
            )
            new_mask = np.ones(result_shape, dtype=bool)
            return new_values, new_mask

        dtype = values.dtype

        # if our mask is all True, then we can use our existing dtype
        if mask_all:
            dtype = values.dtype
            new_values = np.empty(result_shape, dtype=dtype)
        else:
            if isinstance(dtype, ExtensionDtype):
                # GH#41875
                # We are assuming that fill_value can be held by this dtype,
                #  unlike the non-EA case that promotes.
                cls = dtype.construct_array_type()
                new_values = cls._empty(result_shape, dtype=dtype)
                new_values[:] = fill_value
            else:
                dtype, fill_value = maybe_promote(dtype, fill_value)
                new_values = np.empty(result_shape, dtype=dtype)
                new_values.fill(fill_value)

        name = dtype.name
        new_mask = np.zeros(result_shape, dtype=bool)

        # we need to convert to a basic dtype
        # and possibly coerce an input to our output dtype
        # e.g. ints -> floats
        if needs_i8_conversion(values.dtype):
            sorted_values = sorted_values.view("i8")
            new_values = new_values.view("i8")
        else:
            sorted_values = sorted_values.astype(name, copy=False)

        # fill in our values & mask
        libreshape.unstack(
            sorted_values,
            mask.view("u1"),
            stride,
            length,
            width,
            new_values,
            new_mask.view("u1"),
        )

        # reconstruct dtype if needed
        if needs_i8_conversion(values.dtype):
            # view as datetime64 so we can wrap in DatetimeArray and use
            #  DTA's view method
            new_values = new_values.view("M8[ns]")
            new_values = ensure_wrapped_if_datetimelike(new_values)
            new_values = new_values.view(values.dtype)

        return new_values, new_mask
