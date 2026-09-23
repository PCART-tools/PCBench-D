    def get_value(self, series, key):
        if com.is_bool_indexer(key):
            loc = key
        elif is_list_like(key):
            loc = self.get_indexer(key)
        elif isinstance(key, slice):

            if not (key.step is None or key.step == 1):
                raise ValueError("cannot support not-default "
                                 "step in a slice")

            try:
                loc = self.get_loc(key)
            except TypeError:

                # we didn't find exact intervals
                # or are non-unique
                raise ValueError("unable to slice with "
                                 "this key: {}".format(key))

        else:
            loc = self.get_loc(key)
        return series.iloc[loc]
