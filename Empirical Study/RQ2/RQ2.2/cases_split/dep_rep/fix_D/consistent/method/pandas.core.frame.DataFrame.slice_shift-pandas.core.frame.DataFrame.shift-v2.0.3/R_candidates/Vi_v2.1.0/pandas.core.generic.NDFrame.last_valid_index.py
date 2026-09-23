    @final
    @doc(first_valid_index, position="last", klass=_shared_doc_kwargs["klass"])
    def last_valid_index(self) -> Hashable | None:
        return self._find_valid_index(how="last")
