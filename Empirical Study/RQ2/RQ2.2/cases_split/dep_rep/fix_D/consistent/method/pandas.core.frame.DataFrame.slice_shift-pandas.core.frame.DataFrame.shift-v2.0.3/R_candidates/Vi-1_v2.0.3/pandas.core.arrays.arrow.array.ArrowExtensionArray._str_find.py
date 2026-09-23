    def _str_find(self, sub: str, start: int = 0, end: int | None = None):
        if start != 0 and end is not None:
            slices = pc.utf8_slice_codeunits(self._data, start, stop=end)
            result = pc.find_substring(slices, sub)
            not_found = pc.equal(result, -1)
            offset_result = pc.add(result, end - start)
            result = pc.if_else(not_found, result, offset_result)
        elif start == 0 and end is None:
            slices = self._data
            result = pc.find_substring(slices, sub)
        else:
            raise NotImplementedError(
                f"find not implemented with {sub=}, {start=}, {end=}"
            )
        return type(self)(result)
