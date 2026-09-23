    def _check_null(self, **kwargs):
        if getattr(self, 'null', False):
            return [
                checks.Error(
                    'BooleanFields do not accept null values.',
                    hint='Use a NullBooleanField instead.',
                    obj=self,
                    id='fields.E110',
                )
            ]
        else:
            return []
