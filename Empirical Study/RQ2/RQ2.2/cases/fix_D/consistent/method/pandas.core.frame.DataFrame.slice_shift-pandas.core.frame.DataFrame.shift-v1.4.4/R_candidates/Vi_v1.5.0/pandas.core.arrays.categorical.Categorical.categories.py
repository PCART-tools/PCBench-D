    @categories.setter
    def categories(self, categories) -> None:
        warn(
            "Setting categories in-place is deprecated and will raise in a "
            "future version. Use rename_categories instead.",
            FutureWarning,
            stacklevel=find_stack_level(inspect.currentframe()),
        )

        self._set_categories(categories)
