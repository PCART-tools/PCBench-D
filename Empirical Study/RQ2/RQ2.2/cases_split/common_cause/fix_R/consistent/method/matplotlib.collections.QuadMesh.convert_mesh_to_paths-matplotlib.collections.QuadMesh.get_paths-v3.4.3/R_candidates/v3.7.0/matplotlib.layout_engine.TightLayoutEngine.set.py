    def set(self, *, pad=None, w_pad=None, h_pad=None, rect=None):
        for td in self.set.__kwdefaults__:
            if locals()[td] is not None:
                self._params[td] = locals()[td]
