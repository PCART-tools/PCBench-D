    @cached_property
    def validators(self):
        # These validators can't be added at field initialization time since
        # they're based on values retrieved from `connection`.
        validators_ = super().validators
        internal_type = self.get_internal_type()
        min_value, max_value = connection.ops.integer_field_range(internal_type)
        if min_value is not None:
            for validator in validators_:
                if isinstance(validator, validators.MinValueValidator) and validator.limit_value >= min_value:
                    break
            else:
                validators_.append(validators.MinValueValidator(min_value))
        if max_value is not None:
            for validator in validators_:
                if isinstance(validator, validators.MaxValueValidator) and validator.limit_value <= max_value:
                    break
            else:
                validators_.append(validators.MaxValueValidator(max_value))
        return validators_
