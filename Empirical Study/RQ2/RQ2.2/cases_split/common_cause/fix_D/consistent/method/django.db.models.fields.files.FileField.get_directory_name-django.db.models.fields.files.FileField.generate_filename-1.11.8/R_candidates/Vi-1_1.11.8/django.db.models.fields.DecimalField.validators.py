    @cached_property
    def validators(self):
        return super(DecimalField, self).validators + [
            validators.DecimalValidator(self.max_digits, self.decimal_places)
        ]
