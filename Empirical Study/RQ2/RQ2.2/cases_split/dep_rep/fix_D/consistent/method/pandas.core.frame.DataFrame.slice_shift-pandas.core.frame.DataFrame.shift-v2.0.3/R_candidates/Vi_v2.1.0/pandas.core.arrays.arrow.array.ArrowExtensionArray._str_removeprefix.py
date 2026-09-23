    def _str_removeprefix(self, prefix: str):
        # TODO: Should work once https://github.com/apache/arrow/issues/14991 is fixed
        # starts_with = pc.starts_with(self._pa_array, pattern=prefix)
        # removed = pc.utf8_slice_codeunits(self._pa_array, len(prefix))
        # result = pc.if_else(starts_with, removed, self._pa_array)
        # return type(self)(result)
        predicate = lambda val: val.removeprefix(prefix)
        result = self._apply_elementwise(predicate)
        return type(self)(pa.chunked_array(result))
