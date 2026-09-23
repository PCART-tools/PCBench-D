    def _validate_singleton(self, v, values, index, cls):
        if self.sub_fields:
            errors = []
            for field in self.sub_fields:
                value, error = field.validate(v, values, index, cls)
                if error:
                    errors.append(error)
                else:
                    return value, None
            return v, errors[0] if len(self.sub_fields) == 1 else errors
        else:
            return self._apply_validators(v, values, index, cls, self.validators)
