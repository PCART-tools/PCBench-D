    def quiverkey(self, *args, **kw):
        qk = mquiver.QuiverKey(*args, **kw)
        self.add_artist(qk)
        return qk
