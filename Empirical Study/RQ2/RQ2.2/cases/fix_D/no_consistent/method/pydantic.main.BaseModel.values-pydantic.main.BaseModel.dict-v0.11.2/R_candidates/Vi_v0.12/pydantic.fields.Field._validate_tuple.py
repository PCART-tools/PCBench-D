    def _validate_tuple(self, v, values, loc, cls):
        e = None
        if not list_like(v):
            e = errors_.TupleError()
        else:
            actual_length, expected_length = len(v), len(self.sub_fields)
            if actual_length != expected_length:
                e = errors_.TupleLengthError(actual_length=actual_length, expected_length=expected_length)

        if e:
            return v, ErrorWrapper(e, loc=loc, config=self.model_config)

        result, errors = [], []
        for i, (v_, field) in enumerate(zip(v, self.sub_fields)):
            v_loc = *loc, i
            r, e = field.validate(v_, values, loc=v_loc, cls=cls)
            if e:
                errors.append(e)
            else:
                result.append(r)

        if errors:
            return v, errors
        else:
            return tuple(result), None
