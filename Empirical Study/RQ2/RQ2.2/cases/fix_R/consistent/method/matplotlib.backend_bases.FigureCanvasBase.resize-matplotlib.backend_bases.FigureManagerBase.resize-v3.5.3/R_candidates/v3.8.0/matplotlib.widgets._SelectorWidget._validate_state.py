    def _validate_state(self, state):
        supported_state = [
            key for key, value in self._state_modifier_keys.items()
            if key != 'clear' and value != 'not-applicable'
            ]
        _api.check_in_list(supported_state, state=state)
