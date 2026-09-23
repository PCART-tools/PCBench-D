    def get_new_values(self):
        values = self.values

        # place the values
        length, width = self.full_shape
        stride = values.shape[1]
        result_width = width * stride
        result_shape = (length, result_width)

        # if our mask is all True, then we can use our existing dtype
        if self.mask.all():
            dtype = values.dtype
            new_values = np.empty(result_shape, dtype=dtype)
        else:
            dtype, fill_value = _maybe_promote(values.dtype)
            new_values = np.empty(result_shape, dtype=dtype)
            new_values.fill(fill_value)

        new_mask = np.zeros(result_shape, dtype=bool)

        # is there a simpler / faster way of doing this?
        for i in range(values.shape[1]):
            chunk = new_values[:, i * width: (i + 1) * width]
            mask_chunk = new_mask[:, i * width: (i + 1) * width]

            chunk.flat[self.mask] = self.sorted_values[:, i]
            mask_chunk.flat[self.mask] = True

        return new_values, new_mask
