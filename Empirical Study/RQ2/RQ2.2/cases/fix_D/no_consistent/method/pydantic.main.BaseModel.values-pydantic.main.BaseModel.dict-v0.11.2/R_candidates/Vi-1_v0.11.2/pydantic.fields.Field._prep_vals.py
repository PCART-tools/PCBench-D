    def _prep_vals(self, v_funcs):
        v = []
        for f in v_funcs:
            if not f or (self.allow_none and f is not_none_validator):
                continue
            v.append((
                _get_validator_signature(f),
                f,
            ))
        return tuple(v)
