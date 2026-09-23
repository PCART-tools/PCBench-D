    @cached_property
    def allow_sliced_subqueries_with_in(self):
        return self.has_fetch_offset_support
