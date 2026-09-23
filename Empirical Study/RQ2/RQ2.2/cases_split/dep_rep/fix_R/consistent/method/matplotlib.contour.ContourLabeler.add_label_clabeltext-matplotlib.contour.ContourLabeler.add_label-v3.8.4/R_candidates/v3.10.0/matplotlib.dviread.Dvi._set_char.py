    @_dispatch(min=128, max=131, state=_dvistate.inpage, args=('olen1',))
    def _set_char(self, char):
        self._put_char_real(char)
        if isinstance(self.fonts[self.f], cbook._ExceptionInfo):
            return
        self.h += self.fonts[self.f]._width_of(char)
