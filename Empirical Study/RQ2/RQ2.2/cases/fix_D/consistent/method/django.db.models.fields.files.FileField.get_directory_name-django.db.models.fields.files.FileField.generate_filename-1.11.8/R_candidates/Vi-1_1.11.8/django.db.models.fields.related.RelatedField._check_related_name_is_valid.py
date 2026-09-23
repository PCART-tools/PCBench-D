    def _check_related_name_is_valid(self):
        import re
        import keyword
        related_name = self.remote_field.related_name
        if related_name is None:
            return []
        is_valid_id = True
        if keyword.iskeyword(related_name):
            is_valid_id = False
        if six.PY3:
            if not related_name.isidentifier():
                is_valid_id = False
        else:
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\Z', related_name):
                is_valid_id = False
        if not (is_valid_id or related_name.endswith('+')):
            return [
                checks.Error(
                    "The name '%s' is invalid related_name for field %s.%s" %
                    (self.remote_field.related_name, self.model._meta.object_name,
                     self.name),
                    hint="Related name must be a valid Python identifier or end with a '+'",
                    obj=self,
                    id='fields.E306',
                )
            ]
        return []
