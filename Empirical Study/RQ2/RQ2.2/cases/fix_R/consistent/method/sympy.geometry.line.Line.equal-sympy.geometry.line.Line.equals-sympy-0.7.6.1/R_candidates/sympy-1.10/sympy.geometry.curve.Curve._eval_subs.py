    def _eval_subs(self, old, new):
        if old == self.parameter:
            return Point(*[f.subs(old, new) for f in self.functions])
