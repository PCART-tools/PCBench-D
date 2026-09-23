    def __getitem__(self, key):
        if not isinstance(key, tuple):

            # we could have a convertible item here (e.g. Timestamp)
            if not is_list_like_indexer(key):
                key = tuple([key])
            else:
                raise ValueError('Invalid call for scalar access (getting)!')

        key = self._convert_key(key)
        return self.obj._get_value(*key, takeable=self._takeable)
