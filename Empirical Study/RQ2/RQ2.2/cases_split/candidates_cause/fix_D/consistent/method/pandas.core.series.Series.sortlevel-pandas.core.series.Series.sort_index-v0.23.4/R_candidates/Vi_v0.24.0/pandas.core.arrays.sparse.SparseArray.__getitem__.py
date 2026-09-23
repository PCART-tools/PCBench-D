    def __getitem__(self, key):
        if isinstance(key, tuple):
            if len(key) > 1:
                raise IndexError("too many indices for array.")
            key = key[0]

        if is_integer(key):
            return self._get_val_at(key)
        elif isinstance(key, tuple):
            data_slice = self.values[key]
        elif isinstance(key, slice):
            # special case to preserve dtypes
            if key == slice(None):
                return self.copy()
            # TODO: this logic is surely elsewhere
            # TODO: this could be more efficient
            indices = np.arange(len(self), dtype=np.int32)[key]
            return self.take(indices)
        else:
            # TODO: I think we can avoid densifying when masking a
            # boolean SparseArray with another. Need to look at the
            # key's fill_value for True / False, and then do an intersection
            # on the indicies of the sp_values.
            if isinstance(key, SparseArray):
                if is_bool_dtype(key):
                    key = key.to_dense()
                else:
                    key = np.asarray(key)

            if com.is_bool_indexer(key) and len(self) == len(key):
                return self.take(np.arange(len(key), dtype=np.int32)[key])
            elif hasattr(key, '__len__'):
                return self.take(key)
            else:
                raise ValueError("Cannot slice with '{}'".format(key))

        return type(self)(data_slice, kind=self.kind)
