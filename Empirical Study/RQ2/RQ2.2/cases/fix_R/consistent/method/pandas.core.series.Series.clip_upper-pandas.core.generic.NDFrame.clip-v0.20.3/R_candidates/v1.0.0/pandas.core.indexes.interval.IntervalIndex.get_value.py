    @Appender(_index_shared_docs["get_value"] % _index_doc_kwargs)
    def get_value(self, series: ABCSeries, key: Any) -> Any:

        if com.is_bool_indexer(key):
            loc = key
        elif is_list_like(key):
            if self.is_overlapping:
                loc, missing = self.get_indexer_non_unique(key)
                if len(missing):
                    raise KeyError
            else:
                loc = self.get_indexer(key)
        elif isinstance(key, slice):
            if not (key.step is None or key.step == 1):
                raise ValueError("cannot support not-default step in a slice")
            loc = self._convert_slice_indexer(key, kind="getitem")
        else:
            loc = self.get_loc(key)
        return series.iloc[loc]
