    def _validate_mapping(self, v, values, cls):
        if isinstance(v, dict):
            v_iter = v
        else:
            try:
                v_iter = dict(v)
            except TypeError:
                return v, Error(TypeError(f'value is not a valid dict, got {type_display(type(v))}'), None, None)

        result, errors = {}, []
        for k, v_ in v_iter.items():
            key_result, key_errors = self.key_field.validate(k, values, 'key', cls)
            if key_errors:
                errors.append(key_errors)
                continue
            value_result, value_errors = self._validate_singleton(v_, values, k, cls)
            if value_errors:
                errors.append(value_errors)
                continue
            result[key_result] = value_result
        if errors:
            return v, errors
        else:
            return result, None
