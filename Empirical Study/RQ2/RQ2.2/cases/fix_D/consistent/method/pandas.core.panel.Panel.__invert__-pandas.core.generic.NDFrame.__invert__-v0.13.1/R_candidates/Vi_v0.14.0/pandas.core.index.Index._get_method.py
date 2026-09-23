    def _get_method(self, method):
        if method:
            method = method.lower()

        aliases = {
            'ffill': 'pad',
            'bfill': 'backfill'
        }
        return aliases.get(method, method)
