    def _local_dir(self):
        return sorted(set(self.obj._local_dir() + list(self._apply_whitelist)))
