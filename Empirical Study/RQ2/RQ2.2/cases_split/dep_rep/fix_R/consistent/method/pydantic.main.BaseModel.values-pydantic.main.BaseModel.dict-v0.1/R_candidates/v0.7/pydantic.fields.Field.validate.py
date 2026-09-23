    def validate(self, v, values, index=None, cls=None):
        if self.allow_none and v is None:
            return None, None

        if self.whole_pre_validators:
            v, errors = self._apply_validators(v, values, index, cls, self.whole_pre_validators)
            if errors:
                return v, errors

        if self.shape is Shape.SINGLETON:
            v, errors = self._validate_singleton(v, values, index, cls)
        elif self.shape is Shape.MAPPING:
            v, errors = self._validate_mapping(v, values, cls)
        else:
            # list or set
            v, errors = self._validate_sequence(v, values, cls)
            if not errors and self.shape is Shape.SET:
                v = set(v)

        if not errors and self.whole_post_validators:
            v, errors = self._apply_validators(v, values, index, cls, self.whole_post_validators)
        return v, errors
