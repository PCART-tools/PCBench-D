    def _str_removeprefix(self, prefix: str):
        # TODO: Should work once https://github.com/apache/arrow/issues/14991 is fixed
        # starts_with = pc.starts_with(self._data, pattern=prefix)
        # removed = pc.utf8_slice_codeunits(self._data, len(prefix))
        # result = pc.if_else(starts_with, removed, self._data)
        # return type(self)(result)
        if sys.version_info < (3, 9):
            # NOTE pyupgrade will remove this when we run it with --py39-plus
            # so don't remove the unnecessary `else` statement below
            from pandas.util._str_methods import removeprefix

            predicate = functools.partial(removeprefix, prefix=prefix)
        else:
            predicate = lambda val: val.removeprefix(prefix)
        result = self._apply_elementwise(predicate)
        return type(self)(pa.chunked_array(result))
