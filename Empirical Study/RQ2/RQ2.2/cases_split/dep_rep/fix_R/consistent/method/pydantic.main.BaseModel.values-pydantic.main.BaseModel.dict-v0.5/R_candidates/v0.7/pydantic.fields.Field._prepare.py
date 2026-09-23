    def _prepare(self, class_validators):
        if self.default is not None and self.type_ is None:
            self.type_ = type(self.default)

        if self.type_ is None:
            raise ConfigError(f'unable to infer type for attribute "{self.name}"')

        if not self.required and not self.validate_always and self.default is None:
            self.allow_none = True

        self._populate_sub_fields(class_validators)
        self._populate_validators(class_validators)

        self.info = {
            'type': type_display(self.type_),
            'default': self.default,
            'required': self.required,
        }
        if self.required:
            self.info.pop('default')
        if self.sub_fields:
            self.info['sub_fields'] = self.sub_fields
        else:
            self.info['validators'] = [v[1].__qualname__ for v in self.validators]
