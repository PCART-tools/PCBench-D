    def _check_method(self, method):
        if method is None:
            return

        if method in ["bfill", "backfill", "pad", "ffill", "nearest"]:
            raise NotImplementedError(
                f"method {method} not yet implemented for IntervalIndex"
            )

        raise ValueError("Invalid fill method")
