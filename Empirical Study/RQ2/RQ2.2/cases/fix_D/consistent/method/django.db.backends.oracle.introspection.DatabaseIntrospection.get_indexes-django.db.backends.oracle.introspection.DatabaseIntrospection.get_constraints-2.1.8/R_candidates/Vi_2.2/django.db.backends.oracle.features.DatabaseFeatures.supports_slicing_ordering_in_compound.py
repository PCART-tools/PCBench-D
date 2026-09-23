    @cached_property
    def supports_slicing_ordering_in_compound(self):
        return self.has_fetch_offset_support
