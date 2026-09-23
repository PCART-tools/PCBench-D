    @final
    def _check_inplace_and_allows_duplicate_labels(self, inplace):
        if inplace and not self.flags.allows_duplicate_labels:
            raise ValueError(
                "Cannot specify 'inplace=True' when "
                "'self.flags.allows_duplicate_labels' is False."
            )
