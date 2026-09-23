    def _concat_same_dtype(self, indexes, name):
        return _concat._concat_index_same_dtype(indexes).rename(name)
