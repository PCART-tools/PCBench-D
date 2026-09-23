    @property
    def _from_selection(self) -> bool:
        """
        Is the resampling from a DataFrame column or MultiIndex level.
        """
        # upsampling and PeriodIndex resampling do not work
        # with selection, this state used to catch and raise an error
        return self._timegrouper is not None and (
            self._timegrouper.key is not None or self._timegrouper.level is not None
        )
