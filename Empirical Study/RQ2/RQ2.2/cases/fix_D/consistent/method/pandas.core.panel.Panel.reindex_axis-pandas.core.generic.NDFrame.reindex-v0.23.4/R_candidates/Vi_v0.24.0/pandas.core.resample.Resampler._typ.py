    @property
    def _typ(self):
        """
        Masquerade for compat as a Series or a DataFrame.
        """
        if isinstance(self._selected_obj, pd.Series):
            return 'series'
        return 'dataframe'
