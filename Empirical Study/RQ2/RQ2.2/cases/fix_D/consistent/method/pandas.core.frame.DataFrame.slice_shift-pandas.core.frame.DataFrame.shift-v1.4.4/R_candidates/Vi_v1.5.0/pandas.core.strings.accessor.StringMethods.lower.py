    @Appender(_shared_docs["casemethods"] % _doc_args["lower"])
    @forbid_nonstring_types(["bytes"])
    def lower(self):
        result = self._data.array._str_lower()
        return self._wrap_result(result)
