    def dict(self, *, loc_prefix=None):
        loc = self.loc if loc_prefix is None else loc_prefix + self.loc

        d = {
            'loc': loc,
            'msg': self.msg,
            'type': self.type_,
        }

        if self.ctx is not None:
            d['ctx'] = self.ctx

        return d
