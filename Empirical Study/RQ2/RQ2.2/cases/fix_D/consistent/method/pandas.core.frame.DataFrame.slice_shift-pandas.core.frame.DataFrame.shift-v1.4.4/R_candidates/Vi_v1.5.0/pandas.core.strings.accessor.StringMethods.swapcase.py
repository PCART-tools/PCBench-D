    @Appender(_shared_docs["casemethods"] % _doc_args["swapcase"])
    @forbid_nonstring_types(["bytes"])
    def swapcase(self):
        result = self._data.array._str_swapcase()
        return self._wrap_result(result)
