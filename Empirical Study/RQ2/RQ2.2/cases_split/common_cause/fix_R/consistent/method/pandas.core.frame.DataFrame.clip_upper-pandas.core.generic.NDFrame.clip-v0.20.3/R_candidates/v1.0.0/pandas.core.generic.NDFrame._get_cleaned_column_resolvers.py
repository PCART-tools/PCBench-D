    def _get_cleaned_column_resolvers(self) -> Dict[str, ABCSeries]:
        """
        Return the special character free column resolvers of a dataframe.

        Column names with special characters are 'cleaned up' so that they can
        be referred to by backtick quoting.
        Used in :meth:`DataFrame.eval`.
        """
        from pandas.core.computation.parsing import clean_column_name

        if isinstance(self, ABCSeries):
            return {clean_column_name(self.name): self}

        return {
            clean_column_name(k): v for k, v in self.items() if not isinstance(k, int)
        }
