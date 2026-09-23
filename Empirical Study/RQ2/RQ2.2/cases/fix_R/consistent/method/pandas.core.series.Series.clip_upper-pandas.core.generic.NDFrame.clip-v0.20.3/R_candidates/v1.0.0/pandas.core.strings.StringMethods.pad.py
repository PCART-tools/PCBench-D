    @copy(str_pad)
    @forbid_nonstring_types(["bytes"])
    def pad(self, width, side="left", fillchar=" "):
        result = str_pad(self._parent, width, side=side, fillchar=fillchar)
        return self._wrap_result(result)
