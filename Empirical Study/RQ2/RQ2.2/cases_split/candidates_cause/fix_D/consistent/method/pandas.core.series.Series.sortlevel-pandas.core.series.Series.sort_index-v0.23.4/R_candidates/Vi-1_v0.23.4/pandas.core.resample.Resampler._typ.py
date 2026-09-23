    @property
    def _typ(self):
        """ masquerade for compat as a Series or a DataFrame """
        if isinstance(self._selected_obj, pd.Series):
            return 'series'
        return 'dataframe'
