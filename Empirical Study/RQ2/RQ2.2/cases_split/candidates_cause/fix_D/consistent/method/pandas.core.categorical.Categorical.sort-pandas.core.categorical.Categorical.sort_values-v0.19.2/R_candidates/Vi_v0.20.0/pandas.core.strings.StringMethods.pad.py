    @copy(str_pad)
    def pad(self, width, side='left', fillchar=' '):
        result = str_pad(self._data, width, side=side, fillchar=fillchar)
        return self._wrap_result(result)
