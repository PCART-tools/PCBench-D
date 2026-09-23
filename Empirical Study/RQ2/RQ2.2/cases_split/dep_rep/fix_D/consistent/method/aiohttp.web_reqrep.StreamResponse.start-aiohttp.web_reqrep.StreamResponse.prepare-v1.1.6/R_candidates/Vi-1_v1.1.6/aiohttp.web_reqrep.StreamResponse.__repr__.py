    def __repr__(self):
        if self.started:
            info = "{} {} ".format(self._req.method, self._req.path)
        else:
            info = "not started"
        return "<{} {} {}>".format(self.__class__.__name__,
                                   self.reason, info)
