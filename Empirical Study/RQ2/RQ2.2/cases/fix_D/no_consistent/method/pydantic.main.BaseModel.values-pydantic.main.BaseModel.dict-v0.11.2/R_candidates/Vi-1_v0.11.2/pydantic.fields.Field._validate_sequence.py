    def _validate_sequence(self, v, values, loc, cls):
        result, errors = [], []

        for i, v_ in enumerate(v):
            v_loc = *loc, i
            single_result, single_errors = self._validate_singleton(v_, values, v_loc, cls)
            if single_errors:
                errors.append(single_errors)
            else:
                result.append(single_result)

        if errors:
            return v, errors
        else:
            return result, None
