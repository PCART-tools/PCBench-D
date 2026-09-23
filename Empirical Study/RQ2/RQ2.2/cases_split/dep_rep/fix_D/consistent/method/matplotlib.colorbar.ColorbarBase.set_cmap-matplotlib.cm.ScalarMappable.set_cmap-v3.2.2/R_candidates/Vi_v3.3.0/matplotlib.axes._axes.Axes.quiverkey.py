    @docstring.copy(mquiver.QuiverKey.__init__)
    def quiverkey(self, Q, X, Y, U, label, **kw):
        qk = mquiver.QuiverKey(Q, X, Y, U, label, **kw)
        self.add_artist(qk)
        return qk
