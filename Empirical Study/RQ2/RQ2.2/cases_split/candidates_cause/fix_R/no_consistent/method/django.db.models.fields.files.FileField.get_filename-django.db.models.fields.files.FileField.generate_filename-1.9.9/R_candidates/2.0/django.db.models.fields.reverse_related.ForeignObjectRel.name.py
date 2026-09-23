    @cached_property
    def name(self):
        return self.field.related_query_name()
