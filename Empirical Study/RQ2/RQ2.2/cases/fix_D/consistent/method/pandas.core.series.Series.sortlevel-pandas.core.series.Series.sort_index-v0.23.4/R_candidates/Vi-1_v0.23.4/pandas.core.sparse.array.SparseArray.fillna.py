    @Appender(_index_shared_docs['fillna'] % _sparray_doc_kwargs)
    def fillna(self, value, downcast=None):
        if downcast is not None:
            raise NotImplementedError

        if issubclass(self.dtype.type, np.floating):
            value = float(value)

        new_values = np.where(isna(self.sp_values), value, self.sp_values)
        fill_value = value if self._null_fill_value else self.fill_value

        return self._simple_new(new_values, self.sp_index,
                                fill_value=fill_value)
