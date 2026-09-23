    def _get_space_character_free_column_resolvers(self):
        """Return the space character free column resolvers of a dataframe.

        Column names with spaces are 'cleaned up' so that they can be referred
        to by backtick quoting.
        Used in :meth:`DataFrame.eval`.
        """
        from pandas.core.computation.common import _remove_spaces_column_name

        return {_remove_spaces_column_name(k): v for k, v in self.items()}
