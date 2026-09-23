    def _validate_sort_keyword(self, sort):
        if sort not in [None, False]:
            raise ValueError(
                "The 'sort' keyword only takes the values of "
                "None or False; {0} was passed.".format(sort)
            )
