    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.remote_field.limit_choices_to:
            kwargs['limit_choices_to'] = self.remote_field.limit_choices_to
        if self.remote_field.related_name is not None:
            kwargs['related_name'] = self.remote_field.related_name
        if self.remote_field.related_query_name is not None:
            kwargs['related_query_name'] = self.remote_field.related_query_name
        return name, path, args, kwargs
