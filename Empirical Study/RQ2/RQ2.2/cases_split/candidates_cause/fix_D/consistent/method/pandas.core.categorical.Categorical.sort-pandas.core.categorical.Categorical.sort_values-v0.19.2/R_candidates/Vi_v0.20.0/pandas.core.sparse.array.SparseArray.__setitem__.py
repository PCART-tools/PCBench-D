    def __setitem__(self, key, value):
        # if is_integer(key):
        #    self.values[key] = value
        # else:
        #    raise Exception("SparseArray does not support seting non-scalars
        # via setitem")
        raise TypeError(
            "SparseArray does not support item assignment via setitem")
