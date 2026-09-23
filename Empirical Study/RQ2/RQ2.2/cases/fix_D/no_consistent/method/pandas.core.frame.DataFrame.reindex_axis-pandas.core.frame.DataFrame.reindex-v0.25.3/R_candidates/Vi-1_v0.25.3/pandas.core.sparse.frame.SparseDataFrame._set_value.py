    def _set_value(self, index, col, value, takeable=False):
        dense = self.to_dense()._set_value(index, col, value, takeable=takeable)
        return dense.to_sparse(
            kind=self._default_kind, fill_value=self._default_fill_value
        )
