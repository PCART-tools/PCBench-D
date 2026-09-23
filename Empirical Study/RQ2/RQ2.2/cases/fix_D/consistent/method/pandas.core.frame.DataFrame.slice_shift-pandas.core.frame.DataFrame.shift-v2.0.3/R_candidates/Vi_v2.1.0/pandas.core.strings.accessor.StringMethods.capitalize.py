    @Appender(_shared_docs["casemethods"] % _doc_args["capitalize"])
    @forbid_nonstring_types(["bytes"])
    def capitalize(self):
        result = self._data.array._str_capitalize()
        return self._wrap_result(result)
