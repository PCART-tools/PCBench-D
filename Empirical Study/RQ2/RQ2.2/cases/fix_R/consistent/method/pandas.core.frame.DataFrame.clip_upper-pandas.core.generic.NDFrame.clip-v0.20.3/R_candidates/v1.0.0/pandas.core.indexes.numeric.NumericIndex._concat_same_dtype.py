    def _concat_same_dtype(self, indexes, name):
        result = type(indexes[0])(np.concatenate([x._values for x in indexes]))
        return result.rename(name)
