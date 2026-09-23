    def _apply_validators(self, v, values, loc, cls, validators):
        for signature, validator in validators:
            try:
                if signature is ValidatorSignature.JUST_VALUE:
                    v = validator(v)
                elif signature is ValidatorSignature.VALUE_KWARGS:
                    v = validator(v, values=values, config=self.model_config, field=self)
                elif signature is ValidatorSignature.CLS_JUST_VALUE:
                    v = validator(cls, v)
                else:
                    # ValidatorSignature.CLS_VALUE_KWARGS
                    v = validator(cls, v, values=values, config=self.model_config, field=self)
            except (ValueError, TypeError) as exc:
                return v, ErrorWrapper(exc, loc=loc, config=self.model_config)
        return v, None
