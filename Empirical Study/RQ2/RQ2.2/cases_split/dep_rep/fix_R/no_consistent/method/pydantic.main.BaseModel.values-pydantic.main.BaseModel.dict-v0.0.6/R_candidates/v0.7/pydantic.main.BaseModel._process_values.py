    def _process_values(self, input_data: dict) -> Dict[str, Any]:  # noqa: C901 (ignore complexity)
        values = {}
        errors = {}

        for name, field in self.__fields__.items():
            value = input_data.get(field.alias, MISSING)
            if value is MISSING:
                if self.__config__.validate_all or field.validate_always:
                    value = field.default
                else:
                    if field.required:
                        errors[field.alias] = MISSING_ERROR
                    else:
                        values[name] = field.default
                    continue

            v_, errors_ = field.validate(value, values, cls=self.__class__)
            if errors_:
                errors[field.alias] = errors_
            else:
                values[name] = v_

        if (not self.__config__.ignore_extra) or self.__config__.allow_extra:
            extra = input_data.keys() - {f.alias for f in self.__fields__.values()}
            if extra:
                if self.__config__.allow_extra:
                    for field in extra:
                        values[field] = input_data[field]
                else:
                    # config.ignore_extra is False
                    for field in sorted(extra):
                        errors[field] = EXTRA_ERROR

        if errors:
            raise ValidationError(errors)
        return values
