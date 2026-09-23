    def to_list(self):
        """
        Alias for tolist.
        """
        # GH#51254
        warnings.warn(
            "Categorical.to_list is deprecated and will be removed in a future "
            "version. Use obj.tolist() instead",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self.tolist()
