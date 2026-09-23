    @Appender(_shared_docs["casemethods"] % _doc_args["upper"])
    @forbid_nonstring_types(["bytes"])
    def upper(self):
        result = self._data.array._str_upper()
        return self._wrap_result(result)
