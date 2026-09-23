    @_dispatch(min=166, max=170, state=_dvistate.inpage, args=('slen',))
    def _down_z(self, new_z):
        if new_z is not None:
            self.z = new_z
        self.v += self.z
