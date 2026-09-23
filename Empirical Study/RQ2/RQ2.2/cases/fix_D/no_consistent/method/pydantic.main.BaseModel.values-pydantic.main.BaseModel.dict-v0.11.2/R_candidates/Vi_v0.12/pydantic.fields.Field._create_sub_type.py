    def _create_sub_type(self, type_, name):
        return self.__class__(
            type_=type_,
            name=name,
            class_validators=self.class_validators,
            default=self.default,
            required=self.required,
            allow_none=self.allow_none,
            model_config=self.model_config,
        )
