    @Appender(_index_shared_docs["take"] % _index_doc_kwargs)
    def take(self, indices, axis=0, allow_fill=True, fill_value=None, **kwargs):
        if kwargs:
            nv.validate_take(tuple(), kwargs)
        indices = ensure_platform_int(indices)
        if self._can_hold_na:
            taken = self._assert_take_fillable(
                self.values,
                indices,
                allow_fill=allow_fill,
                fill_value=fill_value,
                na_value=self._na_value,
            )
        else:
            if allow_fill and fill_value is not None:
                cls_name = type(self).__name__
                raise ValueError(
                    f"Unable to fill values because {cls_name} cannot contain NA"
                )
            taken = self.values.take(indices)
        return self._shallow_copy(taken)
