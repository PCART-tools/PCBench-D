    @property
    def _typ(self) -> str:
        """
        Masquerade for compat as a Series or a DataFrame.
        """
        if isinstance(self._selected_obj, ABCSeries):
            return "series"
        return "dataframe"
