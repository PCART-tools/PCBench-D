    def _get_unit(self):
        # docstring inherited
        freq = self.rule._rrule._freq
        return self.get_unit_generic(freq)
