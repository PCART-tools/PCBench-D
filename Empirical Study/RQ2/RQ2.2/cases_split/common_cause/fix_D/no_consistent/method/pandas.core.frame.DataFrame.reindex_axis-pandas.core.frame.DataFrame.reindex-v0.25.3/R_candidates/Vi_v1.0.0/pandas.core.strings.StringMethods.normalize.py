    @forbid_nonstring_types(["bytes"])
    def normalize(self, form):
        """
        Return the Unicode normal form for the strings in the Series/Index.
        For more information on the forms, see the
        :func:`unicodedata.normalize`.

        Parameters
        ----------
        form : {'NFC', 'NFKC', 'NFD', 'NFKD'}
            Unicode form.

        Returns
        -------
        normalized : Series/Index of objects
        """
        import unicodedata

        f = lambda x: unicodedata.normalize(form, x)
        result = _na_map(f, self._parent, dtype=str)
        return self._wrap_result(result)
