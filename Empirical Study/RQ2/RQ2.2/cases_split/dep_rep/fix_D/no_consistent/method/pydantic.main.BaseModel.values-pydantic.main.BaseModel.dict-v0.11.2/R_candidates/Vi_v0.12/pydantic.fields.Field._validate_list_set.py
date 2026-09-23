    def _validate_list_set(self, v, values, loc, cls):
        if not list_like(v):
            e = errors_.ListError() if self.shape is Shape.LIST else errors_.SetError()
            return v, ErrorWrapper(e, loc=loc, config=self.model_config)

        result, errors = [], []
        for i, v_ in enumerate(v):
            v_loc = *loc, i
            r, e = self._validate_singleton(v_, values, v_loc, cls)
            if e:
                errors.append(e)
            else:
                result.append(r)

        if errors:
            return v, errors
        else:
            return result, None
