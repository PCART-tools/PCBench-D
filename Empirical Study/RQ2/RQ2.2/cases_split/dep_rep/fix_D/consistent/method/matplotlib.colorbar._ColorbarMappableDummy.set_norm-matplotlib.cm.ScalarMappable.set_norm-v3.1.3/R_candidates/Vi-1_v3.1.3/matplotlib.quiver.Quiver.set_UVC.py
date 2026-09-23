    def set_UVC(self, U, V, C=None):
        # We need to ensure we have a copy, not a reference
        # to an array that might change before draw().
        U = ma.masked_invalid(U, copy=True).ravel()
        V = ma.masked_invalid(V, copy=True).ravel()
        mask = ma.mask_or(U.mask, V.mask, copy=False, shrink=True)
        if C is not None:
            C = ma.masked_invalid(C, copy=True).ravel()
            mask = ma.mask_or(mask, C.mask, copy=False, shrink=True)
            if mask is ma.nomask:
                C = C.filled()
            else:
                C = ma.array(C, mask=mask, copy=False)
        self.U = U.filled(1)
        self.V = V.filled(1)
        self.Umask = mask
        if C is not None:
            self.set_array(C)
        self._new_UV = True
        self.stale = True
