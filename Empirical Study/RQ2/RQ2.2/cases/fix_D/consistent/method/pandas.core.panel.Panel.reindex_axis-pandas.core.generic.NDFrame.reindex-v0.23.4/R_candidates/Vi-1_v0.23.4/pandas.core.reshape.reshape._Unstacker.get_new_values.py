    def get_new_values(self):
        values = self.values

        # place the values
        length, width = self.full_shape
        stride = values.shape[1]
        result_width = width * stride
        result_shape = (length, result_width)
        mask = self.mask
        mask_all = mask.all()

        # we can simply reshape if we don't have a mask
        if mask_all and len(values):
            new_values = (self.sorted_values
                              .reshape(length, width, stride)
                              .swapaxes(1, 2)
                              .reshape(result_shape)
                          )
            new_mask = np.ones(result_shape, dtype=bool)
            return new_values, new_mask

        # if our mask is all True, then we can use our existing dtype
        if mask_all:
            dtype = values.dtype
            new_values = np.empty(result_shape, dtype=dtype)
        else:
            dtype, fill_value = maybe_promote(values.dtype, self.fill_value)
            new_values = np.empty(result_shape, dtype=dtype)
            new_values.fill(fill_value)

        new_mask = np.zeros(result_shape, dtype=bool)

        name = np.dtype(dtype).name
        sorted_values = self.sorted_values

        # we need to convert to a basic dtype
        # and possibly coerce an input to our output dtype
        # e.g. ints -> floats
        if needs_i8_conversion(values):
            sorted_values = sorted_values.view('i8')
            new_values = new_values.view('i8')
            name = 'int64'
        elif is_bool_dtype(values):
            sorted_values = sorted_values.astype('object')
            new_values = new_values.astype('object')
            name = 'object'
        else:
            sorted_values = sorted_values.astype(name, copy=False)

        # fill in our values & mask
        f = getattr(_reshape, "unstack_{name}".format(name=name))
        f(sorted_values,
          mask.view('u1'),
          stride,
          length,
          width,
          new_values,
          new_mask.view('u1'))

        # reconstruct dtype if needed
        if needs_i8_conversion(values):
            new_values = new_values.view(values.dtype)

        return new_values, new_mask
