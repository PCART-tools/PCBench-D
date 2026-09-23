    @final
    def _validate_sort_keyword(self, sort):
        if sort not in [None, False, True]:
            raise ValueError(
                "The 'sort' keyword only takes the values of "
                f"None, True, or False; {sort} was passed."
            )
