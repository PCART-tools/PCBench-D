    def _assert_take_fillable(self, values, indices, allow_fill=True,
                              fill_value=None, na_value=None):
        """ Internal method to handle NA filling of take """
        # only fill if we are passing a non-None fill_value
        if allow_fill and fill_value is not None:
            if (indices < -1).any():
                msg = ('When allow_fill=True and fill_value is not None, '
                       'all indices must be >= -1')
                raise ValueError(msg)
            taken = [lab.take(indices) for lab in self.labels]
            mask = indices == -1
            if mask.any():
                masked = []
                for new_label in taken:
                    label_values = new_label.values()
                    label_values[mask] = na_value
                    masked.append(FrozenNDArray(label_values))
                taken = masked
        else:
            taken = [lab.take(indices) for lab in self.labels]
        return taken
