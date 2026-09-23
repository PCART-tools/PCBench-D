    def prepare(self):
        if self.default is not None and self.type_ is None:
            self.type_ = type(self.default)

        if self.type_ is None:
            raise errors_.ConfigError(f'unable to infer type for attribute "{self.name}"')

        self.validate_always: bool = (
            getattr(self.type_, 'validate_always', False) or any(v.always for v in self.class_validators)
        )

        if not self.required and not self.validate_always and self.default is None:
            self.allow_none = True

        self._populate_sub_fields()
        self._populate_validators()
