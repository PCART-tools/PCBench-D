    def _should_fallback_to_positional(self) -> bool:
        """
        Should an integer key be treated as positional?
        """
        return not self.holds_integer() and not self.is_boolean()
