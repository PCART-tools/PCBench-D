    @final
    def __contains__(self, key) -> bool_t:
        """True if the key is in the info axis"""
        return key in self._info_axis
