    @final
    @cache_readonly
    def result_arraylike(self) -> ArrayLike:
        """
        Analogous to result_index, but returning an ndarray/ExtensionArray
        allowing us to retain ExtensionDtypes not supported by Index.
        """
        # TODO(ExtensionIndex): once Index supports arbitrary EAs, this can
        #  be removed in favor of result_index
        if len(self.groupings) == 1:
            return self.groupings[0].group_arraylike

        # result_index is MultiIndex
        return self.result_index._values
