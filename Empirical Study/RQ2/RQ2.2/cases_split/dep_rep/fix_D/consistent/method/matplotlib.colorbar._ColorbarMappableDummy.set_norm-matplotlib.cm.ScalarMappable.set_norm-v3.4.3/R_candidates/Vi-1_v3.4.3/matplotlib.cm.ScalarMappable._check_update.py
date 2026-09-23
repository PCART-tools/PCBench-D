    def _check_update(self, checker):
        """Return whether mappable has changed since the last check."""
        if self._update_dict[checker]:
            self._update_dict[checker] = False
            return True
        return False
