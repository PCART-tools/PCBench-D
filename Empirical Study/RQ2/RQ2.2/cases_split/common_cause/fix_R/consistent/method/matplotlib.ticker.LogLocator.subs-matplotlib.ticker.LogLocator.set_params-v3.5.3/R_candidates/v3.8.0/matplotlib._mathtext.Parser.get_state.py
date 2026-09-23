    def get_state(self) -> ParserState:
        """Get the current `State` of the parser."""
        return self._state_stack[-1]
