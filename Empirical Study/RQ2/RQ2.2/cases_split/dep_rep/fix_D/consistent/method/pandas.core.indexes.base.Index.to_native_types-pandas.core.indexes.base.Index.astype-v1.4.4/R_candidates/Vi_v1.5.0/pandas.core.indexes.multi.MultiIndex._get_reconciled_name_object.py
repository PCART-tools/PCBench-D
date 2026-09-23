    def _get_reconciled_name_object(self, other) -> MultiIndex:
        """
        If the result of a set operation will be self,
        return self, unless the names change, in which
        case make a shallow copy of self.
        """
        names = self._maybe_match_names(other)
        if self.names != names:
            # Incompatible return value type (got "Optional[MultiIndex]", expected
            # "MultiIndex")
            return self.rename(names)  # type: ignore[return-value]
        return self
