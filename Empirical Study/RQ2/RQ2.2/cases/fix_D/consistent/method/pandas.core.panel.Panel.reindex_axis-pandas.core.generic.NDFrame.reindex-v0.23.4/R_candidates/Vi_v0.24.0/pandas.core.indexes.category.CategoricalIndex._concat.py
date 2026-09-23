    def _concat(self, to_concat, name):
        # if calling index is category, don't check dtype of others
        return CategoricalIndex._concat_same_dtype(self, to_concat, name)
