    @Appender(_index_shared_docs['fillna'] % _sparray_doc_kwargs)
    def fillna(self, value, downcast=None):
        if downcast is not None:
            raise NotImplementedError

        if issubclass(self.dtype.type, np.floating):
            value = float(value)

        if self._null_fill_value:
            return self._simple_new(self.sp_values, self.sp_index,
                                    fill_value=value)
        else:
            new_values = self.sp_values.copy()
            new_values[isnull(new_values)] = value
            return self._simple_new(new_values, self.sp_index,
                                    fill_value=self.fill_value)
