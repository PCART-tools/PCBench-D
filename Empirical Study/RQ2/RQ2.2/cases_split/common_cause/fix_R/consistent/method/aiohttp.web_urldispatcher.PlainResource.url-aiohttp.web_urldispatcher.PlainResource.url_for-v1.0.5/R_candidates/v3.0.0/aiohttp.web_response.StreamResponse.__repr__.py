    def __repr__(self):
        if self._eof_sent:
            info = "eof"
        elif self.prepared:
            info = "{} {} ".format(self._req.method, self._req.path)
        else:
            info = "not prepared"
        return "<{} {} {}>".format(self.__class__.__name__,
                                   self.reason, info)
