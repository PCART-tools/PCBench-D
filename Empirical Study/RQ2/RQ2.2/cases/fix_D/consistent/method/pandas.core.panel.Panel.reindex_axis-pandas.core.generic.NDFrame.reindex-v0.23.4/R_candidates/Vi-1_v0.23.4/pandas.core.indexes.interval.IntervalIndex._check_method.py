    def _check_method(self, method):
        if method is None:
            return

        if method in ['bfill', 'backfill', 'pad', 'ffill', 'nearest']:
            msg = 'method {method} not yet implemented for IntervalIndex'
            raise NotImplementedError(msg.format(method=method))

        raise ValueError("Invalid fill method")
