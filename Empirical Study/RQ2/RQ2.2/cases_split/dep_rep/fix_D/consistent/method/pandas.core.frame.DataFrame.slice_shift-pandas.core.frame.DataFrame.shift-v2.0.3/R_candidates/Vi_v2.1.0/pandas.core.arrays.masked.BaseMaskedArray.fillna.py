    @doc(ExtensionArray.fillna)
    def fillna(
        self, value=None, method=None, limit: int | None = None, copy: bool = True
    ) -> Self:
        value, method = validate_fillna_kwargs(value, method)

        mask = self._mask

        value = missing.check_value_size(value, mask, len(self))

        if mask.any():
            if method is not None:
                func = missing.get_fill_func(method, ndim=self.ndim)
                npvalues = self._data.T
                new_mask = mask.T
                if copy:
                    npvalues = npvalues.copy()
                    new_mask = new_mask.copy()
                func(npvalues, limit=limit, mask=new_mask)
                return self._simple_new(npvalues.T, new_mask.T)
            else:
                # fill with value
                if copy:
                    new_values = self.copy()
                else:
                    new_values = self[:]
                new_values[mask] = value
        else:
            if copy:
                new_values = self.copy()
            else:
                new_values = self[:]
        return new_values
