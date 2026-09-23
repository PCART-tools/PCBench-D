    @cache_readonly
    @final
    def _is_all_dates(self) -> bool:
        """
        Whether or not the index values only consist of dates.
        """
        if needs_i8_conversion(self.dtype):
            return True
        elif self.dtype != _dtype_obj:
            # TODO(ExtensionIndex): 3rd party EA might override?
            # Note: this includes IntervalIndex, even when the left/right
            #  contain datetime-like objects.
            return False
        elif self._is_multi:
            return False
        return is_datetime_array(ensure_object(self._values))
