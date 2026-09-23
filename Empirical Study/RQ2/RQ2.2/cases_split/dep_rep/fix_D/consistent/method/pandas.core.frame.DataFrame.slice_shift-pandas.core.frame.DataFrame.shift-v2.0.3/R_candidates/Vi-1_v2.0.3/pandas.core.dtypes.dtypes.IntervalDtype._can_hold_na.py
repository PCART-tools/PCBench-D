    @cache_readonly
    def _can_hold_na(self) -> bool:
        subtype = self._subtype
        if subtype is None:
            # partially-initialized
            raise NotImplementedError(
                "_can_hold_na is not defined for partially-initialized IntervalDtype"
            )
        if subtype.kind in ["i", "u"]:
            return False
        return True
