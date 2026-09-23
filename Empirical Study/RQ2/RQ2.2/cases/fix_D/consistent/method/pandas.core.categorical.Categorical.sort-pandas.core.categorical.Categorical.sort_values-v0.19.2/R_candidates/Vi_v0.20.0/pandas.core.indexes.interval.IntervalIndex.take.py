    @Appender(_index_shared_docs['take'] % _index_doc_kwargs)
    def take(self, indices, axis=0, allow_fill=True,
             fill_value=None, **kwargs):
        nv.validate_take(tuple(), kwargs)
        indices = _ensure_platform_int(indices)
        left, right = self.left, self.right

        if fill_value is None:
            fill_value = self._na_value
        mask = indices == -1

        if not mask.any():
            # we won't change dtype here in this case
            # if we don't need
            allow_fill = False

        taker = lambda x: x.take(indices, allow_fill=allow_fill,
                                 fill_value=fill_value)

        try:
            new_left = taker(left)
            new_right = taker(right)
        except ValueError:

            # we need to coerce; migth have NA's in an
            # interger dtype
            new_left = taker(left.astype(float))
            new_right = taker(right.astype(float))

        return self._shallow_copy(new_left, new_right)
