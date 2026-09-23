    def _get_new_axes(self):
        ndim = self._get_result_dim()
        new_axes = [None] * ndim

        if self.join_axes is None:
            for i in range(ndim):
                if i == self.axis:
                    continue
                new_axes[i] = self._get_comb_axis(i)

        else:
            # GH 21951
            warnings.warn(
                "The join_axes-keyword is deprecated. Use .reindex or "
                ".reindex_like on the result to achieve the same "
                "functionality.",
                FutureWarning,
                stacklevel=4,
            )

            if len(self.join_axes) != ndim - 1:
                raise AssertionError(
                    "length of join_axes must be equal "
                    "to {length}".format(length=ndim - 1)
                )

            # ufff...
            indices = list(range(ndim))
            indices.remove(self.axis)

            for i, ax in zip(indices, self.join_axes):
                new_axes[i] = ax

        new_axes[self.axis] = self._get_concat_axis()
        return new_axes
