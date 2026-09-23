    def _try_coerce_result(self, result):
        """ reverse of try_coerce_args """

        # GH12564: CategoricalBlock is 1-dim only
        # while returned results could be any dim
        if (not is_categorical_dtype(result)) and isinstance(result, np.ndarray):
            result = _block_shape(result, ndim=self.ndim)

        return result
