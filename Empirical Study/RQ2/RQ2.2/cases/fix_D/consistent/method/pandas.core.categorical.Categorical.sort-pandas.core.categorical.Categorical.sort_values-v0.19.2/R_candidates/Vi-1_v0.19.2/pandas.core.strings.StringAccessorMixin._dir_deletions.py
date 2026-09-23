    def _dir_deletions(self):
        try:
            getattr(self, 'str')
        except AttributeError:
            return set(['str'])
        return set()
