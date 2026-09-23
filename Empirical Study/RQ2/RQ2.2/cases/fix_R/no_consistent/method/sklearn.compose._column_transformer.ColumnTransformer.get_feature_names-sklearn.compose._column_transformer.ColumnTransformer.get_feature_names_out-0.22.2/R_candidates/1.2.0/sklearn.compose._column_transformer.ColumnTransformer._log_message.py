    def _log_message(self, name, idx, total):
        if not self.verbose:
            return None
        return "(%d of %d) Processing %s" % (idx, total, name)
