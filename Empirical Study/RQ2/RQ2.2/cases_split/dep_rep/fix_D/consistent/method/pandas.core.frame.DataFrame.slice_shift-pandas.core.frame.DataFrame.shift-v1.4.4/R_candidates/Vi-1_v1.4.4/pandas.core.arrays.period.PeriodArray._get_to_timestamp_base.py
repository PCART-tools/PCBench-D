    def _get_to_timestamp_base(self) -> int:
        """
        Return frequency code group used for base of to_timestamp against
        frequency code.

        Return day freq code against longer freq than day.
        Return second freq code against hour between second.

        Returns
        -------
        int
        """
        base = self._dtype._dtype_code
        if base < FreqGroup.FR_BUS.value:
            return FreqGroup.FR_DAY.value
        elif FreqGroup.FR_HR.value <= base <= FreqGroup.FR_SEC.value:
            return FreqGroup.FR_SEC.value
        return base
