    def push_state(self) -> None:
        """Push a new `State` onto the stack, copying the current state."""
        self._state_stack.append(self.get_state().copy())
