    def _dir_additions(self):
        return self.obj._dir_additions() | self._apply_whitelist
