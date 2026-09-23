    @Appender(_shared_docs["casemethods"] % _doc_args["casefold"])
    @forbid_nonstring_types(["bytes"])
    def casefold(self):
        result = self._data.array._str_casefold()
        return self._wrap_result(result)
