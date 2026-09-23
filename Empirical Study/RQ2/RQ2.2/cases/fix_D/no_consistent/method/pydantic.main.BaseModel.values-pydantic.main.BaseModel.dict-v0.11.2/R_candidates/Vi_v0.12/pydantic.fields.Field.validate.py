    def validate(self, v, values, *, loc, cls=None):  # noqa: C901 (ignore complexity)
        if self.allow_none and v is None:
            return None, None

        loc = loc if isinstance(loc, tuple) else (loc, )

        if self.parse_json:
            v, error = self._validate_json(v, loc)
            if error:
                return v, error

        if self.whole_pre_validators:
            v, errors = self._apply_validators(v, values, loc, cls, self.whole_pre_validators)
            if errors:
                return v, errors

        if self.shape is Shape.SINGLETON:
            v, errors = self._validate_singleton(v, values, loc, cls)
        elif self.shape is Shape.MAPPING:
            v, errors = self._validate_mapping(v, values, loc, cls)
        elif self.shape is Shape.TUPLE:
            v, errors = self._validate_tuple(v, values, loc, cls)
        else:
            # list or set
            v, errors = self._validate_list_set(v, values, loc, cls)
            if not errors and self.shape is Shape.SET:
                v = set(v)

        if not errors and self.whole_post_validators:
            v, errors = self._apply_validators(v, values, loc, cls, self.whole_post_validators)
        return v, errors
