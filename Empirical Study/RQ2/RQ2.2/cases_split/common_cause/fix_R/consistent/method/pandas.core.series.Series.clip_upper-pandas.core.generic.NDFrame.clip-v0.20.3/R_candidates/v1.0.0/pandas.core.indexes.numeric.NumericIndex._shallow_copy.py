    @Appender(_index_shared_docs["_shallow_copy"])
    def _shallow_copy(self, values=None, **kwargs):
        if values is not None and not self._can_hold_na:
            # Ensure we are not returning an Int64Index with float data:
            return self._shallow_copy_with_infer(values=values, **kwargs)
        return super()._shallow_copy(values=values, **kwargs)
