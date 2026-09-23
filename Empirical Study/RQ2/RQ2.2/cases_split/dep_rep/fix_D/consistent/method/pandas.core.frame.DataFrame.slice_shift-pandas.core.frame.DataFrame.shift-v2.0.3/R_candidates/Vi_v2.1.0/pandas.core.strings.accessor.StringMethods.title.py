    @Appender(_shared_docs["casemethods"] % _doc_args["title"])
    @forbid_nonstring_types(["bytes"])
    def title(self):
        result = self._data.array._str_title()
        return self._wrap_result(result)
