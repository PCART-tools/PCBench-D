    def normalize(self, form):
        """Return the Unicode normal form for the strings in the Series/Index.
        For more information on the forms, see the
        :func:`unicodedata.normalize`.

        Parameters
        ----------
        form : {'NFC', 'NFKC', 'NFD', 'NFKD'}
            Unicode form

        Returns
        -------
        normalized : Series/Index of objects
        """
        import unicodedata
        f = lambda x: unicodedata.normalize(form, compat.u_safe(x))
        result = _na_map(f, self.series)
        return self._wrap_result(result)
