    def _add_delta(self, delta):
        if isinstance(delta, (Tick, timedelta, np.timedelta64)):
            new_values = self._add_delta_td(delta)
            name = self.name
        elif isinstance(delta, TimedeltaIndex):
            new_values = self._add_delta_tdi(delta)
            # update name when delta is index
            name = com._maybe_match_name(self, delta)
        else:
            raise ValueError("cannot add the type {0} to a TimedeltaIndex"
                             .format(type(delta)))

        result = TimedeltaIndex(new_values, freq='infer', name=name)
        return result
