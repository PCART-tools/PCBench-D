    def _check_method(self, method):
        if method is None:
            return

        if method in ['bfill', 'backfill', 'pad', 'ffill', 'nearest']:
            raise NotImplementedError(
                'method {} not yet implemented for '
                'IntervalIndex'.format(method))

        raise ValueError("Invalid fill method")
