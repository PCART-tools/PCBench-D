    @_docstring.copy(mquiver.QuiverKey.__init__)
    def quiverkey(self, Q, X, Y, U, label, **kwargs):
        qk = mquiver.QuiverKey(Q, X, Y, U, label, **kwargs)
        self.add_artist(qk)
        return qk
