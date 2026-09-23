    @cache_readonly
    def _engine(self):

        # we are going to look things up with the codes themselves
        return self._engine_type(lambda: self.codes.astype('i8'), len(self))
