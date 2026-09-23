    def validate(self, v, values, *, loc, cls=None):
        if self.allow_none and v is None:
            return None, None

        if not isinstance(loc, tuple):
            loc = (loc,)

        if self.whole_pre_validators:
            v, errors = self._apply_validators(v, values, loc, cls, self.whole_pre_validators)
            if errors:
                return v, errors

        if self.shape is Shape.SINGLETON:
            v, errors = self._validate_singleton(v, values, loc, cls)
        elif self.shape is Shape.MAPPING:
            v, errors = self._validate_mapping(v, values, loc, cls)
        else:
            # list or set
            if list_like(v):
                v, errors = self._validate_sequence(v, values, loc, cls)
                if not errors and self.shape is Shape.SET:
                    v = set(v)
            else:
                e = errors_.ListError() if self.shape is Shape.LIST else errors_.SetError()
                errors = ErrorWrapper(e, loc=loc, config=self.model_config)

        if not errors and self.whole_post_validators:
            v, errors = self._apply_validators(v, values, loc, cls, self.whole_post_validators)
        return v, errors
