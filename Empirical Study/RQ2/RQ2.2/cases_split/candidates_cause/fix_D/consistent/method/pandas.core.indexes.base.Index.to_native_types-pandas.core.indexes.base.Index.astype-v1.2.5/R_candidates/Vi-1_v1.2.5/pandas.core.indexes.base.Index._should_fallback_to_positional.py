    def _should_fallback_to_positional(self) -> bool:
        """
        Should an integer key be treated as positional?
        """
        if self.holds_integer() or self.is_boolean():
            return False
        return True
