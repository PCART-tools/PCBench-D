    @property
    def max_len(self) -> int:
        """
        :obj:`int`: **Deprecated** Kept here for backward compatibility. Now renamed to :obj:`model_max_length` to
        avoid ambiguity.
        """
        warnings.warn(
            "The `max_len` attribute has been deprecated and will be removed in a future version, use `model_max_length` instead.",
            FutureWarning,
        )
        return self.model_max_length
