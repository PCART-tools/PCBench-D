    @_dispatch(140, state=_dvistate.inpage)
    def _eop(self, _):
        self.state = _dvistate.outer
        del self.h, self.v, self.w, self.x, self.y, self.z, self.stack
