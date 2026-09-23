    @final
    def _validate_sort_keyword(self, sort):
        if sort not in [None, False]:
            raise ValueError(
                "The 'sort' keyword only takes the values of "
                f"None or False; {sort} was passed."
            )
