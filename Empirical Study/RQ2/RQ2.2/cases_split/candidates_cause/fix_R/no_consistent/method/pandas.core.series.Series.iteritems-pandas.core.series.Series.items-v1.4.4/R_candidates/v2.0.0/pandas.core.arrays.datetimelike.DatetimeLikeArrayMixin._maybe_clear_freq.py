    def _maybe_clear_freq(self) -> None:
        # inplace operations like __setitem__ may invalidate the freq of
        # DatetimeArray and TimedeltaArray
        pass
