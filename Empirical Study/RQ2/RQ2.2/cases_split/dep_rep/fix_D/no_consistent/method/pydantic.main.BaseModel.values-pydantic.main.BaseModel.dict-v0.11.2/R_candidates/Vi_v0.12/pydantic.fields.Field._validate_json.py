    def _validate_json(self, v, loc):
        try:
            return Json.validate(v), None
        except (ValueError, TypeError) as exc:
            return v, ErrorWrapper(exc, loc=loc, config=self.model_config)
